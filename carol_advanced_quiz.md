# CAROL — Evaluación Avanzado — Ingenieros y Líderes
**Sistema:** CAROL Assessment System v2  
**Desarrollado por:** M. Gallegos / F. Salazar

---

## ℹ️ Información General

| Campo | Valor |
|-------|-------|
| Total preguntas | **43** |
| Puntaje máximo | **52.5 pts** |
| Tiempo estimado | **75 minutos** |
| Puntaje mínimo aprobatorio | **80% (42 pts mín.)** |
| Preguntas Teóricas (1 pt c/u) | **24** |
| Preguntas Prácticas (1.5 pts c/u) | **19** |

## 📊 Distribución por Área de Conocimiento

| Área | Preguntas | Pts Teórico | Pts Práctico | Pts Máx |
|------|-----------|-------------|--------------|---------|
| 🔵 Máquina e Inyectora | 6 | 3×1pt=3 | 3×1.5pt=4.5 | **7.0** |
| 🟢 Proceso de Inyección | 7 | 3×1pt=3 | 4×1.5pt=6.0 | **9.0** |
| 🟡 Calidad y Defectos | 5 | 2×1pt=2 | 3×1.5pt=4.5 | **6.5** |
| 🔴 Seguridad Industrial | 5 | 3×1pt=3 | 2×1.5pt=3.0 | **6.5** |
| 🟣 Materiales Plásticos | 5 | 5×1pt=5 | 0×1.5pt=0.0 | **5.0** |
| 🔷 Eficiencia y Lean | 5 | 2×1pt=2 | 3×1.5pt=4.5 | **6.5** |
| 🟤 Desperdicios (Muda) | 5 | 3×1pt=3 | 2×1.5pt=3.0 | **6.0** |
| 🔶 Ingeniería de Moldes | 5 | 3×1pt=3 | 2×1.5pt=3.0 | **6.0** |
| **TOTAL** | **43** | **24** | **19** | **52.5** |

## 🎯 Criterios de Evaluación

- ✅ **Aprobado:** ≥80% del puntaje máximo (42+ pts)
- ❌ **No Aprobado:** <80% — Se requiere plan de capacitación antes de re-evaluación

## ⚖️ Ponderación de Reactivos

- **Teórico (1.0 pt):** Conocimiento conceptual y técnico
- **Práctico (1.5 pts):** Diagnóstico de fallas, cálculos, toma de decisiones en escenario real

## 📝 Banco de Preguntas

### 🔵 Máquina e Inyectora (6 preguntas)

---

**ID:** `mach_1` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La presión hidráulica se multiplica en la punta del husillo debido a la Ley de Pascal y la diferencia de áreas.

**Con un ratio de intensificación de 10:1 y 1,500 PSI en el manómetro hidráulico, calcula la presión específica sobre el plástico:**

- ○ **a)** 1,500 PSI (Relación directa 1:1)
- ○ **b)** 150 PSI (Reducción por fricción del husillo)
- ✅ **c)** 15,000 PSI (Multiplicación por área)
- ○ **d)** 16,500 PSI (Suma de presión absoluta + relativa)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** 15,000 PSI (Multiplicación por área)

**Razonamiento:** La presión específica es el resultado de la presión hidráulica multiplicada por el ratio de área entre el pistón y el husillo (1500 * 10).
</details>

---

**ID:** `mach_2` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El oxígeno a altas temperaturas reacciona rápidamente con polímeros orgánicos.

**¿Cuál es la consecuencia físico-química de una descompresión (suck-back) excesiva en resinas sensibles como el Nylon?**

- ○ **a)** Cristalización inducida por choque térmico en la boquilla
- ✅ **b)** Oxidación y degradación por entrada de aire al barril
- ○ **c)** Aumento exponencial de la viscosidad intrínseca
- ○ **d)** Generación de vacío absoluto en la cavidad del molde

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Oxidación y degradación por entrada de aire al barril

**Razonamiento:** El retroceso excesivo aspira oxígeno atmosférico hacia la cámara caliente, provocando oxidación inmediata y manchas (splay).
</details>

---

**ID:** `mach_3` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La consistencia del cojín es el mejor indicador de la repetibilidad volumétrica del proceso.

