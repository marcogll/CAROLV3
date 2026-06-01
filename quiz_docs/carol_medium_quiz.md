# CAROL — Evaluación Medio — Técnicos de Proceso
**Sistema:** CAROL Assessment System v2  
**Desarrollado por:** M. Gallegos / F. Salazar

---

## ℹ️ Información General

| Campo | Valor |
|-------|-------|
| Total preguntas | **60** |
| Puntaje máximo | **76.0 pts** |
| Tiempo estimado | **60 minutos** |
| Puntaje mínimo aprobatorio | **75% (57 pts mín.)** |
| Preguntas Teóricas (1 pt c/u) | **28** |
| Preguntas Prácticas (1.5 pts c/u) | **32** |

## 📊 Distribución por Área de Conocimiento

| Área | Preguntas | Pts Teórico | Pts Práctico | Pts Máx |
|------|-----------|-------------|--------------|---------|
| 🔵 Máquina e Inyectora | 9 | 4×1pt=4 | 5×1.5pt=7.5 | **11.5** |
| 🟢 Proceso de Inyección | 9 | 5×1pt=5 | 4×1.5pt=6.0 | **11.0** |
| 🟡 Calidad y Defectos | 9 | 2×1pt=2 | 7×1.5pt=10.5 | **12.5** |
| 🔴 Seguridad Industrial | 9 | 2×1pt=2 | 7×1.5pt=10.5 | **12.0** |
| 🟣 Materiales Plásticos | 8 | 6×1pt=6 | 2×1.5pt=3.0 | **9.0** |
| 🔷 Eficiencia y Lean | 8 | 5×1pt=5 | 3×1.5pt=4.5 | **10.0** |
| 🟤 Desperdicios (Muda) | 8 | 4×1pt=4 | 4×1.5pt=6.0 | **10.0** |
| **TOTAL** | **60** | **28** | **32** | **76.0** |

## 🎯 Criterios de Evaluación

- ✅ **Aprobado:** ≥75% del puntaje máximo (57+ pts)
- ❌ **No Aprobado:** <75% — Se requiere plan de capacitación antes de re-evaluación

## ⚖️ Ponderación de Reactivos

- **Teórico (1.0 pt):** Conocimiento conceptual y técnico
- **Práctico (1.5 pts):** Diagnóstico de fallas, cálculos, toma de decisiones en escenario real

## 📝 Banco de Preguntas

### 🔵 Máquina e Inyectora (9 preguntas)

---

**ID:** `mach_1` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Los sensores de temperatura son los ojos del sistema de control.

**¿Qué variable física mide realmente un termopar insertado en una zona del barril de plastificación?**

- ○ **a)** La temperatura del núcleo de la masa de plástico fundido
- ✅ **b)** La temperatura del acero del barril en ese punto específico
- ○ **c)** La temperatura superficial de la resistencia calefactora
- ○ **d)** La temperatura generada por la fricción de cizalla del husillo

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La temperatura del acero del barril en ese punto específico

**Razonamiento:** El termopar toca el metal del barril. La temperatura del plástico es una consecuencia, pero no es lo que el sensor mide directamente.
</details>

---

**ID:** `mach_2` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La presión hidráulica no es equivalente a la presión ejercida sobre el polímero.

**Si el manómetro hidráulico marca 1,000 PSI y la máquina tiene un ratio de intensificación de 10:1, ¿cuál es la presión plástica aplicada?**

- ○ **a)** 100 PSI (Reducción por fricción mecánica)
- ○ **b)** 1,000 PSI (Relación directa hidráulica 1:1)
- ✅ **c)** 10,000 PSI (Multiplicación por área del pistón)
- ○ **d)** 11,000 PSI (Suma acumulada de presiones)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** 10,000 PSI (Multiplicación por área del pistón)

**Razonamiento:** La presión sobre el plástico es mayor que la hidráulica debido a la diferencia de áreas entre el pistón hidráulico y la punta del husillo.
</details>

---

**ID:** `mach_3` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La válvula antirretorno es crítica para mantener la presión durante el empaque.

**Durante la fase de sostenimiento, observas que el husillo sigue avanzando lentamente (creeping) sin detenerse. Diagnóstico probable:**

- ○ **a)** La compuerta del molde se congeló prematuramente por enfriamiento
- ✅ **b)** Fuga interna en el anillo de cierre (válvula check)
- ○ **c)** Exceso de contrapresión programada durante la carga
- ○ **d)** El perfil de temperaturas del barril está invertido

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Fuga interna en el anillo de cierre (válvula check)

**Razonamiento:** Si el husillo avanza en 'Hold', significa que el material se está fugando hacia atrás a través del anillo check desgastado.
</details>

---

**ID:** `mach_4` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La geometría del tornillo determina su capacidad para fundir y mezclar.

**¿Qué indica la relación L/D (Longitud/Diámetro) en la especificación de un husillo?**

- ○ **a)** La capacidad máxima de inyección calculada en gramos
- ✅ **b)** La longitud de vuelo del husillo dividida por su diámetro
- ○ **c)** La distancia máxima de apertura permitida de la prensa
- ○ **d)** El ratio de compresión entre zona de alimentación y medición

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La longitud de vuelo del husillo dividida por su diámetro

