# Caso de Uso — Asesor de Vehículos 4x4 Off-Road

Proyecto final del Módulo 2 — BSG Institute  
Fecha: Abril 2026

---

## 1. Dominio

### Selección del dominio

El dominio elegido es el asesoramiento técnico de vehículos 4x4 para uso off-road. Este mercado combina conocimiento mecánico especializado (sistemas 4WD, diferenciales, suspensiones, neumáticos) con decisiones de compra de equipamiento y preparación de rutas.

La motivación principal para elegir este dominio fue la **asimetría de información**: un entusiasta principiante puede tardar semanas en encontrar respuestas confiables en foros y videos dispersos, mientras que un experto las resuelve en minutos. Un agente conversacional con perfil persistente del vehículo del usuario puede cerrar esa brecha en segundos.

### Áreas de conocimiento cubiertas

| Área | Ejemplos concretos |
|---|---|
| **Sistemas 4WD** | 4x4 tiempo parcial vs. tiempo completo, alto/bajo rango, cubos de bloqueo, cajas de transferencia (NP231, NP241, BorgWarner) |
| **Diferenciales** | Diferencial abierto, LSD, bloqueo (e-locker, air locker, mecánico), cómo afecta la tracción en terreno técnico |
| **Suspensión** | Resortes de espiral vs. ballesta, kits de elevación, coilovers, long-travel, articulación (flex) |
| **Neumáticos** | Matemática de relaciones de aspecto, índices de carga, tipos de terreno (A/T, M/T), efectos del sobredimensionado en la transmisión |
| **Overlanding y trail** | Recuperación (hi-lift, MaxTrax, cuerda cinética), técnica de winch, cruces de ríos, presión de inflado por superficie |
| **Mercado actual** | Toyota, Jeep, Ford, Land Rover, Rivian; aftermarket (ARB, Fox, Icon, TeraFlex, Warn) |

---

## 2. Perfil del Usuario

El sistema soporta tres arquetipos principales. Cada perfil se almacena en Firestore (`colección users`) y se inyecta en el prompt del sistema en cada turno de conversación para personalizar las respuestas del agente.

### Perfil A — Explorador Principiante

| Campo | Valor |
|---|---|
| **Nombre** | Carlos R. |
| **Vehículo** | 2021 Ford Bronco Sport (stock) |
| **Elevación** | 0 pulgadas (sin lift) |
| **Neumáticos** | 245/65R17 (originales) |
| **Diferenciales de bloqueo** | No |
| **Uso principal** | `overlanding` |
| **Nivel de habilidad** | `beginner` |

**Necesidades:** Entiende poco sobre mecánica 4WD. Necesita que el agente le explique conceptos básicos sin asumir conocimientos previos. Sus preguntas típicas: "¿Cuándo activo el 4WD?", "¿Qué presión de neumáticos llevo en arena?".

**Valor del agente:** Respuestas calibradas a nivel principiante, sin jerga excesiva, con pasos concretos y seguros.

---

### Perfil B — Entusiasta Intermedio

| Campo | Valor |
|---|---|
| **Nombre** | Alex T. |
| **Vehículo** | 2022 Toyota 4Runner TRD Pro |
| **Elevación** | 3.0 pulgadas |
| **Neumáticos** | 285/70R17 |
| **Diferenciales de bloqueo** | Sí |
| **Uso principal** | `overlanding` |
| **Nivel de habilidad** | `intermediate` |

**Necesidades:** Conoce bien su rig pero busca optimizar configuraciones y planificar rutas técnicas. Sus preguntas típicas: "¿Cuánto torque pierdo por el sobredimensionado de neumáticos?", "¿Cuándo activo el bloqueo trasero en roca vs. barro?".

**Valor del agente:** El perfil del rig permite respuestas específicas (p. ej., "con tus 285/70R17 y 3 pulgadas de lift, la presión óptima en arena es 18–22 PSI"). No es necesario repetir especificaciones en cada pregunta.

---

### Perfil C — Experto Trail / Competición

| Campo | Valor |
|---|---|
| **Nombre** | Dana M. |
| **Vehículo** | 2019 Jeep Wrangler JL Rubicon |
| **Elevación** | 6.0 pulgadas |
| **Neumáticos** | 37/12.50R17 |
| **Diferenciales de bloqueo** | Sí (delantero y trasero) |
| **Uso principal** | `trail` |
| **Nivel de habilidad** | `expert` |

**Necesidades:** Busca información técnica avanzada: re-engranaje, límites del eje, configuraciones de winch, datos de fabricantes del aftermarket. Sus preguntas típicas: "¿Qué relación de engranaje necesito con mis 37s para mantener la aceleración original?", "¿Cuál es el límite de tracción del eje Dana 44 con air lockers en ambos extremos?".

**Valor del agente:** Respuestas directas sin nivel introductorio, referencias a marcas y part numbers específicos, uso del buscador Tavily para datos actuales del mercado.

---

## 3. Prompts

Los siguientes prompts fueron utilizados durante el desarrollo del proyecto para implementar cada fase mediante el sistema `opsx:apply`.

### Fase 1 — Backend Core e Integración con Firestore

```
/opsx:apply "Phase 1: Backend Core and Firestore Integration" --description "
Implement the backend structure based on propose.md and 'Guia_proyecto_agenteia.pdf'.

### Tasks

1. Create '/backend' with FastAPI and LangChain setup.
2. Implement Firestore logic in 'firebase/chat_history.py' and 'firebase/clients.py'
   for persistent memory.
3. Create 'seed.py' with 3 rich user profiles for testing.
4. Set up the LangChain agent with the Tavily search tool in 'agent/agent.py'.
5. Include Unit Tests in '/backend/tests' using pytest and mocks for Firebase/OpenAI.

Document everything in English as per the requirements."
```