**Una variación del cojín (cushion) superior a +/- 10% ciclo a ciclo es un indicador primario de:**

- ○ **a)** Desviación en el algoritmo PID de temperatura de zonas
- ✅ **b)** Fuga en la válvula check (anillo) o desgaste del barril
- ○ **c)** Variación en la velocidad de apertura de la rodillera
- ○ **d)** Fluctuación turbulenta en la presión de la red de agua

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Fuga en la válvula check (anillo) o desgaste del barril

**Razonamiento:** La inestabilidad del cojín implica que el volumen de material delante del tornillo no se mantiene, fugándose hacia atrás durante la inyección.
</details>

---

**ID:** `mach_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La velocidad de procesamiento de la CPU de la máquina influye en la precisión milimétrica.

**El 'Scan Time' o tiempo de respuesta del controlador de la máquina afecta críticamente a:**

- ○ **a)** La eficiencia energética del motor eléctrico principal
- ✅ **b)** La repetibilidad del punto de transferencia (VPT)
- ○ **c)** La capacidad máxima de tonelaje de cierre
- ○ **d)** La temperatura operativa del aceite hidráulico

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La repetibilidad del punto de transferencia (VPT)

**Razonamiento:** Un escaneo lento provoca que la máquina reaccione tarde al alcanzar la posición de corte, variando el volumen inyectado.
</details>

---

**ID:** `mach_5` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La geometría del husillo determina la calidad de la homogeneización térmica.

**Comparando un husillo L/D 24:1 contra uno 18:1, la principal ventaja técnica del 24:1 es:**

- ○ **a)** Mayor capacidad de transmisión de presión hidráulica
- ✅ **b)** Mejor calidad de mezclado y homogeneidad térmica
- ○ **c)** Menor tiempo de residencia del material en el barril
- ○ **d)** Reducción significativa del torque requerido para girar

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Mejor calidad de mezclado y homogeneidad térmica

**Razonamiento:** Mayor longitud permite zonas de transición más suaves y mejor distribución de calor, resultando en un fundido (melt) más uniforme.
</details>

---

**ID:** `mach_6` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La contrapresión genera calor por fricción, pero también estrés mecánico.

**Además de aumentar la temperatura de la masa, ¿qué efecto mecánico negativo tiene la contrapresión excesiva?**

- ✅ **a)** Desgaste acelerado en la punta del husillo y barril
- ○ **b)** Reducción de la fuerza de cierre disponible en la prensa
- ○ **c)** Fugas de aceite en el sistema de expulsión hidráulico
- ○ **d)** Deformación elástica permanente de las barras (tie-bars)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Desgaste acelerado en la punta del husillo y barril

**Razonamiento:** Aumenta la carga axial y la fricción del tornillo contra la pared del barril y el material, acelerando la abrasión.
</details>

### 🟢 Proceso de Inyección (7 preguntas)

---

**ID:** `proc_1` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La reología de polímeros estudia cómo fluye la materia bajo fuerzas aplicadas.

**En la curva de viscosidad, la región 'Newtonian Flat' (Meseta Newtoniana) se caracteriza porque:**

- ○ **a)** La viscosidad cae drásticamente con la velocidad de corte
- ✅ **b)** La viscosidad es estable independientemente del corte (shear)
- ○ **c)** El material comienza a degradarse térmicamente por fricción
- ○ **d)** La presión de inyección requerida es cercana a cero

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La viscosidad es estable independientemente del corte (shear)

**Razonamiento:** Es la zona de baja cizalla donde el polímero se comporta como un fluido newtoniano antes de empezar a adelgazar (shear thinning).
</details>

---

**ID:** `proc_2` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Operar al límite de la capacidad de presión elimina la capacidad de control del proceso.

**El objetivo de un estudio de 'Caída de Presión' (Pressure Drop) es asegurar que:**

- ✅ **a)** La máquina tenga ~10% de presión hidráulica de reserva
- ○ **b)** El molde soporte la fuerza de cierre máxima sin abrirse
- ○ **c)** El tiempo de ciclo sea lo más corto físicamente posible
- ○ **d)** La temperatura del agua mantenga un flujo turbulento

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La máquina tenga ~10% de presión hidráulica de reserva

**Razonamiento:** Si la máquina usa el 100% de su presión para llenar, pierde control sobre la velocidad (Process Limited). Se requiere un margen de seguridad.
</details>

---

**ID:** `proc_3` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El área bajo la curva de presión refleja la energía consumida para llenar el molde.

**Un aumento repentino en la integral de presión o 'Trabajo de Inyección' sugiere:**

- ○ **a)** Una fuga interna en la válvula check o anillo
- ✅ **b)** Aumento de viscosidad por material frío u obstrucción
- ○ **c)** Disminución drástica de la fuerza de cierre real
- ○ **d)** Aumento inusual en la temperatura de las resistencias

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Aumento de viscosidad por material frío u obstrucción

**Razonamiento:** Más trabajo para llegar a la misma posición indica mayor resistencia al flujo (viscosidad alta o canal bloqueado).
</details>

---

**ID:** `proc_4` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Determinar cuándo se corta físicamente la conexión entre la pieza y el sistema de alimentación.

**El criterio técnico definitivo para confirmar el 'Sellado de Compuerta' (Gate Freeze) es:**

- ✅ **a)** Estabilización del peso de la pieza vs tiempo de hold
- ○ **b)** Enfriamiento de la colada a temperatura ambiente
- ○ **c)** Finalización del tiempo de dosificación del husillo
- ○ **d)** Ausencia total de rechupados en la superficie

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Estabilización del peso de la pieza vs tiempo de hold

**Razonamiento:** Se grafica peso vs tiempo. Cuando el peso deja de subir, la compuerta se ha cerrado físicamente y ya no entra material.
</details>

---

**ID:** `proc_5` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La fricción molecular a altas velocidades se convierte en energía térmica.

**Debido al calentamiento por cizalla (Shear Heating), aumentar la velocidad de inyección provoca:**

- ○ **a)** Enfriamiento adiabático del frente de flujo por expansión
- ✅ **b)** Aumento real de la temperatura de la masa fundida
- ○ **c)** Aumento de la densidad del material por compactación
- ○ **d)** Reducción inmediata del índice de fluidez (MFI)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Aumento real de la temperatura de la masa fundida

**Razonamiento:** La fricción molecular a alta velocidad genera calor interno, reduciendo la viscosidad efectiva.
</details>

---

**ID:** `proc_6` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La consistencia del proceso depende de cómo se controla el volumen inyectado.

**¿Por qué se prefiere el VPT (Transferencia) por Posición en lugar de por Tiempo o Presión?**

- ○ **a)** Porque es más fácil de programar en el controlador
- ✅ **b)** Porque garantiza un volumen de disparo consistente
- ○ **c)** Porque protege el molde de picos de sobrepresión
- ○ **d)** Porque reduce el consumo energético del motor

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Porque garantiza un volumen de disparo consistente

**Razonamiento:** La posición correlaciona directamente con el volumen desplazado. El tiempo varía si cambia la viscosidad, causando inestabilidad.
</details>

---

**ID:** `spec_6` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La presión efectiva sobre la pieza depende de la reserva de material.

**¿Por qué el monitoreo del 'Cojín' es más crítico que el 'Tiempo de Inyección' para la consistencia dimensional?**

- ✅ **a)** Porque confirma que hubo material suficiente para transferir la presión
- ○ **b)** Porque es un parámetro más fácil de visualizar en la pantalla
- ○ **c)** Porque el tiempo de inyección nunca varía en máquinas modernas
- ○ **d)** Porque el cojín determina la velocidad de enfriamiento de la pieza

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Porque confirma que hubo material suficiente para transferir la presión

**Razonamiento:** Si no hay cojín, no hay presión hidráulica sobre la pieza (presión efectiva = 0), causando rechupados y medidas cortas.
</details>

### 🟡 Calidad y Defectos (5 preguntas)

---

**ID:** `qual_1` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El flujo laminar es deseable para evitar marcas superficiales en la pieza.

**La solución técnica para eliminar el 'Jetting' (gusanito) es:**

- ○ **a)** Aumentar drásticamente la temperatura de boquilla y molde
- ✅ **b)** Perfilar la velocidad (lento al inicio) para crear flujo laminar
- ○ **c)** Aumentar la contrapresión al máximo posible
- ○ **d)** Reducir el tiempo de enfriamiento para congelar el flujo

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Perfilar la velocidad (lento al inicio) para crear flujo laminar

**Razonamiento:** Entrar lento permite que el material toque las paredes y se expanda progresivamente (Fountain Flow) en lugar de dispararse.
</details>

---

**ID:** `qual_2` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La estructura molecular de los semicristalinos depende del tiempo que tienen para ordenarse.

**En polímeros semicristalinos, ¿qué factor determina el grado de cristalinidad y la contracción final?**

- ○ **a)** La presión de inyección máxima alcanzada
- ✅ **b)** La tasa de enfriamiento (Temperatura de molde)
- ○ **c)** La velocidad de rotación del husillo en la carga
- ○ **d)** El porcentaje de carga de fibra de vidrio añadido

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La tasa de enfriamiento (Temperatura de molde)

**Razonamiento:** Un enfriamiento lento (molde caliente) permite a las moléculas ordenarse en cristales, aumentando la densidad y contracción.
</details>

---

**ID:** `qual_3` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Los índices de capacidad estadística predicen la tasa de rechazo a largo plazo.

**Un Cpk de 0.8 en una dimensión crítica indica estadísticamente que:**

- ○ **a)** El proceso es capaz y está perfectamente centrado
- ✅ **b)** El proceso no es capaz; alta probabilidad de defectos
- ○ **c)** El instrumento de medición requiere calibración urgente
- ○ **d)** La varianza del proceso es menor a la tolerancia permitida

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El proceso no es capaz; alta probabilidad de defectos

**Razonamiento:** Cpk < 1.33 se considera no capaz. La curva de distribución del proceso excede los límites de especificación.
</details>

---

**ID:** `qual_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La fusión de frentes de flujo requiere energía térmica para entrelazar las cadenas moleculares.

