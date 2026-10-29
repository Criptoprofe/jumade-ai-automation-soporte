# Pre-entrega Módulo 5 — Agente con conocimiento organizacional (RAG)

Entregable: **`PreEntrega_Modulo5_DepaoliJuanManuel.pdf`** (5 piezas en el orden de la consigna).

## Qué se agregó al proyecto JUMA

Los Workers de Soporte y Ventas del Módulo 4 ahora consultan el **Manual de Soporte y Ventas de Jumade v2.1** antes de responder, citan la sección del manual y aplican la regla de contingencia "No sé".

| Archivo | Contenido |
|---|---|
| `Manual_Soporte_y_Ventas_Jumade_v2.pdf` | Documento maestro (6 páginas, 11 secciones, 14 tablas). `build_manual.py` lo genera. |
| `Manual_Soporte_y_Ventas_Jumade_v2.md` | Salida de LlamaParse (LlamaCloud, modo agéntico) ya limpia: tablas HTML → Markdown, sin pies de página. |
| `chunks_manual.json` | 18 fragmentos (uno por sección) con metadatos `seccion`, `titulo`, `documento`, `version`, `vigencia`, `fuente`. |
| `rag_indexar_manual.json` | Workflow **JUMA - RAG: indexar manual en Qdrant**: Code (chunks) → Default Data Loader (metadatos) → Embeddings OpenAI `text-embedding-3-small` → Qdrant Vector Store (insert) en la colección `manual_jumade`. |
| `rag_tool_buscar_manual.json` | Workflow **JUMA - RAG: Vector Store Retrieve Tool (buscar en manual)**: Execute Workflow Trigger (`query`) → Set `Parámetros de recuperación` (**top_k = 4**, **min_score = 0.35**) → Qdrant (Get Many) → Filter por score → Code `Formatear contexto citable` (`OK` / `SIN_RESULTADOS`). Debe quedar **publicado/activo** para que los Workers puedan invocarlo. |
| `worker_soporte.json` | Worker de Soporte con la herramienta `buscar_manual_jumade` (Tools Agent) y el bloque RAG en el System Prompt. |
| `worker_ventas.json` | Worker de Ventas: llama al mismo sub-workflow y recibe el contexto citable en el System Message de la LLM Chain. |
| `manager.json` | Manager del Módulo 4 sin cambios funcionales (se exporta para mantener el conjunto completo). |
| `capturas/` | LlamaCloud (parse), nodo de parámetros Top-K/Min Score, nodo Qdrant, System Prompt RAG, ejecución con la rama Tool en verde. |
| `build_pdf.py` | Genera el PDF del entregable. |

## Nota sobre LlamaCloud

En el plan gratuito de LlamaCloud, el Index y los Data Sources requieren plan pago (la API devuelve `403 requires Starter, Pro, or Enterprise plan`). Por eso LlamaCloud se usó para el **parseo** (LlamaParse) y la base vectorial vive en **Qdrant Cloud** (clúster gratuito `jumade-rag`, colección `manual_jumade`, 23 puntos, 1536 dimensiones, coseno).

## Resultado de las 5 preguntas ciegas

5/5 correctas en contenido (ninguna afirmación fuera del manual); 4/5 impecables en formato: en la pregunta sin respuesta en el manual (merchandising) el agente dijo "No sé" pero agregó una cita a una sección inexistente. Se corrigió el prompt ("cuando respondas 'No sé', no agregues ninguna cita"). Detalle y análisis crítico en el PDF.

## Cómo importar

1. Crear la credencial **Qdrant API** (URL del clúster + API key) y la colección `manual_jumade` (1536, Cosine).
2. Importar `rag_indexar_manual.json`, asignar credenciales (OpenAI + Qdrant) y ejecutarlo una vez.
3. Importar `rag_tool_buscar_manual.json`, asignar credenciales y **publicarlo**.
4. Importar `worker_soporte.json` y `worker_ventas.json`; en el nodo de herramienta / Execute Workflow volver a seleccionar el sub-workflow RAG.
5. Importar `manager.json` y reasignar los Workers.
