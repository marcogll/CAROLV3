# CAROL v3 — Plan de Mejora y Despliegue

> **Estado:** Draft v1.0  
> **Creado:** 2026-06-01  
> **Repo:** [github.com/marcogll/CAROLV3](https://github.com/marcogll/CAROLV3)  
> **Deploy actual:** [carol.soul23.mx](https://carol.soul23.mx)

---

## 1. Problemas Identificados

### 🔴 Crítico: Datos no persisten en MySQL

| Síntoma | Causa probable | Impacto |
|---------|---------------|---------|
| Evaluaciones funcionan (98% score) pero no se guardan | `DB_HOST` no está configurado en el contenedor `app` o `pymysql` no está instalado | Sin historial de candidatos, sin reportes, sin admin panel |

**Diagnóstico técnico:**

En `server.py`:
```python
DB_HOST = os.getenv("DB_HOST", "")
# ...
if DB_HOST:
    try:
        import pymysql
        # ...
```

Si `DB_HOST` está vacío o `pymysql` falla al importar, el sistema **silenciosamente** cae a JSON files (`DATA_DIR = .carol_data/`). No hay error visible para el usuario.

En `docker-compose.yml`:
```yaml
app:
  environment:
    DB_HOST: db  # ← Correcto para Docker network interna
```

**Pero en Coolify/Hostinger:** Es posible que las variables de entorno no estén siendo inyectadas correctamente al contenedor.

### 🟡 Seguridad: Secrets hardcoded

| Variable | Ubicación | Riesgo |
|----------|-----------|--------|
| `ADMIN_PASSWORD` | `server.py:22` | Cualquiera con acceso al repo ve la contraseña |
| `JWT_SECRET` | `server.py:23` | Tokens falsificables |

### 🟡 Dependencias incompletas

`requirements.txt` solo tiene:
```
fpdf2
```

Falta `pymysql` — sin él, MySQL nunca funciona.

---

## 2. Plan de Acción

### Fase 1: Fix Persistencia de Datos (Hoy — Bloqueante)

**Paso 1.1 — Verificar entorno en producción**

Acceder al servidor (SSH o Coolify panel) y ejecutar:
```bash
# Dentro del contenedor app
docker exec -it carol_app env | grep DB_
docker exec -it carol_app python3 -c "import pymysql; print('OK')"
```

**Resultado esperado:**
- `DB_HOST=db`
- `DB_NAME=carol`
- `pymysql` importa sin error

**Si `DB_HOST` está vacío:**
- Revisar configuración de variables en Coolify
- Verificar que el `.env` se copie al build

**Si `pymysql` no está instalado:**
```bash
# Fix inmediato en el contenedor (temporal)
docker exec -it carol_app pip install pymysql
# Luego rebuild de imagen con fix permanente
```

**Paso 1.2 — Añadir `pymysql` a requirements.txt**

```diff
  fpdf2
+ pymysql
```

**Paso 1.3 — Añadir logging de modo DB**

En `server.py`, después de la detección de `USE_MYSQL`:
```python
print(f"[DB] Mode: {'MySQL' if USE_MYSQL else 'JSON files'} ({DB_HOST or 'no host'})")
```

Esto permitirá ver en los logs de Coolify qué modo está activo.

**Paso 1.4 — Redeploy y verificar**

```bash
git add requirements.txt server.py
git commit -m "fix(db): add pymysql dependency + DB mode logging"
git push origin main
# Trigger redeploy en Coolify
```

**Paso 1.5 — Test de persistencia**

1. Registrar un candidato en `/register`
2. Verificar que aparezca en la base de datos:
   ```bash
   docker exec -it carol_db mysql -ucarol -p carol -e "SELECT * FROM candidates;"
   ```
3. Completar una evaluación
4. Verificar tabla `results`

---

### Fase 2: Seguridad (Mañana)

**Paso 2.1 — Mover secrets a variables de entorno**

En `server.py`:
```diff
- ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Yamakasi111")
- JWT_SECRET = os.getenv("JWT_SECRET", "carol-jwt-change-me-in-production")
+ ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
+ JWT_SECRET = os.getenv("JWT_SECRET", "")
+
+ if not ADMIN_PASSWORD or not JWT_SECRET:
+     raise RuntimeError("ADMIN_PASSWORD and JWT_SECRET must be set via environment variables")
```

**Paso 2.2 — Actualizar `.env.example`**

```bash
# MySQL Database
DB_ROOT_PASSWORD=changeme_root
DB_NAME=carol
DB_USER=carol
DB_PASSWORD=changeme_db

# Admin Auth (REQUIRED — no defaults)
ADMIN_PASSWORD=your_secure_password_here
JWT_SECRET=your_random_32_char_string_here

# External port (Coolify/Traefik)
APP_PORT=80
```

**Paso 2.3 — Rotar credenciales en producción**

1. Generar nuevo JWT secret:
   ```bash
   openssl rand -base64 32
   ```
2. Cambiar `ADMIN_PASSWORD`
3. Actualizar variables en Coolify
4. Redeploy

---

### Fase 3: Features — Admin Panel y Validación (Esta semana)

**Paso 3.1 — Endpoint admin `/api/admin/candidates`**

```python
# En server.py, dentro de CarolHandler.do_GET()
elif path == "/api/admin/candidates":
    # Verificar auth (JWT token en header)
    token = self.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = _decode_token(token)
        if payload.get("role") != "admin":
            raise ValueError("Not admin")
    except Exception:
        self._send_json(403, {"error": "Unauthorized"})
        return
    
    candidates = get_candidates()
    self._send_json(200, {"candidates": candidates})
```

**Paso 3.2 — Validación de candidato registrado**

En el flujo de evaluación, antes de mostrar el quiz:
```python
# Verificar si el candidato existe
candidates = get_candidates()
candidate = next((c for c in candidates if c.get("employee_id") == employee_id or c.get("contact_email") == email), None)

if not candidate:
    # Modo cerrado: rechazar
    # Modo abierto: permitir pero solo mostrar resultados al final (no guardar)
    pass
```

**Paso 3.3 — Modo abierto/cerrado (feature flag)**

```python
OPEN_MODE = os.getenv("OPEN_MODE", "false").lower() == "true"

# En el handler de evaluación:
if not OPEN_MODE and not candidate:
    self._send_json(403, {"error": "Candidato no registrado. Contacte a su administrador."})
    return
```

**Paso 3.4 — Generador de reportes PDF**

Usar `fpdf2` (ya en requirements):
```python
from fpdf import FPDF

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "CAROL v3 — Reporte de Evaluación", ln=True)
    
    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(4)

# Endpoint: GET /api/results/{id}/pdf
```

---

### Fase 4: Mobile y UX (Siguiente semana)

**Paso 4.1 — Responsive design**

Revisar `/web` (frontend HTML/CSS):
- Añadir `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Media queries para botones y formularios en móvil
- Test en iPhone SE / Android pequeño

**Paso 4.2 — Admin dashboard UI**

Crear `/web/admin.html`:
- Tabla de candidatos con filtros (nombre, empresa, nivel, fecha)
- Botón "Descargar CSV" de resultados
- Vista de detalle por candidato (modal)

---

## 3. Despliegue y Lanzamiento

### 3.1 Estrategia de deploy

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Local     │ ──► │   Staging   │ ──► │ Production  │
│  (test)     │     │ (carol-stg) │     │(carol.soul23)│
└─────────────┘     └─────────────┘     └─────────────┘
```

**Actual:** Solo producción. Riesgoso para fixes.

**Recomendación:** Crear rama `develop` y deploy de prueba en `carol-stg.soul23.mx`.

### 3.2 Checklist de lanzamiento (go-live)

- [ ] MySQL persistiendo datos correctamente
- [ ] Admin password cambiado (no default)
- [ ] JWT secret rotado
- [ ] HTTPS funcionando (certificado válido)
- [ ] Backup automático de DB configurado
- [ ] Logs de errores enviados a Telegram/email
- [ ] Rate limiting en endpoints públicos
- [ ] PDF generation testeado

### 3.3 Monitoreo post-lanzamiento

| Métrica | Herramienta | Alerta |
|---------|-------------|--------|
| DB connection errors | Coolify logs | > 5 errores/hora |
| Disk usage (JSON fallback) | `df -h` | > 80% |
| Failed logins | Custom log | > 10 intentos/hora |
| Evaluaciones completadas | Query SQL diaria | Reporte automático |

---

## 4. Notas Técnicas

### Estructura de tablas actual

**candidates:**
```sql
id, candidate_id, survey_id, full_name, employee_id, birth_year, birth_month,
department, job_role, years_experience, self_evaluation, company_name,
contact_email, assigned_level, status, registered_at, submitted_at, created_at
```

**results:**
```sql
id, candidate_id, submitted_at, candidate_json, assessment_json, results_json,
category_breakdown_json, wrong_question_ids_json, stored_at, created_at
```

### Endpoints actuales

| Método | Path | Descripción |
|--------|------|-------------|
| POST | `/webhook/carol-registration` | Registro de candidato |
| POST | `/webhook/carol-assessment` | Envío de evaluación |
| GET | `/api/candidates` | Lista candidatos (JSON) |
| GET | `/api/results` | Lista resultados (JSON) |
| GET | `/api/results/{id}` | Detalle de resultado |
| GET | `/api/results/{id}/csv` | Export CSV individual |

### Endpoints necesarios (nuevos)

| Método | Path | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/admin/candidates` | Lista completa admin | JWT admin |
| GET | `/api/admin/results` | Lista resultados admin | JWT admin |
| GET | `/api/results/{id}/pdf` | Reporte PDF | JWT admin |
| POST | `/api/admin/auth` | Login admin | — |

---

## 5. Próximos pasos inmediatos

1. **Verificar variables de entorno** en Coolify (¿`DB_HOST` está seteado?)
2. **Añadir `pymysql`** a `requirements.txt`
3. **Hacer commit/push** del fix
4. **Testear registro** en producción
5. **Confirmar persistencia** con query directa a MySQL

---

*Plan creado por Talia (Staff of Soul 23) usando GitHub CLI skill.*  
*Para actualizar: editar este archivo, commit, push.*