**Una línea de soldadura (Weld Line) se convierte en una falla estructural crítica si:**

- ○ **a)** Es visible a simple vista bajo luz normal
- ✅ **b)** La temperatura del frente de flujo es inferior a la Tg al unirse
- ○ **c)** Se encuentra ubicada en una zona estética clase A
- ○ **d)** El molde tiene una textura superficial muy rugosa

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La temperatura del frente de flujo es inferior a la Tg al unirse

**Razonamiento:** Si el material está demasiado frío, no hay entrelazamiento molecular (difusión) entre los frentes, creando una grieta potencial.
</details>

---

**ID:** `qual_5` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* En zonas ciegas donde no es posible mecanizar un venteo tradicional, se requieren materiales especiales.

**Para prevenir el 'Efecto Diesel' en una costilla ciega (blind rib) donde no hay salida de aire, la solución de ingeniería es:**

- ○ **a)** Aumentar la velocidad de inyección para llenar rápido
- ✅ **b)** Uso de insertos de acero poroso sinterizado
- ○ **c)** Bajar la temperatura del molde drásticamente
- ○ **d)** Aplicar vacío general a toda la máquina

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Uso de insertos de acero poroso sinterizado

**Razonamiento:** El acero poroso permite que el gas escape a través de la estructura del metal mientras retiene el plástico.
</details>