**Razonamiento:** Es una medida geométrica clave (ej. 20:1) que determina la capacidad de mezclado y plastificación.
</details>

---

**ID:** `mach_5` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La alimentación del material depende de condiciones específicas de fricción y temperatura.

**Si la temperatura en la garganta de alimentación no se controla y sube demasiado, ¿qué problema de proceso se genera?**

- ✅ **a)** Puenteo de material (Bridging) y falla de carga
- ○ **b)** Degradación inmediata del pigmento en la tolva
- ○ **c)** Aumento descontrolado de la presión hidráulica
- ○ **d)** Cristalización prematura del polímero en el husillo

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Puenteo de material (Bridging) y falla de carga

**Razonamiento:** Los pellets se ablandan y se pegan entre sí en la garganta, bloqueando el paso hacia el tornillo.
</details>

---

**ID:** `mach_6` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La unidad de potencia es la encargada de convertir energía eléctrica en energía de fluido.

**En un sistema hidráulico, ¿qué componente es responsable de generar el caudal necesario para el movimiento?**

- ○ **a)** La válvula proporcional de flujo
- ○ **b)** El acumulador de nitrógeno a presión
- ✅ **c)** La bomba hidráulica principal
- ○ **d)** El cilindro de inyección trasero

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La bomba hidráulica principal

**Razonamiento:** La bomba convierte energía mecánica en energía hidráulica (caudal); las válvulas solo lo regulan.
</details>

---

**ID:** `mach_7` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La integridad estructural de la máquina depende de placas de acero específicas.

**Identifica cuál de las siguientes NO es una platina estándar en una inyectora:**

- ○ **a)** Platina Fija (Lado A)
- ○ **b)** Platina Móvil (Lado B)
- ✅ **c)** Platina de Rotación Axial
- ○ **d)** Platina Trasera o de Soporte

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Platina de Rotación Axial

**Razonamiento:** Las platinas estándar son fija, móvil y de soporte. La rotación axial no es un componente estructural estándar.
</details>

---

**ID:** `mach_8` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La compatibilidad entre sensores y controladores es esencial para lecturas precisas.

**¿Qué consecuencia tiene conectar un termopar Tipo J en una tarjeta configurada para Tipo K?**

- ○ **a)** Ninguna, ambos miden la temperatura de la misma forma
- ✅ **b)** Lectura errónea de temperatura y riesgo de proceso
- ○ **c)** Daño permanente e irreversible al PLC de la máquina
- ○ **d)** El calentamiento será mucho más lento pero preciso

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Lectura errónea de temperatura y riesgo de proceso

**Razonamiento:** Las curvas de voltaje/temperatura son diferentes. El controlador leerá una temperatura falsa, pudiendo sobrecalentar o enfriar el sistema.
</details>

---

**ID:** `mach_9` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Los mecanismos del molde deben coordinarse para evitar colisiones internas.

**¿Cuál es la función crítica de los 'Return Pins' (Pernos de retorno) en el molde?**

- ○ **a)** Empujar la pieza fuera del molde al abrir
- ✅ **b)** Retraer la placa de botadores al cerrar el molde
- ○ **c)** Guiar la alineación fina entre cavidad y corazón
- ○ **d)** Soportar la presión de inyección en la placa trasera

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Retraer la placa de botadores al cerrar el molde

**Razonamiento:** Aseguran mecánicamente que los botadores regresen a posición cero antes de inyectar, evitando choques.
</details>

### 🟢 Proceso de Inyección (9 preguntas)

---

**ID:** `proc_10` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La inyección se divide en dos fases de control distintas.

**¿Qué define exactamente el punto de conmutación o transferencia (VPT)?**

- ✅ **a)** El cambio de control de Velocidad a control de Presión
- ○ **b)** El momento exacto en que el molde se llena al 100%
- ○ **c)** El inicio inmediato del tiempo de enfriamiento del ciclo
- ○ **d)** El punto donde se activa la contrapresión del husillo

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El cambio de control de Velocidad a control de Presión

**Razonamiento:** Es la transición crítica donde la máquina deja de empujar por velocidad (llenado) y empieza a empacar por presión.
</details>

---

**ID:** `proc_11` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La maquinaria global requiere manejar diferentes sistemas de unidades.

**Calcula rápidamente: Si tienes 350 Bar, ¿cuál es su equivalente aproximado en PSI? (Factor x14.5)**

- ○ **a)** 2,400 PSI
- ○ **b)** 3,500 PSI
- ✅ **c)** 5,075 PSI
- ○ **d)** 50,000 PSI

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** 5,075 PSI

**Razonamiento:** Cálculo directo: 350 * 14.5 = 5,075. Es vital para operadores que manejan máquinas con diferentes unidades.
</details>

---

**ID:** `proc_12` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El comportamiento del plástico fundido no es lineal como el del agua.

**Debido al comportamiento pseudoplástico (Shear Thinning), ¿qué pasa con la viscosidad al aumentar la velocidad de inyección?**

- ○ **a)** La viscosidad aumenta (se hace más espeso)
- ✅ **b)** La viscosidad disminuye (fluye más fácil)
- ○ **c)** La viscosidad permanece constante (Newtoniano)
- ○ **d)** El material se degrada instantáneamente

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La viscosidad disminuye (fluye más fácil)

