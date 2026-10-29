# Pre-entrega Módulo 5 — Agente con conocimiento organizacional (RAG)

Entregable: **`PreEntrega_Modulo5_DepaoliJuanManuel.pdf`** (5 piezas en el orden de la consigna).

## Qué se agregó al proyecto JUMA

Los Workers de Soporte y Ventas del Módulo 4 ahora consultan el **Manual de Soporte y Ventas de Jumade v2.1** antes de responder, citan la sección del manual y aplican la regla de contingencia "No sé".

| Archivo | Contenido |
|---|---|
| `Manual_Soporte_y_Ventas_Jumade_v2.pdf` | Documento maestro (6 páginas, 11 secciones, 14 tablas). `build_manual.py` lo genera. |
| `Manual_Soporte_y_Ventas_Jumade_v2.md` | Salida de LlamaParse (LlamaCloud, modo agéntico) ya limpia: tablas HTML → Markdown, sin pies de página. |
| `chunks_manual.json` | 18 fragmentos (uno por sección) con metadatos `seccion`, `titulo`, `documento`, `version`, `vigencia`, `fuente`. |
| `rag_indexar_manual.json` | Workflow **JUMA - RAG: indexar manual en Qdrant**: Code (chunks) → Default Data Loader (metadatos) → Embeddings Google Gemini `gemini-embedding-001` (3072 dims) → Qdrant Vector Store (insert) en la colección `manual_jumade`. |
| `rag_tool_buscar_manual.json` | Workflow **JUMA - RAG: Vector Store Retrieve Tool (buscar en manual)**: Execute Workflow Trigger (`query`) → Set `Parámetros de recuperación` (**top_k = 4**, **min_score = 0.62**, calibrado para gemini-embedding-001; con text-embedding-3-small de OpenAI el valor equivalente fue 0.35) → Qdrant (Get Many) → Filter por score → Code `Formatear contexto citable` (`OK` / `SIN_RESULTADOS`). Debe quedar **publicado/activo** para que los Workers puedan invocarlo. |
| `worker_soporte.json` | Worker de Soporte con la herramienta `buscar_manual_jumade` (Tools Agent) y el bloque RAG en el System Prompt. |
| `worker_ventas.json` | Worker de Ventas: llama al mismo sub-workflow y recibe el contexto citable en el System Message de la LLM Chain. |
| `manager.json` | Manager del Módulo 4 con los modelos migrados a Google Gemini (ver nota). |
| `capturas/` | LlamaCloud (parse), nodo de parámetros Top-K/Min Score, nodo Qdrant, System Prompt RAG, ejecución con la rama Tool en verde. |
| `build_pdf.py` | Genera el PDF del entregable. |

## Nota sobre LlamaCloud

En el plan gratuito de LlamaCloud, el Index y los Data Sources requieren plan pago (la API devuelve `403 requires Starter, Pro, or Enterprise plan`). Por eso LlamaCloud se usó para el **parseo** (LlamaParse) y la base vectorial vive en **Qdrant Cloud** (clúster gratuito `jumade-rag`, colección `manual_jumade`, 23 puntos, 3072 dimensiones, coseno).

## Nota sobre el modelo (migración a Google Gemini)

Durante este módulo se agotaron los créditos gratuitos de OpenAI que trae n8n. Todos los nodos de modelo del proyecto (Manager, Workers, embeddings) pasaron a **Google Gemini** vía una API key gratuita de Google AI Studio (credencial `googlePalmApi` en n8n):

- Chat: `gemini-3.5-flash-lite` (nivel gratuito: 15 solicitudes/min, 500/día; los modelos Flash completos solo permiten 20/día, insuficiente para las pruebas).
- Embeddings: `gemini-embedding-001` (3072 dimensiones). El índice se recreó y el Min Score se recalibró de 0.35 a 0.62 porque los puntajes de similitud no son portables entre modelos.
- Los nodos de IA tienen reintento activado (3 intentos, 15 s) para absorber los límites de cuota (429).

## Resultado de las 5 preguntas ciegas

Ronda final (Gemini): 5/5 correctas en contenido, 4/5 con cita completa (la respuesta de Mac/celular omitió la cita). El caso trampa (merchandising) respondió "No sé" sin inventar. Las rondas previas sirvieron para detectar y corregir dos fallas: expresiones no evaluadas en el System Prompt de los Workers (faltaba el `=` inicial) y una cita fabricada al responder "No sé". Detalle y análisis crítico en el PDF.

## Cómo importar

1. Crear las credenciales **Qdrant API** (URL del clúster + API key) y **Google Gemini (PaLM) API** (key de AI Studio), y la colección `manual_jumade` (3072, Cosine).
2. Importar `rag_indexar_manual.json`, asignar credenciales (Gemini + Qdrant) y ejecutarlo una vez.
3. Importar `rag_tool_buscar_manual.json`, asignar credenciales y **publicarlo**.
4. Importar `worker_soporte.json` y `worker_ventas.json`; en el nodo de herramienta / Execute Workflow volver a seleccionar el sub-workflow RAG.
5. Importar `manager.json` y reasignar los Workers.