### 🔴 Seguridad Industrial (5 preguntas)

---

**ID:** `safe_1` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Ciertos materiales liberan gases altamente peligrosos al descomponerse.

**Al purgar POM (Acetal) degradado, el riesgo químico específico es:**

- ✅ **a)** Liberación de gas Formaldehído (tóxico/irritante)
- ○ **b)** Formación de ácido clorhídrico altamente corrosivo
- ○ **c)** Generación de monóxido de carbono inodoro
- ○ **d)** Explosión por partículas de polvo en suspensión

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Liberación de gas Formaldehído (tóxico/irritante)

**Razonamiento:** El POM se descompone en formaldehído, que ataca ojos y vías respiratorias severamente. Requiere ventilación.
</details>

---

**ID:** `safe_2` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La seguridad moderna requiere validación activa, no solo colocar un candado.

**En un procedimiento LOTO avanzado, después de colocar el candado, ¿cuál es el paso final de verificación?**

- ○ **a)** Firmar la bitácora de mantenimiento en la oficina
- ✅ **b)** Intentar arrancar el equipo para confirmar 'Energía Cero'
- ○ **c)** Avisar verbalmente al gerente de planta
- ○ **d)** Tomar una fotografía del candado colocado

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Intentar arrancar el equipo para confirmar 'Energía Cero'