**Razonamiento:** Los polímeros adelgazan por cizallamiento; a mayor velocidad, las cadenas se alinean y la resistencia al flujo baja.
</details>

---

**ID:** `proc_13` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Determinar el tiempo correcto de sostenimiento es un proceso científico.

**¿Qué determina un 'Estudio de Sellado de Compuerta' (Gate Freeze Study)?**

- ○ **a)** La temperatura exacta de fusión del material
- ✅ **b)** El tiempo mínimo de sostenimiento para evitar reflujo
- ○ **c)** La presión máxima que soporta el molde sin abrirse
- ○ **d)** El tiempo total de enfriamiento requerido por la pieza

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El tiempo mínimo de sostenimiento para evitar reflujo

**Razonamiento:** Busca el punto en el tiempo donde la entrada se solidifica y el peso de la pieza se estabiliza.
</details>

---

**ID:** `proc_14` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La transferencia efectiva de presión requiere un colchón de material.

**Técnicamente, ¿por qué es grave que el cojín llegue a cero durante el proceso?**

- ○ **a)** Porque el impacto metal-metal daña la punta del husillo
- ✅ **b)** Porque se pierde el control de la presión sobre la cavidad
- ○ **c)** Porque el sistema hidráulico entra en cavitación y pierde potencia
- ○ **d)** Porque aumenta el tiempo de ciclo innecesariamente

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Porque se pierde el control de la presión sobre la cavidad

**Razonamiento:** Si el tornillo toca fondo, la presión hidráulica se transfiere al metal, no al plástico, dejando la pieza 'suelta'.
</details>

---

**ID:** `proc_15` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El plástico reduce su volumen significativamente al enfriarse.

**¿Cuál es la variable de proceso más influyente para controlar la contracción final de la pieza?**

- ○ **a)** La temperatura de la zona de alimentación
- ○ **b)** La velocidad de rotación del husillo
- ✅ **c)** La presión de sostenimiento (Packing pressure)
- ○ **d)** La velocidad de apertura del molde

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** La presión de sostenimiento (Packing pressure)

**Razonamiento:** El empaque introduce material adicional para compensar la reducción de volumen al enfriar.
</details>

---

**ID:** `proc_16` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El control del estado del material fundido al finalizar la dosificación evita problemas en el siguiente ciclo.

**¿Qué defecto en la pieza o problema en el molde se genera por una falta de descompresión (suck-back)?**

- ○ **a)** Tiro corto en la pieza por falta de carga
- ✅ **b)** Hilos o babeo en la boquilla que obstruyen la entrada
- ○ **c)** Quemaduras por efecto diesel en el molde
- ○ **d)** Deformación severa de la pieza al expulsar

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Hilos o babeo en la boquilla que obstruyen la entrada

**Razonamiento:** Sin descompresión, la presión residual hace que el plástico gotee (babeo), creando hilos fríos que bloquean el siguiente disparo.
</details>

---

**ID:** `proc_17` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La compactación del fundido antes de la inyección asegura la consistencia.

**¿Qué defecto esperarías si la contrapresión (Back Pressure) es excesivamente baja?**

- ○ **a)** Rebaba excesiva en la línea de partición
- ✅ **b)** Pobre mezcla, aire atrapado y peso inconsistente
- ○ **c)** Degradación del material por cizallamiento y fricción
- ○ **d)** Dificultad para expulsar la pieza por vacío

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Pobre mezcla, aire atrapado y peso inconsistente

**Razonamiento:** La contrapresión compacta el fundido. Sin ella, entra aire y la densidad del disparo varía.
</details>

---

**ID:** `proc_18` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La historia térmica del material afecta sus propiedades finales.

**¿Qué es el 'Tiempo de Residencia' en inyección?**

- ○ **a)** El tiempo total del ciclo de inyección completo
- ✅ **b)** El tiempo que el polímero pasa expuesto a calor en el barril
- ○ **c)** El tiempo que tarda la pieza en solidificar
- ○ **d)** El tiempo de vida útil estimado del molde

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El tiempo que el polímero pasa expuesto a calor en el barril

**Razonamiento:** Es crucial para materiales sensibles; demasiado tiempo de residencia degrada el polímero.
</details>

### 🟡 Calidad y Defectos (9 preguntas)

---

**ID:** `qual_19` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Defectos contradictorios suelen apuntar a problemas mecánicos del herramental.

**Tienes una pieza con Rebaba (Flash) pero con Peso Bajo (Short shot). ¿Qué indica esta contradicción?**

- ○ **a)** Exceso de presión de sostenimiento aplicada tardíamente
- ✅ **b)** Daño en el molde o desalineación de platinas (Falta de sello)
- ○ **c)** Material demasiado viscoso para la temperatura actual
- ○ **d)** Tiempo de inyección programado muy corto

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Daño en el molde o desalineación de platinas (Falta de sello)

**Razonamiento:** Significa que el material se escapa antes de llenar la pieza. El molde no está sellando correctamente.
</details>

---

**ID:** `qual_20` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El comportamiento del flujo depende de la velocidad de entrada a la cavidad.

**¿Qué defecto causa un 'gusanito' o serpenteo visible en la superficie de la pieza frente a la compuerta?**