**Resultado:** Estructura FastAPI con agente LangChain ReAct (GPT-4o), integración Firestore para historial de conversaciones y perfil de usuario, semilla de datos de prueba y suite pytest.

---

### Fase 2 — Desarrollo del Frontend y Streaming SSE

```
/opsx:apply "Phase 2: Frontend Development and SSE Streaming" --description "
Develop the React frontend following the 'Guia_proyecto_agenteia.pdf' specifications.

### Tasks

1. Initialize '/frontend' using Vite and React.
2. Implement the chat interface with a user selector and message history.
3. Integrate Server-Sent Events (SSE) to handle real-time token streaming
   from the backend.
4. Add Vitest unit tests in '/frontend/src/__tests__' for the main components.

Ensure all UI text and documentation are in English."
```

**Resultado:** Interfaz React 18 + Vite + Tailwind CSS con selector de usuario, burbujas de chat en tiempo real vía `EventSource` y cobertura Vitest ≥ 80%.

---

### Fase 3 — Infraestructura como Código y GitHub Actions

```
/opsx:apply "Phase 3: Infrastructure as Code and GitHub Actions" --description "
Provision the cloud environment and automation pipelines.

### Tasks

1. Create '/infrastructure' with Terraform files for GCP Cloud Run and Secret Manager.
2. Configure IAM roles for the service account to access Firestore.
3. Create '.github/workflows/main.yml' to run backend/frontend tests
   and automate deployment to GCP on push to main.
4. Finalize the README.md and CASE_STUDY.md in English."
```

**Resultado:** Terraform para GCP Cloud Run + Secret Manager, pipelines CI/CD en GitHub Actions (tests en PR, despliegue automático en merge a `main`).

---

## 4. Decisiones

### 4.1 Arquitectura del agente — LangChain ReAct con GPT-4o

**Decisión:** Usar el patrón ReAct (Razonamiento + Acción) de LangChain con GPT-4o como modelo base.

**Justificación:** ReAct permite al agente razonar paso a paso antes de elegir si usar la herramienta de búsqueda (Tavily) o responder directamente desde su conocimiento. Esto es crítico en un dominio donde algunas preguntas (mecánica básica) tienen respuestas estables, pero otras (precios de mercado, disponibilidad de piezas) requieren datos actuales. GPT-4o ofrece el equilibrio óptimo entre capacidad de razonamiento técnico y costo por token para este caso de uso.

---

### 4.2 Persistencia — Firestore como base de datos única

**Decisión:** Usar Firebase Firestore (NoSQL documental) para almacenar perfiles de usuario (`users`) e historial de conversaciones (`conversations`). Una sola colección por concepto, con `user_id` como ID de documento.

**Justificación:** La consulta dominante es `user_id → perfil` (lookup O(1)), para la que Firestore es óptimo. No hay relaciones entre entidades que justifiquen SQL. La naturaleza schemaless de Firestore permite añadir campos al perfil (p. ej., `winch_brand`) sin migraciones. El Firebase Admin SDK garantiza que el frontend nunca accede directamente a la base de datos.

---

### 4.3 Streaming — Server-Sent Events (SSE)

**Decisión:** Implementar streaming de tokens vía SSE en el endpoint `GET /api/chat/stream` en lugar de WebSockets o HTTP largo.

**Justificación:** SSE es unidireccional (servidor → cliente), lo que es suficiente para streaming de tokens. Es más simple que WebSockets (no requiere handshake ni gestión de conexión bidireccional) y es nativo en los navegadores con la API `EventSource`. El protocolo de eventos definido (`data: <token>`, `event: done`, `event: error`) es minimalista y fácil de depurar.

---

### 4.4 Testing — Nullable Infrastructure sin mocks de frameworks

**Decisión:** No usar `unittest.mock`, `patch`, ni `vi.mock`. En su lugar, inyectar dependencias (Firestore, LLM, Tavily) como parámetros y proporcionar implementaciones in-memory (stubs) para los tests.

**Justificación:** Los mocks de frameworks acoplan los tests a la implementación interna (nombres de métodos, número de llamadas). Los stubs son implementaciones reales del contrato: si el servicio cambia su interfaz interna sin romper el contrato, los tests siguen pasando. Además, los tests son instantáneos: sin I/O real, sin timeouts, sin llamadas a APIs de pago en CI.

---

### 4.5 Despliegue — GCP Cloud Run con Terraform

**Decisión:** Desplegar el backend como contenedor sin estado en GCP Cloud Run. Gestionar secretos (API keys) con Secret Manager. Provisionamiento con Terraform.

**Justificación:** Cloud Run escala a cero automáticamente (coste cero sin tráfico) y a múltiples instancias bajo carga, sin gestionar servidores. Secret Manager evita hardcodear credenciales en imágenes o variables de entorno del repositorio. Terraform permite reproducir la infraestructura completa en un nuevo proyecto con un solo `terraform apply`.

---

### 4.6 Personalización del prompt — Inyección de perfil en cada turno

**Decisión:** En cada llamada al agente, cargar el perfil del usuario desde Firestore y construir el system prompt con esos datos antes de pasarle el historial de conversación.

**Justificación:** El agente necesita contexto del rig para dar consejos concretos ("con tus 285/70R17..."). Al inyectarlo en el system prompt en lugar de pedirle al usuario que lo repita, se reduce la fricción y se mejora la calidad de las respuestas. Si el usuario actualiza su perfil (nuevo lift, nuevos neumáticos), el cambio toma efecto en el siguiente turno sin reiniciar la sesión.