**Razonamiento:** El paso crítico de 'Try-out' o prueba de arranque confirma que el bloqueo fue efectivo y no hay energía residual.
</details>

---

**ID:** `safe_3` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La energía hidráulica puede almacenarse incluso sin energía eléctrica.

**El peligro latente de un acumulador hidráulico, incluso con la máquina apagada, es:**

- ○ **a)** Alta temperatura residual en las líneas
- ✅ **b)** Energía de presión almacenada lista para liberarse
- ○ **c)** Generación de campos magnéticos permanentes
- ○ **d)** Fugas de gas nitrógeno que causan asfixia

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Energía de presión almacenada lista para liberarse

**Razonamiento:** El acumulador mantiene aceite a presión. Si se desconecta una manguera sin drenarlo, puede causar inyección de fluido letal.
</details>

---

**ID:** `safe_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El uso de agua en incendios eléctricos es fatal; se requieren agentes limpios.

**Extintor correcto para fuego en tableros electrónicos (Clase C):**

- ○ **a)** Agua a presión (Tipo A) con aditivo penetrante
- ✅ **b)** Dióxido de Carbono (CO2) o Agente Limpio
- ○ **c)** Espuma formadora de película acuosa (AFFF)
- ○ **d)** Polvo especial para metales combustibles (Tipo D)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Dióxido de Carbono (CO2) o Agente Limpio

**Razonamiento:** Agentes no conductores y que no dejen residuo corrosivo son esenciales para equipo electrónico.
</details>

---

**ID:** `safe_5` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La integración de robots requiere protocolos de comunicación de seguridad estandarizados.

**Según la norma Euromap 67, ¿cuál es la función de los canales de seguridad redundantes (doble canal)?**

- ○ **a)** Aumentar la velocidad de transmisión de datos al robot
- ✅ **b)** Asegurar que si un canal falla, el otro detenga la máquina
- ○ **c)** Permitir el control remoto inalámbrico desde la oficina
- ○ **d)** Reducir la cantidad de cableado en la instalación

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Asegurar que si un canal falla, el otro detenga la máquina

**Razonamiento:** La redundancia es clave en seguridad (Categoría 3/4); el sistema debe detectar fallos en su propia supervisión.
</details>

### 🟣 Materiales Plásticos (5 preguntas)

---

**ID:** `mat_1` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El corte de las cadenas poliméricas cambia radicalmente la reología del material.

**La degradación por escisión de cadenas (Chain Scission) resulta en:**

- ○ **a)** Aumento de peso molecular y viscosidad
- ✅ **b)** Reducción de peso molecular, viscosidad y propiedades
- ○ **c)** Mejora significativa en la resistencia al impacto
- ○ **d)** Reticulación (cross-linking) de la estructura molecular

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Reducción de peso molecular, viscosidad y propiedades

**Razonamiento:** Al romperse las cadenas largas, el material se vuelve más líquido (fluye más) pero pierde su fuerza estructural.
</details>

---

**ID:** `mat_2` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El agua actúa como un agente reactivo que destruye el polímero a nivel molecular.

**La hidrólisis en materiales como PC o PBT es una reacción química donde el agua:**

- ○ **a)** Actúa como un lubricante externo temporal
- ✅ **b)** Rompe los enlaces covalentes de la cadena polimérica
- ○ **c)** Se evapora rápidamente sin afectar la estructura
- ○ **d)** Genera únicamente burbujas superficiales cosméticas

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Rompe los enlaces covalentes de la cadena polimérica

**Razonamiento:** Es una degradación química irreversible a nivel molecular, no solo un defecto cosmético.
</details>

---

**ID:** `mat_3` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El cambio de fase de sólido a líquido requiere más energía en materiales ordenados.

**Diferencia térmica clave: Los semicristalinos poseen Calor Latente de Fusión, lo que implica:**

- ○ **a)** Requieren menos energía térmica debido a su estructura
- ✅ **b)** Requieren mucha más energía para fundir y enfriar que los amorfos
- ○ **c)** Se enfrían instantáneamente al tocar el molde
- ○ **d)** No tienen temperatura de fusión (Tm) definida

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Requieren mucha más energía para fundir y enfriar que los amorfos

**Razonamiento:** Se necesita energía extra para romper la estructura cristalina al fundir, y hay que extraer esa energía al enfriar.
</details>

---

**ID:** `mat_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Las pruebas de laboratorio estáticas no siempre reflejan la realidad dinámica de la inyección.