- ✅ **a)** Jetting (Efecto Jet)
- ○ **b)** Splay (Ráfagas)
- ○ **c)** Weld Line (Línea de unión)
- ○ **d)** Sink Mark (Rechupado)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Jetting (Efecto Jet)

**Razonamiento:** Ocurre cuando el plástico entra muy rápido a una cavidad abierta y no se pega a las paredes, 'volando' a través de ella.
</details>

---

**ID:** `qual_21` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La compresión rápida de gases genera temperaturas extremas.

**¿Qué fenómeno físico causa el 'Efecto Diesel' (quemadura en el borde de la pieza)?**

- ○ **a)** Oxidación acelerada del metal del molde
- ✅ **b)** Compresión adiabática del aire atrapado
- ○ **c)** Reacción química exotérmica del masterbatch
- ○ **d)** Fricción excesiva del husillo contra el barril

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Compresión adiabática del aire atrapado

**Razonamiento:** El aire atrapado se comprime tan rápido que eleva su temperatura hasta incendiar el plástico (como un motor diesel).
</details>

---

**ID:** `qual_22` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Los volátiles en el material se expanden violentamente al perder presión.

**Las ráfagas plateadas (Silver streaks) distribuidas por toda la pieza suelen indicar:**

- ○ **a)** Exceso de fuerza de cierre en la máquina
- ✅ **b)** Humedad en el material (Vapor)
- ○ **c)** Falta de velocidad de inyección
- ○ **d)** Temperatura de molde demasiado fría

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Humedad en el material (Vapor)

**Razonamiento:** La humedad explota en vapor al inyectarse, dejando estelas plateadas en la dirección del flujo.
</details>

---

**ID:** `qual_23` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La forma en que se unen los frentes de flujo determina la resistencia mecánica.

**¿Cuál es la diferencia técnica entre Línea de Soldadura (Weld) y Línea de Fusión (Meld)?**

- ○ **a)** No existe diferencia, son sinónimos técnicos
- ✅ **b)** El ángulo de encuentro de los frentes de flujo (<135° vs >135°)
- ○ **c)** La temperatura del molde en el punto de contacto
- ○ **d)** El tipo de material amorfo vs semicristalino

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El ángulo de encuentro de los frentes de flujo (<135° vs >135°)

**Razonamiento:** En la 'Weld' los frentes chocan de frente (más débil); en la 'Meld' fluyen paralelos y se unen lateralmente.
</details>

---

**ID:** `qual_24` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El enfriamiento desigual crea tensiones internas que deforman la pieza.

**Para corregir un problema de Pandeo (Warpage) en una pieza plana, ¿qué ajuste es más efectivo?**

- ○ **a)** Aumentar significativamente la temperatura de la masa
- ✅ **b)** Equilibrar el enfriamiento entre lado fijo y móvil
- ○ **c)** Incrementar la fuerza de cierre al máximo disponible
- ○ **d)** Reducir el tiempo de ciclo a la mitad

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Equilibrar el enfriamiento entre lado fijo y móvil

**Razonamiento:** El pandeo ocurre por enfriamiento diferencial; igualar las temperaturas de las caras del molde reduce la tensión interna.
</details>

---

**ID:** `qual_25` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La compatibilidad química es esencial para que el material se funda como una sola masa.

**La 'Delaminación' (capas que se desprenden) es síntoma inequívoco de:**

- ✅ **a)** Contaminación con polímero incompatible
- ○ **b)** Velocidad de inyección excesivamente lenta
- ○ **c)** Presión de sostenimiento inusualmente alta
- ○ **d)** Temperatura de molde peligrosamente baja

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Contaminación con polímero incompatible

**Razonamiento:** Materiales como PE y ABS no se mezclan; forman capas separadas que se pelan como una cebolla.
</details>

---

**ID:** `qual_26` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El material degradado puede acumularse en el sistema y desprenderse aleatoriamente.

**¿Cuál es la fuente más común de 'Puntos Negros' aleatorios en producción continua?**

- ○ **a)** Suciedad y sarro en el sistema de agua de enfriamiento
- ✅ **b)** Acumulación de carbón en zonas muertas del barril/husillo
- ○ **c)** Falla intermitente en el sensor de presión de cavidad
- ○ **d)** Exceso de aditivo estabilizador UV en la mezcla

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Acumulación de carbón en zonas muertas del barril/husillo

**Razonamiento:** Material estancado se degrada a carbón y se desprende poco a poco, contaminando disparos aleatorios.
</details>

---

**ID:** `qual_27` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La calidad moderna se basa en datos y prevención, no solo en inspección.

**¿Qué herramienta de Calidad se utiliza para monitorear la estabilidad estadística (Cpk) del proceso?**

- ○ **a)** Diagrama de Causa y Efecto (Ishikawa)
- ✅ **b)** Gráficos de Control Estadístico (SPC)
- ○ **c)** Análisis de Modo y Efecto de Falla (AMEF)
- ○ **d)** Metodología de orden y limpieza (5S)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Gráficos de Control Estadístico (SPC)

**Razonamiento:** El SPC permite ver si el proceso varía dentro de límites naturales o si hay causas especiales actuando.
</details>

### 🔴 Seguridad Industrial (9 preguntas)

---

**ID:** `safe_28` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Los dispositivos electrónicos pueden fallar; las barreras físicas son la única garantía.

