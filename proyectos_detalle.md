# Dossier Detallado de Proyectos
## Eudaldo Cal Saul · Desarrollador Full-Stack, IA & Automatización

Este documento recopila la información técnica, arquitecturas, funcionalidades clave y logros de los principales proyectos desarrollados bajo el sello de **D4Lab** y proyectos propios.

---

## 1. D4Sim — Simulador de Vuelo 2D & Tutor IFR con Inteligencia Artificial
**URL:** [https://d4-sim.vercel.app/](https://d4-sim.vercel.app/)  
**Rol:** Desarrollador Mobile & Backend Full-Stack

### 📝 Descripción
Aplicación web y móvil universal orientada al entrenamiento procedimental en vuelo instrumental (IFR) para pilotos. Recrea instrumentación aeronáutica real de forma interactiva y utiliza un tutor virtual inteligente para evaluar y guiar en tiempo real las maniobras de los pilotos.

### 🛠 Tecnologías Utilizadas
*   **Frontend:** React Native, Expo (SDK 54), TypeScript, Expo Router, React Native Reanimated (transiciones a 60 FPS), React Native SVG (renderizado vectorial de instrumentos), Tailwind CSS.
*   **Backend:** Node.js (TypeScript), Vercel Serverless Functions, API REST.
*   **Integraciones de IA:** OpenAI API (GPT-4o-mini) y Gemini API (Gemini 2.5 Flash Lite) con control de flujo por fallbacks y respuestas tipadas mediante *JSON Schema Mode*.
*   **DevOps & Testing:** Jest, `jest-expo` (TDD / Pruebas unitarias), Vercel, Yarn, Git.

### 📐 Arquitectura & Diseño
*   **Clean Architecture & Domain-Driven Design (DDD):**
    *   *Capa de Dominio:* Lógica matemática pura de física de vuelo y cálculo geométrico sin dependencias. Algoritmos aeronáuticos para el cálculo de distancias DME con corrección de altitud (*slant range*), navegación Point-to-Point (P2P) y clasificación de entradas a patrones de espera (Directa, Paralela, Gota de Agua).
    *   *Capa de Servicios:* Servicios aislados para el control de tráfico aéreo (ATC), telemetría y el tutor inteligente (`aiTutorService`).
    *   *Capa de Presentación:* Componentes reactivos optimizados y renderizado SVG de alta frecuencia para los instrumentos (CDI, VOR, ADF, HSI, altímetro, velocímetro).
*   **Estrategia Híbrida de IA & Resiliencia Offline:**
    *   Evaluación en la nube: envía las últimas 30 coordenadas de telemetría a la API de IA para contrastarla con las directrices de los manuales estándar de vuelo (SOPs IFR).
    *   Fallback local: si la conexión falla o para respuestas inmediatas, utiliza un motor heurístico complejo escrito en TypeScript que emite instrucciones precisas de forma instantánea.
*   **Seguridad:** CORS restrictivo y rate limiting por IP en endpoints de IA.

---

## 2. Workflows de Automatización con n8n (D4Lab / TesIA.es)
**Rol:** Arquitecto de Automatización & DevOps

### 📝 Descripción
Ecosistema de automatizaciones desatendidas autoalojado que actúa como el motor operacional y de marketing de D4Lab y la plataforma de oposiciones TesIA.es.

### 🛠 Tecnologías Utilizadas
*   **Orquestación:** n8n (autoalojado en servidor local).
*   **Bases de Datos:** Firestore (NoSQL), PostgreSQL, SQLite.
*   **Modelos de IA:** Gemini, OpenAI, Anthropic, Ollama.
*   **Integración de APIs:** Facebook Graph API, Instagram API, Threads API, Google Business Profile API, Stripe API, Google Drive API.
*   **Infraestructura:** Docker, Vercel, Firebase.

### 📐 Arquitectura & Diseño
*   **Gestión de Estados Asíncronos:** Uso de Firestore para el mantenimiento de sesiones, históricos de interacción y persistencia de estados a lo largo de ejecuciones multipartes.
*   **Orquestación Multimodelo Dinámica:** Enrutamiento inteligente de peticiones hacia diferentes LLMs en función del coste, latencia y complejidad de la tarea (ej. Gemini para tareas masivas de texto, GPT-4o para análisis lógico estructurado).
*   **Pipelines Autónomos Activos:**
    *   *Generación de Contenido:* Generación automática de artículos de blog técnicos y posts para redes sociales basados en efemérides o disparadores del mercado, con auto-publicación desatendida.
    *   *Gamificación y Redes:* Publicación de la "Pregunta del Día", encuestas de engagement semanales y retos de estudio para alumnos de oposiciones.
    *   *Cualificación y Facturación:* Embudo inteligente de leads, cotización de presupuestos PDF dinámicos y pasarela de pago recurrente en Stripe.

---

## 3. TesIA.es — Educación Potenciada por IA para Oposiciones
**URL:** [https://tesia.es](https://tesia.es)  
**Rol:** Desarrollador Full-Stack & Creador del Producto

### 📝 Descripción
Plataforma educativa interactiva (EdTech) para opositores de la Administración General del Estado (AGE), especializada en el cuerpo de Técnicos Auxiliares de Informática (TAI - C1) y Auxiliares Administrativos (C2).

### 🛠 Tecnologías Utilizadas
*   **Stack:** Next.js (React), Firebase Auth, Firestore, Stripe (pagos y suscripciones recurrentes), Tailwind CSS.
*   **IA:** Retrieval-Augmented Generation (RAG), Gemini API.

### 📐 Arquitectura & Diseño
*   **Tutor Socrático RAG:** Motor de tutoría conversacional que asiste a los alumnos respondiendo dudas técnicas complejas de temario legislativo o informático. Emplea RAG contrastando las dudas con las bases de conocimiento oficiales de la convocatoria para evitar alucinaciones.
*   **Generador Dinámico de Tests:** Base de datos relacional/documental que alimenta simulacros y bloques de tests personalizados con explicación analítica generada automáticamente por IA para cada opción de respuesta incorrecta.

---

## 4. D4-Ticket AI — Plataforma de Gestión de Incidencias Agéntica
**URL:** [https://d4-ticket-ai.vercel.app](https://d4-ticket-ai.vercel.app)  
**Rol:** Desarrollador Full-Stack

### 📝 Descripción
Plataforma colaborativa en tiempo real para la gestión, clasificación y resolución automatizada de incidencias y soporte técnico a través de agentes virtuales inteligentes.

### 🛠 Tecnologías Utilizadas
*   **Frontend:** Next.js, React, Tailwind CSS, WebSockets (colaboración en tiempo real).
*   **Backend:** FastAPI (Python), PostgreSQL, Redis (caché y mensajería).
*   **Agentes de IA:** LangGraph (gráficos de estados agénticos), RAG, pgvector (búsqueda semántica de incidencias similares).
*   **Hosting:** Vercel (frontend) y Railway (backend y base de datos).

### 📐 Arquitectura & Diseño
*   **Flujo Agéntico con LangGraph:** Gestión del ticket mediante un grafo de decisión donde diferentes agentes especializados (clasificador, buscador de base de conocimiento, redactor de respuesta) colaboran para proponer soluciones al operador humano o resolver el ticket directamente de manera autónoma.
*   **Búsqueda Semántica Vectorial:** Integración de pgvector para buscar resoluciones históricas parecidas basadas en el significado del reporte de incidencia, reduciendo el tiempo medio de resolución (MTTR).

---

## 5. D4Stream — Detección Predictiva de Fallos de Hardware
**Rol:** Desarrollador backend & Machine Learning Engineer

### 📝 Descripción
Sistema industrializado para la monitorización de telemetría en tiempo real y la predicción temprana de fallos en infraestructuras y dispositivos de hardware crítico.

### 🛠 Tecnologías Utilizadas
*   **Machine Learning & IA:** PyTorch (redes neuronales recurrentes/LSTMs para series temporales), FAISS (búsqueda rápida de vectores de fallos), Ollama (LLM local).
*   **Backend & APIs:** FastAPI (Python).
*   **Base de Datos:** PostgreSQL (TimescaleDB para almacenamiento de telemetría de series de tiempo).

### 📐 Arquitectura & Diseño
*   **Inferencia Predictiva:** Redes neuronales que analizan series temporales procedentes de sensores de hardware y generan puntuaciones de anomalía para predecir cuándo un componente está próximo a fallar operacionalmente.
*   **Buscador Documental Local:** Sistema RAG con base vectorial local utilizando FAISS y Ollama, permitiendo a los técnicos de soporte consultar manuales y diagramas esquemáticos del PLC o hardware dañado mediante lenguaje natural directamente desde el panel de control.