**¿Por qué el MFI no es representativo del comportamiento dentro del molde?**

- ○ **a)** Porque se mide a una temperatura demasiado baja
- ✅ **b)** Porque es una prueba de bajo cizallamiento (Low Shear)
- ○ **c)** Porque usa un peso estándar no calibrado
- ○ **d)** Porque el material utilizado suele estar contaminado

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Porque es una prueba de bajo cizallamiento (Low Shear)

**Razonamiento:** La inyección es un proceso de ALTO cizallamiento. El MFI mide flujo casi estático, ignorando el adelgazamiento por corte.
</details>

---

**ID:** `mat_5` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El comportamiento pvT (Presión-Volumen-Temperatura) es fundamental para predecir dimensiones.

**En un diagrama pvT, ¿qué representa la 'rodilla' o cambio brusco de pendiente en la curva de enfriamiento isobárico?**

- ○ **a)** El punto crítico de degradación térmica del polímero
- ✅ **b)** La temperatura de transición vítrea (Tg) o cristalización
- ○ **c)** El momento exacto en que se abre el molde
- ○ **d)** La presión máxima alcanzada por la máquina

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La temperatura de transición vítrea (Tg) o cristalización

**Razonamiento:** Es el punto donde el material cambia de estado (fase), alterando drásticamente su volumen específico.
</details>

### 🔷 Eficiencia y Lean (5 preguntas)

---

**ID:** `eff_1` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La termodinámica impone límites físicos a la velocidad de producción.

**El factor limitante físico (Cuello de botella) más común para reducir el tiempo de ciclo es:**

- ○ **a)** La velocidad de inyección máxima de la máquina
- ✅ **b)** La conductividad térmica del plástico (Tiempo de enfriamiento)
- ○ **c)** La velocidad de los movimientos mecánicos del molde
- ○ **d)** El tiempo de reacción del robot de extracción

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La conductividad térmica del plástico (Tiempo de enfriamiento)

**Razonamiento:** El plástico es un aislante térmico. Extraer el calor del centro de la pared es el proceso más lento por física pura.
</details>

---

**ID:** `eff_2` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Distinguir entre tareas que detienen la máquina y las que no es la base del SMED.

**En SMED, un ejemplo de actividad INTERNA es:**

- ○ **a)** Precalentar el molde en un banco externo de pruebas
- ✅ **b)** Asegurar el molde a la platina (Clamping)
- ○ **c)** Buscar las llaves y herramientas necesarias
- ○ **d)** Organizar las mangueras de agua antes del cambio

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Asegurar el molde a la platina (Clamping)

**Razonamiento:** Actividad Interna = Máquina detenida forzosamente. No puedes atornillar el molde si la máquina está produciendo.
</details>

---

**ID:** `eff_3` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El cálculo del OEE revela dónde se pierden las oportunidades de producción.

**Si tu OEE es 60% pero la Calidad es 99% y la Disponibilidad 98%, el problema está en:**

- ✅ **a)** Desempeño (Performance) - Ciclos lentos o micro-paros
- ○ **b)** Calidad - Piezas defectuosas ocultas en el proceso
- ○ **c)** Disponibilidad - Tiempos muertos largos no reportados
- ○ **d)** Planeación - Falta de órdenes de producción

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Desempeño (Performance) - Ciclos lentos o micro-paros

**Razonamiento:** Matemáticamente: Si AxQ son altos, P debe ser muy bajo para arrastrar el promedio a 60%.
</details>