**Antes de meter el cuerpo entre las platinas para mantenimiento, ¿qué paso es INNEGOCIABLE?**

- ○ **a)** Colocar un letrero visible de 'No Operar'
- ✅ **b)** Aplicar bloqueo y etiquetado (LOTO) de energías
- ○ **c)** Avisar verbalmente al supervisor de turno
- ○ **d)** Confiar en que el sensor de seguridad funciona

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Aplicar bloqueo y etiquetado (LOTO) de energías

**Razonamiento:** Confiar en sensores o letreros es causa de muerte. Solo el bloqueo físico de energía garantiza seguridad.
</details>

---

**ID:** `safe_29` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La descomposición térmica de polímeros genera presión interna peligrosa.

**¿Por qué la purga de material degradado representa un riesgo de explosión?**

- ○ **a)** Por una reacción química exotérmica con el oxígeno
- ✅ **b)** Por la expansión violenta de gases atrapados a presión
- ○ **c)** Por el contacto térmico con el agua de refrigeración
- ○ **d)** Por la electricidad estática generada por fricción

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Por la expansión violenta de gases atrapados a presión

**Razonamiento:** El material descompuesto genera gases. Si la boquilla está tapada o fría, al destaparla, el gas expande violentamente.
</details>

---

**ID:** `safe_30` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El cierre del molde debe ser monitoreado para evitar daños costosos.

**El sistema de 'Protección de Molde' (baja presión) sirve para:**

- ○ **a)** Ahorrar energía eléctrica durante la fase de cierre
- ✅ **b)** Detectar obstrucciones y detener el cierre antes de dañar el molde
- ○ **c)** Mejorar el tiempo de ciclo en moldes de apertura rápida
- ○ **d)** Aumentar la vida útil del aceite hidráulico del sistema

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Detectar obstrucciones y detener el cierre antes de dañar el molde

**Razonamiento:** Si el molde encuentra resistencia (pieza atorada) durante el cierre a baja presión, debe abortar para no aplastarla.
</details>

---

**ID:** `safe_31` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Los fluidos a alta presión pueden causar lesiones graves e incendios.

**Ante una ruptura de manguera hidráulica con fuga de aceite a alta presión, lo primero es:**

- ○ **a)** Intentar tapar la fuga manualmente con un trapo
- ✅ **b)** Activar el Paro de Emergencia para detener la bomba
- ○ **c)** Colocar material absorbente en el piso
- ○ **d)** Buscar al técnico de mantenimiento especializado

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Activar el Paro de Emergencia para detener la bomba

**Razonamiento:** El aceite a presión inyecta la piel y es inflamable. Cortar la fuente de energía (bomba) es prioridad.
</details>

---

**ID:** `safe_32` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El equipo de protección estándar es insuficiente para temperaturas extremas.

**Para manipular purgas calientes, el EPP mínimo requerido incluye:**

- ○ **a)** Guantes de látex desechables y lentes oscuros
- ✅ **b)** Careta facial completa y guantes térmicos largos
- ○ **c)** Mascarilla para polvos finos y tapones auditivos
- ○ **d)** Guantes de carnaza cortos y lentes de seguridad claros

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Careta facial completa y guantes térmicos largos

**Razonamiento:** Se requiere protección contra calor extremo y salpicaduras a la cara/cuello.
</details>

---

**ID:** `safe_33` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El izaje de cargas pesadas requiere componentes certificados.

**Al izar un molde, ¿qué condición deben cumplir los cáncamos (eyebolts)?**

- ○ **a)** Estar soldados permanentemente a la placa del molde
- ✅ **b)** Tener capacidad de carga certificada mayor al peso del molde
- ○ **c)** Ser fabricados de acero inoxidable obligatoriamente
- ○ **d)** Estar pintados de color amarillo seguridad brillante

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Tener capacidad de carga certificada mayor al peso del molde

**Razonamiento:** El fallo de un cáncamo subdimensionado es catastrófico. La carga nominal debe exceder el peso total.
</details>

---

**ID:** `safe_34` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Las zonas no visibles de la máquina requieren sistemas de seguridad automáticos.

**¿Qué función cumple el interbloqueo (interlock) de la puerta trasera?**

- ○ **a)** Mantener la puerta cerrada mediante electroimanes
- ✅ **b)** Detener bomba y movimientos si la puerta es abierta
- ○ **c)** Encender la luz de alarma estroboscópica
- ○ **d)** Registrar el evento de apertura en el sistema

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Detener bomba y movimientos si la puerta es abierta

**Razonamiento:** Es una zona ciega para el operador. Si se abre, la máquina debe morir instantáneamente.
</details>

---

**ID:** `safe_35` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El agente extintor incorrecto puede agravar un incendio eléctrico.

**Para un fuego eléctrico en el gabinete de control, ¿qué extintor usas?**

- ○ **a)** Tipo A (Agua presurizada)
- ✅ **b)** Tipo C (CO2 o Polvo Químico)
- ○ **c)** Tipo K (Acetato de Potasio)
- ○ **d)** Tipo D (Polvo para metales)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Tipo C (CO2 o Polvo Químico)

**Razonamiento:** El Tipo C es no conductivo. Usar agua en un tablero energizado causa electrocución.
</details>

---