---

**ID:** `eff_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La confiabilidad del equipo se mide por la frecuencia de sus averías.

**El MTBF (Mean Time Between Failures) mide:**

- ○ **a)** La velocidad promedio de reparación del equipo
- ✅ **b)** La confiabilidad y frecuencia de fallas del equipo
- ○ **c)** El tiempo total de vida útil de la máquina
- ○ **d)** La eficiencia promedio del operador de turno

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La confiabilidad y frecuencia de fallas del equipo

**Razonamiento:** Indica qué tan seguido se rompe la máquina. Clave para programar mantenimiento preventivo.
</details>

---

**ID:** `eff_5` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Los costos de mala calidad van mucho más allá del material tirado.

**El Costo Real de la 'No Calidad' incluye:**

- ○ **a)** Únicamente el valor de la resina desperdiciada
- ✅ **b)** Material + Energía + Mano de obra + Costo de oportunidad + Riesgo cliente
- ○ **c)** El salario del departamento de calidad + Auditorías
- ○ **d)** El costo de la disposición de basura + Fletes

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Material + Energía + Mano de obra + Costo de oportunidad + Riesgo cliente

**Razonamiento:** Producir basura cuesta lo mismo o más que producir piezas buenas, más el lucro cesante.
</details>

### 🟤 Desperdicios (Muda) (5 preguntas)

---

**ID:** `wast_1` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Agregar valor es lo único por lo que el cliente paga; el resto es desperdicio.

**El sobre-empaque (overpacking) que causa piezas pesadas y estrés interno es un desperdicio de tipo:**

- ○ **a)** Transporte y Movimiento innecesario
- ✅ **b)** Sobre-procesamiento y Material
- ○ **c)** Espera e Inventario acumulado
- ○ **d)** Talento Humano subutilizado

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Sobre-procesamiento y Material

**Razonamiento:** Usas más material del necesario y aplicas más presión (proceso) de la requerida, agregando costo sin valor.
</details>

---

**ID:** `wast_2` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El inventario excesivo actúa como un amortiguador que esconde problemas operativos.

**El exceso de inventario (WIP o Terminado) es negativo porque:**

- ✅ **a)** Oculta ineficiencias del sistema y atrapa flujo de efectivo
- ○ **b)** Mejora la respuesta ante variaciones de demanda imprevistas
- ○ **c)** Asegura que los operadores siempre tengan trabajo disponible
- ○ **d)** Aumenta el valor de los activos circulantes de la empresa

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Oculta ineficiencias del sistema y atrapa flujo de efectivo

**Razonamiento:** Es la analogía del 'río y las rocas'. El nivel alto de agua (inventario) tapa los problemas (rocas) del fondo.
</details>

---

**ID:** `wast_3` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La falta de mantenimiento preventivo en moldes genera tiempos muertos reactivos.

**Un mantenimiento deficiente de venteos genera desperdicio principalmente por:**

- ○ **a)** Aumento en el consumo de energía eléctrica del motor
- ✅ **b)** Paros no programados para limpieza y scrap por quemaduras
- ○ **c)** Desgaste prematuro del aceite hidráulico por calor
- ○ **d)** Reducción significativa de la fuerza de cierre

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Paros no programados para limpieza y scrap por quemaduras

**Razonamiento:** Los venteos sucios obligan a detener la producción para limpiar (Disponibilidad) y generan defectos (Calidad).
</details>

---

**ID:** `wast_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El diseño del sistema de alimentación impacta la eficiencia del material.

**Técnicamente, usar Colada Fría en lugar de Colada Caliente implica:**

- ○ **a)** Mayor eficiencia energética del sistema
- ✅ **b)** Generación intrínseca de desperdicio (scrap/regrind) en cada ciclo
- ○ **c)** Mejor control de la temperatura de masa fundida
- ○ **d)** Menor tiempo de ciclo total de enfriamiento

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Generación intrínseca de desperdicio (scrap/regrind) en cada ciclo

**Razonamiento:** La colada fría es material que se calienta y enfría solo para ser tirado o re-molido, lo cual es ineficiente termodinámicamente.
</details>

---

**ID:** `wast_5` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La eficiencia energética es un indicador clave de sostenibilidad y costo.