**ID:** `safe_36` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Las regulaciones locales dictan los estándares mínimos de protección.

**En México, la norma STPS que regula los dispositivos de seguridad en maquinaria es:**

- ○ **a)** NOM-017-STPS (Equipo de Protección Personal)
- ✅ **b)** NOM-004-STPS (Maquinaria y Equipo)
- ○ **c)** NOM-002-STPS (Prevención de Incendios)
- ○ **d)** NOM-029-STPS (Mantenimiento Eléctrico)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** NOM-004-STPS (Maquinaria y Equipo)

**Razonamiento:** La NOM-004 establece la obligación de guardas, paros de emergencia y bloqueos.
</details>

### 🟣 Materiales Plásticos (8 preguntas)

---

**ID:** `mat_37` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La fluidez es una propiedad fundamental para determinar la procesabilidad.

**¿Qué indica el índice MFI (Melt Flow Index) de una resina?**

- ○ **a)** Su resistencia al impacto según prueba Izod
- ✅ **b)** Su viscosidad o facilidad para fluir
- ○ **c)** Su temperatura de transición vítrea específica
- ○ **d)** Su porcentaje de carga de fibra de vidrio

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Su viscosidad o facilidad para fluir

**Razonamiento:** MFI alto = material muy fluido (baja viscosidad); MFI bajo = material duro (alta viscosidad).
</details>

---

**ID:** `mat_38` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Ciertos polímeros sufren daños moleculares irreversibles en presencia de agua.

**¿Qué fenómeno químico sufre el Policarbonato (PC) o Nylon (PA) si se inyecta húmedo?**

- ○ **a)** Polimerización (endurecimiento de la cadena)
- ✅ **b)** Hidrólisis (rotura de cadenas moleculares)
- ○ **c)** Oxidación (cambio de coloración)
- ○ **d)** Reticulación (cross-linking de enlaces)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Hidrólisis (rotura de cadenas moleculares)

**Razonamiento:** El agua corta las cadenas del polímero, destruyendo sus propiedades mecánicas irreversiblemente.
</details>

---

**ID:** `mat_39` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La estructura molecular define cómo cambia el volumen al solidificar.

**Diferencia clave de procesamiento entre amorfos (ej. ABS) y semicristalinos (ej. PP):**

- ○ **a)** Los amorfos requieren temperaturas de molde superiores
- ✅ **b)** Los semicristalinos tienen mayor contracción (shrinkage)
- ○ **c)** Los amorfos son siempre transparentes y rígidos
- ○ **d)** Los semicristalinos presentan menor resistencia al impacto

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Los semicristalinos tienen mayor contracción (shrinkage)

**Razonamiento:** Al cristalizar, las moléculas se empaquetan densamente, reduciendo volumen significativamente más que los amorfos.
</details>

---

**ID:** `mat_40` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El reprocesamiento de material afecta la integridad de las cadenas poliméricas.

**El uso de 'Regrind' (molido) por encima del 20% suele ocasionar:**

- ○ **a)** Mejora en el brillo superficial por cristalización
- ✅ **b)** Pérdida de propiedades mecánicas e inestabilidad
- ○ **c)** Reducción en la temperatura de fusión requerida
- ○ **d)** Aumento considerable en la fuerza de cierre

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Pérdida de propiedades mecánicas e inestabilidad

**Razonamiento:** El material reprocesado tiene historias térmicas previas (degradación) y cadenas más cortas.
</details>

---

**ID:** `mat_41` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El aire de secado debe tener muy baja humedad relativa para ser efectivo.

**Para un secado eficiente, el 'Punto de Rocío' (Dew Point) del aire debe ser:**

- ○ **a)** Positivo (+10°C) para evitar condensación
- ✅ **b)** Negativo (-40°C o inferior)
- ○ **c)** Igual a la temperatura ambiente del taller
- ○ **d)** Igual a la temperatura de fusión del material

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Negativo (-40°C o inferior)

**Razonamiento:** Se requiere aire extremadamente seco para 'robarle' la humedad al plástico.
</details>

---

**ID:** `mat_42` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Los concentrados de color son potentes y deben usarse con precisión.

**¿Cuál es el rango típico de dosificación de Masterbatch (color)?**

- ○ **a)** 10% a 15%
- ✅ **b)** 1% a 4%
- ○ **c)** 0.01% a 0.05%
- ○ **d)** 50% (mitad y mitad)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** 1% a 4%

**Razonamiento:** El masterbatch es muy concentrado. Usar más del 5% altera la química base del material y es costoso.
</details>

---

**ID:** `mat_43` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La resistencia al flujo del material dicta los requisitos de la máquina.

**Procesar materiales de alta viscosidad (duros de fluir) requiere:**

- ✅ **a)** Mayor presión de inyección y temperatura
- ○ **b)** Mayor velocidad de enfriamiento en el molde
- ○ **c)** Menor fuerza de cierre en la unidad de cierre
- ○ **d)** Husillos con bajo ratio de compresión

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Mayor presión de inyección y temperatura

**Razonamiento:** Necesitas más energía (calor y fuerza) para empujar un fluido espeso dentro del molde.
</details>

---

**ID:** `mat_44` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La clasificación de los plásticos depende de sus prestaciones mecánicas y térmicas.

**¿Qué distingue a un plástico de 'Ingeniería' de un 'Commodity'?**

- ○ **a)** El precio de mercado internacional únicamente
- ✅ **b)** Su desempeño térmico y mecánico superior
- ○ **c)** Su facilidad para ser reciclado químicamente
- ○ **d)** Su disponibilidad en colores naturales

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Su desempeño térmico y mecánico superior

**Razonamiento:** Los de ingeniería (PC, PA, POM) soportan cargas y temperaturas donde los commodities (PE, PP) fallan.
</details>

### 🔷 Eficiencia y Lean (8 preguntas)

---

**ID:** `eff_45` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El OEE se ve afectado cuando la máquina no opera a su velocidad de diseño.

**Si una máquina produce piezas buenas, pero corre a 30s de ciclo en lugar de los 25s estándar, ¿qué factor del OEE cae?**

- ○ **a)** Disponibilidad (Availability)
- ✅ **b)** Desempeño (Performance)
- ○ **c)** Calidad (Quality)
- ○ **d)** Ninguno, todo está bien

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Desempeño (Performance)

**Razonamiento:** El Desempeño mide la velocidad real vs la velocidad teórica/estándar.
</details>

---

**ID:** `eff_46` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Clasificar las tareas de preparación es el primer paso para reducir tiempos.

**En la técnica SMED, ¿cómo se define una operación 'Interna'?**

- ○ **a)** Aquella que se puede ejecutar con la máquina en ciclo automático
- ✅ **b)** Aquella que solo se puede realizar con la máquina detenida
- ○ **c)** La que realiza el operador interno de la planta
- ○ **d)** La limpieza profunda del interior del molde

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Aquella que solo se puede realizar con la máquina detenida

**Razonamiento:** Las actividades internas son el cuello de botella del cambio, ya que requieren parar el equipo.
</details>

---

**ID:** `eff_47` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La pérdida de velocidad es uno de los desperdicios más difíciles de detectar.

**Si la máquina produce piezas buenas, pero corre a 30s de ciclo en lugar de los 25s estándar, ¿qué indicador del OEE cae?**

- ○ **a)** Disponibilidad (Availability)
- ✅ **b)** Desempeño (Performance)
- ○ **c)** Calidad (Quality)
- ○ **d)** Ninguno, todo está bien

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Desempeño (Performance)

**Razonamiento:** El Desempeño mide la velocidad real vs la velocidad teórica/estándar.
</details>

---

**ID:** `eff_48` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La preparación anticipada es clave para minimizar el tiempo de paro.

**En un cambio SMED, ¿qué es una actividad 'Externa'?**

- ○ **a)** Desmontar el molde viejo de la platina
- ✅ **b)** Pre-calentar y preparar el molde nuevo mientras la máquina trabaja
- ○ **c)** Limpiar la platina con la máquina parada
- ○ **d)** Ajustar los botadores con la puerta abierta

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Pre-calentar y preparar el molde nuevo mientras la máquina trabaja

**Razonamiento:** Son tareas que se hacen 'fuera' del tiempo de paro, sin detener la producción actual.
</details>

---

**ID:** `eff_49` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La comparación con los mejores de la industria establece la meta a seguir.

**¿Qué porcentaje de OEE se considera 'Clase Mundial'?**

- ○ **a)** 60% o más
- ✅ **b)** 85% o más
- ○ **c)** 99.9%
- ○ **d)** 100%

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** 85% o más

**Razonamiento:** 85% es el benchmark de excelencia aceptado internacionalmente.
</details>

---

**ID:** `eff_50` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Ignorar la capacidad total del molde tiene costos ocultos altos.

**Operar un molde de 4 cavidades con 1 cavidad bloqueada afecta principalmente:**

- ○ **a)** La calidad dimensional de las otras 3 piezas restantes
- ✅ **b)** El costo pieza y la eficiencia del activo
- ○ **c)** La vida útil del husillo y la válvula check
- ○ **d)** El consumo de energía eléctrica del motor principal

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El costo pieza y la eficiencia del activo

**Razonamiento:** Estás usando el 100% de la máquina para sacar el 75% de la producción. Es una pérdida financiera directa.
</details>

---

**ID:** `eff_51` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El ritmo de producción debe sincronizarse con la demanda del cliente.

**¿Qué es el 'Takt Time'?**

- ○ **a)** El tiempo mínimo que la máquina puede correr
- ✅ **b)** El ritmo de producción necesario para cumplir la demanda del cliente
- ○ **c)** El tiempo que tarda el cambio de turno
- ○ **d)** El tiempo de enfriamiento calculado

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** El ritmo de producción necesario para cumplir la demanda del cliente

**Razonamiento:** Es una métrica de demanda, no de capacidad de máquina. (Tiempo disponible / Demanda).
</details>

---

**ID:** `eff_52` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El mantenimiento moderno se basa en datos reales, no en suposiciones.

**El Mantenimiento Predictivo se basa en:**

- ○ **a)** Reparar inmediatamente cuando la máquina falla
- ✅ **b)** Monitoreo de condición (vibración, calor) para anticipar fallas
- ○ **c)** Cambiar piezas por calendario fijo anual
- ○ **d)** Inspección visual diaria por parte del operador

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Monitoreo de condición (vibración, calor) para anticipar fallas