**¿Qué métrica se utiliza comúnmente para comparar la eficiencia energética entre diferentes máquinas de inyección?**

- ○ **a)** Caballos de fuerza (HP) del motor principal
- ✅ **b)** Consumo Específico de Energía (kWh/kg de material procesado)
- ○ **c)** Amperaje máximo del tablero de control
- ○ **d)** Voltaje de alimentación trifásico (220V vs 440V)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Consumo Específico de Energía (kWh/kg de material procesado)

**Razonamiento:** El kWh/kg normaliza el consumo respecto a la producción, permitiendo comparar máquinas grandes y pequeñas.
</details>

### 🔶 Ingeniería de Moldes (5 preguntas)

---

**ID:** `spec_1` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La dinámica de fluidos dicta la eficiencia de la transferencia de calor.

**En refrigeración de moldes, un Número de Reynolds > 4,000 garantiza:**

- ○ **a)** Flujo Laminar (Estabilidad de presión sin turbulencia)
- ✅ **b)** Flujo Turbulento (Máxima eficiencia de transferencia de calor)
- ○ **c)** Presión excesiva que puede dañar las mangueras
- ○ **d)** Ausencia total de corrosión galvánica en los canales

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Flujo Turbulento (Máxima eficiencia de transferencia de calor)

**Razonamiento:** La turbulencia rompe la capa límite aislante del agua contra el metal, extrayendo calor mucho más rápido.
</details>

---

**ID:** `spec_2` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La rigidez de la máquina interactúa con la estructura del molde.

**La 'Deflexión de Platinas' causa rebaba central aunque el tonelaje sea correcto debido a:**

- ✅ **a)** Deformación elástica de la platina que abre el molde en el centro
- ○ **b)** Expansión térmica incontrolada de las placas del molde
- ○ **c)** Compresión plástica excesiva del acero del molde
- ○ **d)** Falta de paralelismo severo en las guías de las barras

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Deformación elástica de la platina que abre el molde en el centro

**Razonamiento:** Si el molde es pequeño, la platina se 'dobla' alrededor de él como una hoja de papel, perdiendo presión de sello en el centro.
</details>

---

**ID:** `spec_3` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La simulación predictiva ahorra costos al identificar errores antes de cortar acero.

**¿En qué etapa es más rentable utilizar simulación CAE (Moldflow)?**

- ○ **a)** Durante la producción masiva para corregir fallas
- ✅ **b)** En la fase de diseño de pieza y molde
- ○ **c)** Después de fabricar el molde para validarlo
- ○ **d)** Al cotizar el precio final de la resina

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** En la fase de diseño de pieza y molde

**Razonamiento:** El costo de corregir un error en diseño es despreciable comparado con modificar acero endurecido.
</details>

---

**ID:** `spec_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Los sistemas de colada caliente avanzados permiten control secuencial.

**La ventaja técnica principal de una compuerta valvulada (Valve Gate) es:**

- ○ **a)** Menor costo operativo por eliminación de canales fríos
- ✅ **b)** Control independiente del flujo y mejor acabado cosmético
- ○ **c)** Eliminación total del sistema de enfriamiento del molde
- ○ **d)** Reducción significativa de la fuerza de cierre requerida

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Control independiente del flujo y mejor acabado cosmético

**Razonamiento:** Permite abrir/cerrar la entrada a voluntad (secuenciado) y deja una marca casi invisible en la pieza.
</details>

---

**ID:** `spec_5` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La geometría de la pieza afecta la disipación de calor.

**El 'Efecto de Esquina' (Corner Effect) en refrigeración provoca puntos calientes porque:**

- ○ **a)** El agua fluye mucho más lento en las esquinas agudas
- ✅ **b)** Hay mayor masa de plástico transfiriendo calor a menor área de acero
- ○ **c)** El acero es estructuralmente más delgado en las esquinas
- ○ **d)** La fricción del flujo genera calor adicional en los bordes

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Hay mayor masa de plástico transfiriendo calor a menor área de acero

**Razonamiento:** Geometría básica: El calor converge desde dos lados hacia una esquina interna que tiene poca superficie para disiparlo.
</details>