**Razonamiento:** Usa datos para predecir cuándo fallará un componente antes de que suceda.
</details>

### 🟤 Desperdicios (Muda) (8 preguntas)

---

**ID:** `wast_53` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* La limpieza profunda revela anomalías antes de que causen fallas.

**¿Qué principio de las 5S implica que limpiar no es solo embellecer, sino inspeccionar fallas potenciales?**

- ○ **a)** Seiri (Clasificar)
- ✅ **b)** Seiso (Limpiar)
- ○ **c)** Seiton (Ordenar)
- ○ **d)** Shitsuke (Disciplina)

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Seiso (Limpiar)

**Razonamiento:** Limpiar es inspeccionar. Al limpiar detectas fugas, tornillos sueltos o cables pelados.
</details>

---

**ID:** `wast_54` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Producir más de lo necesario genera una cadena de problemas ocultos.

**¿Cuál se considera el 'peor' desperdicio porque oculta a los demás?**

- ○ **a)** Transporte innecesario de material
- ✅ **b)** Sobreproducción
- ○ **c)** Movimientos excesivos del operador
- ○ **d)** Esperas y tiempos muertos en línea

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Sobreproducción

**Razonamiento:** Hacer de más genera inventario, que esconde defectos, paros y problemas de flujo.
</details>

---

**ID:** `wast_55` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Realizar tareas que el cliente no valora es una pérdida neta.

**Tener que recortar rebaba a todas las piezas saliendo de la máquina es un ejemplo de:**

- ○ **a)** Valor Agregado al producto
- ✅ **b)** Sobre-procesamiento (Extra-processing)
- ○ **c)** Eficiencia operativa en acabado
- ○ **d)** Control de Calidad en línea

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Sobre-procesamiento (Extra-processing)

**Razonamiento:** Es trabajo extra que el cliente no paga y que no debería existir si el proceso fuera correcto.
</details>

---

**ID:** `wast_56` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* El material estancado representa capital inmovilizado y riesgo.

**El exceso de Inventario en proceso (WIP) causa:**

- ○ **a)** Mayor flexibilidad de producción diaria
- ✅ **b)** Problemas de flujo de efectivo y riesgo de daños/obsolescencia
- ○ **c)** Reducción significativa de tiempos de entrega
- ○ **d)** Mejor utilización del espacio de planta

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Problemas de flujo de efectivo y riesgo de daños/obsolescencia

**Razonamiento:** El inventario es dinero estancado en el piso que puede dañarse o perderse.
</details>

---

**ID:** `wast_57` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* Las herramientas de estandarización deben estar vigentes para ser útiles.

**¿Qué hace que una Ayuda Visual sea ineficaz o peligrosa para la calidad?**

- ○ **a)** Que tenga demasiados colores o gráficos
- ✅ **b)** Que no esté actualizada o no muestre límites claros de aceptación
- ○ **c)** Que esté plastificada para protección
- ○ **d)** Que incluya fotos reales del producto

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Que no esté actualizada o no muestre límites claros de aceptación

**Razonamiento:** Una ayuda visual obsoleta puede inducir al operador a aceptar piezas malas o rechazar buenas.
</details>

---

**ID:** `wast_58` &nbsp;|&nbsp; **Tipo:** Práctico &nbsp;|&nbsp; **Puntos:** 1.5

> 📌 *Contexto:* El desorden en el área de trabajo es un indicador de falta de disciplina.

**Encontrar herramientas tiradas y piezas mezcladas bajo la máquina indica falla en:**

- ○ **a)** La programación de producción semanal
- ✅ **b)** Las 5S (Orden y Limpieza)
- ○ **c)** El mantenimiento preventivo mensual
- ○ **d)** La calidad de la materia prima entrante

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Las 5S (Orden y Limpieza)

**Razonamiento:** Evidencia falta de Seiton (Orden) y Seiso (Limpieza).
</details>

---

**ID:** `wast_59` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* Los sistemas a prueba de error previenen defectos desde su origen.

**Un dispositivo 'Poka-Yoke' sirve para:**

- ○ **a)** Aumentar la velocidad de la banda transportadora
- ✅ **b)** Hacer imposible cometer un error específico (A prueba de error)
- ○ **c)** Medir la eficiencia del operador en tiempo real
- ○ **d)** Limpiar las piezas automáticamente al salir

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Hacer imposible cometer un error específico (A prueba de error)

**Razonamiento:** Ejemplo: Un conector que solo entra en una posición para evitar polaridad invertida.
</details>

---

**ID:** `wast_60` &nbsp;|&nbsp; **Tipo:** Teórico &nbsp;|&nbsp; **Puntos:** 1

> 📌 *Contexto:* La filosofía Lean busca la optimización de los recursos.

**El objetivo final de eliminar desperdicios (Muda) es:**

- ○ **a)** Despedir personal sobrante en la planta
- ✅ **b)** Aumentar el valor para el cliente y reducir costos
- ○ **c)** Tener la fábrica más bonita estéticamente
- ○ **d)** Cumplir con normas gubernamentales básicas

<details><summary>💡 Respuesta y Razonamiento</summary>

**Correcta:** Aumentar el valor para el cliente y reducir costos

**Razonamiento:** Lean Manufacturing busca maximizar el valor entregado minimizando los recursos usados.
</details>
