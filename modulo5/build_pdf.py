# -*- coding: utf-8 -*-
"""Genera PreEntrega_Modulo5_DepaoliJuanManuel.pdf (A4 apaisado) con las 5 piezas de la consigna."""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Image, Table, TableStyle, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

pdfmetrics.registerFont(TTFont("Inter", "/tmp/fonts/Inter.ttf"))
pdfmetrics.registerFont(TTFont("Inter-I", "/tmp/fonts/Inter-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Inter-B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))

TEAL = colors.HexColor("#01696F"); TEXT = colors.HexColor("#28251D")
MUTED = colors.HexColor("#7A7974"); SURF = colors.HexColor("#F3F2EE"); LINE = colors.HexColor("#D9D7D0")
OK = colors.HexColor("#1B7F3B"); WARN = colors.HexColor("#B4650A")

BASE = "/home/user/workspace/jumade-ai-automation/modulo5/"
OUT = BASE + "PreEntrega_Modulo5_DepaoliJuanManuel.pdf"
CAP = BASE + "capturas/"
PAGE = landscape(A4); W, H = PAGE; M = 14 * mm; CW = W - 2 * M

st = dict(
    h1=ParagraphStyle("h1", fontName="Inter", fontSize=17, leading=21, textColor=TEAL, spaceAfter=2),
    h2=ParagraphStyle("h2", fontName="Inter", fontSize=11.5, leading=14, textColor=TEAL, spaceBefore=5, spaceAfter=3),
    meta=ParagraphStyle("meta", fontName="Inter", fontSize=8.5, leading=11, textColor=MUTED, spaceAfter=4),
    body=ParagraphStyle("body", fontName="Inter", fontSize=8.8, leading=12, textColor=TEXT, spaceAfter=3),
    small=ParagraphStyle("small", fontName="Inter", fontSize=7.6, leading=9.8, textColor=TEXT),
    cap=ParagraphStyle("cap", fontName="Inter-I", fontSize=7.3, leading=9, textColor=MUTED, spaceBefore=1, spaceAfter=4),
    cell=ParagraphStyle("cell", fontName="Inter", fontSize=7.4, leading=9.3, textColor=TEXT),
    cellh=ParagraphStyle("cellh", fontName="Inter", fontSize=7.8, leading=9.6, textColor=colors.white),
    cellm=ParagraphStyle("cellm", fontName="Mono", fontSize=6.6, leading=8.4, textColor=TEXT),
)

def P(t, s="body"): return Paragraph(t, st[s])

def img(path, width=None, height=None):
    iw, ih = PILImage.open(path).size
    if width and not height: height = width * ih / iw
    if height and not width: width = height * iw / ih
    if width > CW: height = height * CW / width; width = CW
    return Image(path, width=width, height=height)

def tbl(rows, widths, head=True, mono_cols=()):
    data = []
    for r_i, r in enumerate(rows):
        row = []
        for c_i, c in enumerate(r):
            style = "cellh" if (head and r_i == 0) else ("cellm" if c_i in mono_cols else "cell")
            row.append(Paragraph(c, st[style]))
        data.append(row)
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    ts = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, LINE),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if head: ts.append(("BACKGROUND", (0, 0), (-1, 0), TEAL))
    for i in range(1, len(data)):
        if i % 2 == 0: ts.append(("BACKGROUND", (0, i), (-1, i), SURF))
    t.setStyle(TableStyle(ts)); return t

def side(left, right, lw=0.5):
    t = Table([[left, right]], colWidths=[CW * lw, CW * (1 - lw)])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (0, 0), 6), ("RIGHTPADDING", (1, 0), (1, 0), 0)]))
    return t

def footer(c, doc):
    c.saveState(); c.setFont("Inter", 7.2); c.setFillColor(MUTED)
    c.drawString(M, 8 * mm, "Pre-entrega Módulo 5 · Ingesta documental y cerebro documental (RAG) · JUMA (Jumade) · Juan Manuel Depaoli")
    c.drawRightString(W - M, 8 * mm, f"Página {doc.page}")
    c.setStrokeColor(LINE); c.line(M, 11 * mm, W - M, 11 * mm); c.restoreState()

FUENTE = "Manual de Soporte y Ventas de Jumade v2.1"
story = []

# ================= PIEZA 1 =================
story += [P("Pre-entrega Módulo 5 · Agente con conocimiento organizacional (RAG)", "h1"),
          P("Proyecto JUMA — asistente de soporte y ventas del estudio de videojuegos Jumade · Alumno: Juan Manuel Depaoli · "
            "Curso AI Automation Avanzado (Coderhouse) · n8n Cloud + LlamaCloud (LlamaParse) + Qdrant Cloud + Google Gemini (gemini-embedding-001 y gemini-3.5-flash-lite) · "
            "Repositorio: github.com/Criptoprofe/jumade-ai-automation-soporte (carpeta modulo5/)", "meta"),
          P("Pieza 1 · Documento parseado en LlamaCloud: jerarquía de títulos y tablas preservadas", "h2")]
p1txt = [P("<b>Documento elegido.</b> <i>Manual de Soporte y Ventas de Jumade v2.1</i> (PDF, 6 páginas, 11 secciones, 14 tablas): es el archivo maestro "
           "institucional que usa el equipo humano para responder a jugadores, tiendas y prensa. Cubre catálogo y precios, plataformas confirmadas y "
           "descartadas, requisitos de PC, claves y activación, política de reembolsos, diagnóstico por síntoma, niveles de prioridad y tiempos de "
           "respuesta, hoja de ruta, descuentos, prensa, privacidad y glosario.", "body"),
         P("<b>Qué se limpió antes de subirlo.</b> Se eliminaron pies de página con numeración y separadores decorativos, se quitaron marcadores de "
           "negrita dentro de los títulos, se unificaron las tablas con encabezado real en la primera fila (sin celdas combinadas ni columnas vacías) "
           "y se corrigieron palabras cortadas por saltos de línea. Luego del parseo se convirtieron las tablas HTML a tablas Markdown y se "
           "fragmentó el texto por sección (18 fragmentos con metadatos <font face='Mono'>seccion</font>, <font face='Mono'>titulo</font>, "
           "<font face='Mono'>version</font> y <font face='Mono'>fuente</font>).", "body"),
         P("<b>Qué muestra la captura.</b> Resultado del job de LlamaParse (modo agéntico, 6 páginas, estado SUCCESS): los encabezados "
           "<i>1. Sobre Jumade…</i> y <i>1.1 Catálogo vigente</i> conservan su jerarquía y la tabla de catálogo quedó interpretada como celdas "
           "(Producto · Género · Plataformas · Precio · Estado), no como texto plano.", "body"),
         P("<b>Nota honesta sobre el almacén.</b> En el plan gratuito de LlamaCloud, el Index y los Data Sources exigen plan pago (la API responde "
           "403 \"requires Starter, Pro, or Enterprise plan\", verificado el 29/10/2026). Por eso LlamaCloud se usó para el parseo y la base vectorial "
           "se montó en <b>Qdrant Cloud</b> (colección <font face='Mono'>manual_jumade</font>, 23 puntos, 3072 dimensiones, métrica coseno) con "
           "embeddings <font face='Mono'>gemini-embedding-001</font> (Google AI Studio, nivel gratuito). La arquitectura y los parámetros son los mismos que pide la consigna.", "body")]
story += [side(img(CAP + "01_llamacloud_parse.png", width=CW * 0.5), p1txt, 0.5),
          P("Figura 1. LlamaCloud › Parse › job pjb-4fcb… con Manual_Soporte_y_Ventas_Jumade_v2.pdf: vista Markdown del resultado con la jerarquía de títulos y la tabla 1.1 como celdas.", "cap")]

# ================= PIEZA 2 =================
story += [PageBreak(), P("Pieza 2 · Vector Store Retrieve Tool: Top-K = 4 y Minimum Score = 0,62", "h2"),
          P("La herramienta <font face='Mono'>buscar_manual_jumade</font> es un sub-workflow (<i>JUMA - RAG: Vector Store Retrieve Tool</i>) acoplado al "
            "AI Agent del Worker de Soporte (modo Tools Agent) y al Worker de Ventas. Los dos parámetros viven en un único nodo Set para calibrarlos en un solo "
            "lugar; el nodo Qdrant Vector Store (Get Many) toma el Top-K por expresión y un Filter descarta todo fragmento por debajo del Minimum Score.", "body")]
story += [side(img(CAP + "03_set_topk_minscore.png", width=CW * 0.5), img(CAP + "04_qdrant_retrieve_node.png", width=CW * 0.5), 0.5), Spacer(1, 2),
          P("Figura 2 (izq.). Nodo <b>Parámetros de recuperación (Top-K y Min Score)</b>: top_k = 4, min_score = 0.62. "
            "Figura 3 (der.). Nodo <b>Qdrant Vector Store (Retrieve: Get Many)</b>: colección manual_jumade, Prompt = {{ $json.query }}, Limit = {{ $json.top_k }}.", "cap")]
just = [["Decisión", "Por qué"],
        ["Top-K = 4", "Cada fragmento es una sección completa del manual (≈ 150–300 tokens). Con K = 4 el contexto inyectado ronda 800–1.100 tokens: alcanza para que "
                      "una pregunta que cruza dos secciones (p. ej. precio de la Deluxe + qué incluye, o plataformas + requisitos) tenga las dos a mano, y entra holgado "
                      "en la cuota gratuita de Gemini Flash-Lite (250K tokens/min). K = 2 dejó afuera la sección correcta en la calibración (la Deluxe apareció en 3.ª posición); K ≥ 6 sólo agregaba "
                      "ruido (glosario, reembolsos) sin cambiar la respuesta."],
        ["Minimum Score = 0,62", "El umbral depende del modelo de embeddings, así que se calibró empíricamente con 7 consultas de prueba. Con gemini-embedding-001 los fragmentos "
                                 "realmente pertinentes puntuaron entre 0,634 y 0,78 de similitud coseno, mientras que una consulta fuera de dominio (\"¿qué clima hace en Tandil?\") "
                                 "llegó a 0,608 sólo porque el manual menciona Tandil. El umbral 0,62 queda en el hueco entre ambos grupos: descarta lo irrelevante y los fragmentos "
                                 "de relleno (la Deluxe quedó con 3 fragmentos en lugar de 4; Mac/celular con 1) sin recortar el acierto más bajo (1.1 Catálogo, 0,634). "
                                 "Con la primera versión del índice (text-embedding-3-small de OpenAI) el mismo análisis dio 0,35: relevantes 0,39–0,70, fuera de dominio 0,315."],
        ["Balance precisión / costo", "Prioricé precisión contextual sobre ahorro extremo: el costo marginal de 2 fragmentos más es despreciable frente al costo de una "
                                      "respuesta inventada a un jugador. El tope de 4 y el umbral evitan el otro extremo (pegar el manual entero en cada consulta) y mantienen cada turno "
                                      "en 2–3 llamadas cortas al modelo, lo que importa en un nivel gratuito limitado por solicitudes por minuto."]]
story += [tbl(just, [CW * 0.16, CW * 0.84])]

# ================= PIEZA 3 =================
story += [PageBreak(), P("Pieza 3 · System Prompt RAG: fuentes citadas y regla de contingencia \"No sé\"", "h2")]
p3txt = [P("El bloque <b># BASE DE CONOCIMIENTO (RAG) — HERRAMIENTA buscar_manual_jumade</b> se agregó al System Message del Worker de Soporte "
           "(AI Agent, Tools Agent) y, con el mismo texto, al Worker de Ventas. Reglas, tal como están en n8n:", "body"),
         P("<b>0.</b> Antes de afirmar cualquier dato fáctico (plataformas, requisitos, precios, reembolsos, plazos, claves, versiones, descuentos, prensa) "
           "tenés que llamar a la herramienta con la consulta reformulada en términos del manual.", "small"), Spacer(1, 3),
         P("<b>1.</b> Respondé únicamente con la información que aparece en los fragmentos recuperados. No uses conocimiento previo ni completes huecos con suposiciones.", "small"), Spacer(1, 3),
         P("<b>2.</b> Citá la fuente al final de la respuesta con este formato exacto: <font face='Mono'>(Fuente: Manual de Soporte y Ventas de Jumade v2.1, "
           "sección \"&lt;título de la sección del fragmento&gt;\")</font>.", "small"), Spacer(1, 3),
         P("<b>3. REGLA DE ORO \"NO SÉ\":</b> si la herramienta devuelve SIN_RESULTADOS, o si los fragmentos no contienen la respuesta concreta a lo que se "
           "pregunta, decí de forma explícita <b>\"No sé, no tengo ese dato confirmado en el manual\"</b> y ofrecé derivar la consulta a una persona del equipo. "
           "Nunca inventes ni extrapoles. Cuando respondas \"No sé\", no agregues ninguna cita de fuente.", "small"), Spacer(1, 3),
         P("<b>4.</b> Si el fragmento indica que algo \"no está disponible\" o \"no se puede prometer\", transmitilo tal cual; eso sí es información confirmada.", "small"), Spacer(1, 5),
         P("<b>Descripción de negocio de la herramienta</b> (guía la activación en el ciclo ReAct): <i>\"Busca en el Manual de Soporte y Ventas de Jumade v2.1 "
           "(única fuente oficial) y devuelve los fragmentos más relevantes con su sección y puntaje. Usala SIEMPRE antes de afirmar precios, plataformas, "
           "requisitos, reembolsos, plazos, claves, versiones o promociones.\"</i>", "body")]
story += [side(img(CAP + "06_worker_soporte_system_prompt.png", width=CW * 0.5), p3txt, 0.5),
          P("Figura 4. Editor de expresión del System Message del nodo <b>Agente Soporte (redacción)</b>, Worker de Soporte Técnico: se leen la instrucción de citar fuentes (regla 2) y la regla de contingencia \"No sé\" (regla 3).", "cap")]

# ================= PIEZA 4 =================
story += [PageBreak(), P("Pieza 4 · Reporte de validación: 5 preguntas ciegas (vocabulario informal y sinónimos)", "h2"),
          P("Las preguntas entraron por el chat del Manager (no por el Worker directo), para validar el circuito completo: clasificación → Worker → herramienta RAG → "
            "respuesta citada. Columna \"Fragmento recuperado\": fragmentos que pasaron el Min Score, con su similitud coseno. Ronda final con la configuración definitiva "
            "(Gemini Flash-Lite + gemini-embedding-001, Top-K 4, Min Score 0,62): ejecuciones n8n n.º 267–281 del 29/10/2026. Las rondas previas (n.º 189–264) se usaron para encontrar y corregir las fallas que se analizan en la página siguiente.", "body")]
G = "<font face='Inter-B' color='#1B7F3B'>✔</font>"; Y = "<font face='Inter-B' color='#B4650A'>⚠</font>"
rows = [["#", "Pregunta (informal / sinónimo)", "Intención", "Fragmento recuperado (sección · score)", "Respuesta del agente", "Veredicto"],
        ["1", "\"Hola, ¿el juego anda en la Steam Deck?\" (<i>anda</i> = funciona / compatibilidad)", "Soporte técnico",
         "Consulta reformulada por el agente: «Steam Deck requisitos plataformas Jumade». 1.2 Plataformas confirmadas y no confirmadas · 0,780 (tabla: «Funciona en Steam Deck con la calificación Verificado»); 5.1 Diagnóstico · 0,758; 5.2 Rutas de archivos · 0,749; 1. Sobre Jumade · 0,748",
         "\"Sí, el juego funciona en la Steam Deck con la calificación «Verificado» vía Proton. Si tenés algún inconveniente al iniciarlo, probá verificando los archivos del juego desde Steam.\" (Fuente: Manual… v2.1, sección \"1.2 Plataformas confirmadas y no confirmadas\")",
         G + " Correcto (cita fuente)"],
        ["2", "\"mandé un mail por un bug ayer, ¿cuánto tardan en contestar?\" (<i>mail/bug/tardan</i> ≠ vocabulario del manual: correo, incidencia, tiempo de primera respuesta)", "Soporte técnico",
         "Reformulada: «plazos de respuesta soporte mail bug». 6. Niveles de prioridad y tiempos de respuesta · 0,725 y 0,710 (Alta 4 h hábiles · Normal 1 día hábil · Baja 3 días hábiles); 3.2 Claves · 0,639; Portada · 0,622",
         "\"Los tiempos de respuesta dependen de la prioridad asignada al caso: los problemas técnicos que impiden jugar tienen un plazo de primera respuesta de 1 día hábil, mientras que los bugs menores sin bloqueo se responden en 3 días hábiles…\" (Fuente: Manual… v2.1, sección \"6. Niveles de prioridad y tiempos de respuesta\")",
         G + " Correcto (cita fuente; eligió las dos prioridades que aplican a un bug)"],
        ["3", "\"¿hay versión para Mac o para el celular?\" (<i>Mac/celular</i> vs. macOS / iOS y Android en el manual)", "Ventas",
         "1.2 Plataformas confirmadas y no confirmadas · 0,720 (macOS: «No disponible, sin planes anunciados»; iOS/Android: «No disponible»). Los otros 3 candidatos (0,603–0,615) quedaron bajo el umbral: 1 solo fragmento inyectado",
         "\"Te cuento que actualmente no hay versión para Mac ni planes anunciados para celulares. Contame si te interesa alguna de las plataformas disponibles para ver cómo podemos ayudarte.\"",
         Y + " Correcto en contenido (negativo confirmado por el manual); omitió la cita de fuente"],
        ["4", "\"¿cuánto sale la edición Deluxe y qué trae?\" (<i>sale/trae</i> = precio / contenido del bundle)", "Ventas",
         "7. Actualizaciones y DLC · 0,651; 11. Glosario · 0,636 (Edición Deluxe = bundle con juego base, banda sonora e «Islas del Norte»); 1.1 Catálogo vigente · 0,634 (22,99 USD); 1.2 Plataformas · 0,608 → descartado por Min Score",
         "\"La Edición Deluxe cuesta 22,99 USD y trae el juego base, la banda sonora y la expansión «Islas del Norte».\" (Fuente: Manual… v2.1, sección \"1.1 Catálogo vigente\")",
         G + " Correcto (cruza 2 fragmentos y cita el del precio)"],
        ["5", "\"¿venden remeras o merchandising de Jumade?\" (tema <b>ausente</b> del manual: caso diseñado para la regla \"No sé\")", "Ventas",
         "1. Sobre Jumade y catálogo · 0,758; 9.1 Claves de prensa · 0,718; Portada · 0,715; 1.1 Catálogo · 0,698 — los 4 pasan el umbral por vocabulario comercial compartido, pero ninguno habla de merchandising",
         "\"No sé, no tengo ese dato confirmado. Si querés, puedo derivar tu consulta a una persona del equipo para que te lo confirme.\"",
         G + " Correcto (aplicó la regla \"No sé\", sin inventar ni citar)"]]
story += [tbl(rows, [CW * 0.025, CW * 0.19, CW * 0.075, CW * 0.27, CW * 0.29, CW * 0.15])]
story += [Spacer(1, 4),
          P("<b>Métrica de precisión: 5/5 respuestas correctas en contenido (100 %); 4/5 con el formato completo de cita (80 %).</b> Ninguna respuesta afirmó algo que no "
            "estuviera en el manual y el caso trampa (merchandising) activó la contención \"No sé\" sin cita fabricada. Recall de recuperación: en los 4 casos con respuesta en el "
            "manual, la sección correcta superó el umbral (en el caso 4 en 3.ª posición, con 0,634: a 0,014 del Min Score, el margen más fino de la batería).", "body")]

story += [PageBreak(), P("Pieza 4 (cont.) · Análisis crítico, fallas encontradas en las rondas previas y acciones correctivas", "h2")]
an = [["Hallazgo", "Qué pasó", "Causa raíz", "Acción correctiva (aplicada / pendiente)"],
      ["Falsos negativos en la 1.ª ronda (casos 3 y 4)",
       "El Worker de Ventas contestó \"No sé\" a Mac/celular y a la Deluxe aunque la herramienta había recuperado 1.2 Plataformas y 1.1 Catálogo.",
       "Bug de configuración, no de recuperación: el System Message de ambos Workers no empezaba con \"=\", así que n8n no evaluaba la expresión <font face='Mono'>{{ $json.contexto }}</font> y el modelo recibía el texto literal en lugar de los fragmentos.",
       "<b>Aplicada.</b> Se antepuso \"=\" a los System Messages; desde la 2.ª ronda ambos casos pasaron a correctos. Lección: validar en la vista de ejecución que el prompt final contenga los fragmentos (rama Tool en verde y tokens de entrada &gt; 1.500)."],
      ["Cita inventada al responder \"No sé\" (caso 5, 2.ª ronda)",
       "El agente aplicó bien la contención pero cerró con <i>(Fuente: …, sección \"Merchandising\")</i>, una sección que no existe.",
       "El prompt exigía citar \"siempre\" y el modelo resolvió la tensión fabricando la sección. Los 4 fragmentos superan el umbral por compartir vocabulario comercial (\"venden\", \"Jumade\"), así que la herramienta no devuelve SIN_RESULTADOS y la contención depende del prompt.",
       "<b>Aplicada y verificada.</b> Nueva regla: \"Cuando respondas 'No sé', no agregues ninguna cita de fuente\". En la ronda final el caso 5 respondió \"No sé\" limpio. Subir el Min Score no es alternativa: a 0,70 también se perdería la Deluxe (0,634)."],
      ["Cambio de modelo de embeddings a mitad del trabajo",
       "Los créditos gratuitos de OpenAI en n8n se agotaron durante la 3.ª ronda (\"used all your free n8n AI credits\"). Se migró a Google Gemini (AI Studio, nivel gratuito).",
       "Un umbral de similitud no es portable entre modelos: gemini-embedding-001 comprime los puntajes (fuera de dominio 0,61 vs. 0,32 con OpenAI). Además, la herramienta publicada seguía corriendo la versión anterior hasta volver a publicarla.",
       "<b>Aplicada.</b> Colección recreada (3072 dims), manual reindexado, Min Score recalibrado de 0,35 a 0,62 con las mismas 7 consultas, sub-workflow republicado. Queda documentado en el plan de gobernanza: todo cambio de embeddings obliga a reindexar y recalibrar."],
      ["Límites de cuota del nivel gratuito (429)",
       "Con gemini-3.5-flash los Workers fallaron por \"too many requests\": el nivel gratuito permite 5 solicitudes/min y 20/día para los modelos Flash completos.",
       "Cada pregunta consume 3–4 llamadas (clasificador + agente ReAct con herramienta + extractor). La rama de contingencia respondió con el mensaje de escalamiento, sin inventar.",
       "<b>Aplicada.</b> Todos los nodos pasaron a gemini-3.5-flash-lite (15/min, 500/día) y los nodos de IA tienen reintento (3 intentos, 15 s). La contingencia funcionó como estaba diseñada: ante error del modelo, el jugador recibe un mensaje de derivación humana."],
      ["Cita omitida (caso 3, ronda final)",
       "La respuesta fue correcta pero sin el bloque (Fuente: …).",
       "El Worker de Ventas usa una LLM Chain con salida JSON estructurada; con un solo fragmento inyectado, Flash-Lite priorizó la brevedad pedida (máximo 3 oraciones) por sobre la regla de cita.",
       "<b>Pendiente.</b> Mover la cita a un campo propio del JSON de salida (<font face='Mono'>fuente</font>) para que no compita con el límite de oraciones, y migrar Ventas al esquema Tools Agent que ya usa Soporte, que reformula la consulta y cita de forma consistente."],
      ["Consulta fuera de dominio (prueba extra)",
       "\"¿qué clima hace en Tandil?\" → mejor fragmento 0,608 &lt; 0,62 → SIN_RESULTADOS → \"No sé\" sin cita.",
       "El umbral cumple su función de contención para temas ajenos a la empresa, incluso cuando comparten una palabra clave (Tandil) con el manual.",
       "Ninguna. Se incorpora al set de regresión del plan de gobernanza."]]
story += [tbl(an, [CW * 0.15, CW * 0.27, CW * 0.29, CW * 0.29])]
story += [KeepTogether([Spacer(1, 4), img(CAP + "07_exec_worker_soporte_208.png", height=48 * mm),
          P("Figura 5. Ejecución n.º 268 del Worker de Soporte (pregunta 1, ronda final): la rama <b>Tool → buscar_manual_jumade</b> en verde (1 ítem), 2 llamadas al modelo Gemini (ciclo ReAct) y la salida final con la cita a la sección 1.2 del manual.", "cap")])]

# ================= PIEZA 5 =================
story += [PageBreak(), P("Pieza 5 · Plan de gobernanza de la base de conocimiento indexada", "h2"),
          P("Alcance: colección <font face='Mono'>manual_jumade</font> en Qdrant Cloud (clúster jumade-rag), workflow de ingesta <i>JUMA - RAG: indexar manual en Qdrant</i>, "
            "el PDF fuente en <font face='Mono'>modulo5/Manual_Soporte_y_Ventas_Jumade_v2.pdf</font> y su Markdown limpio. El manual ya declara \"Próxima revisión: 1 de enero de 2027\"; "
            "el plan alinea la base vectorial con ese calendario para que el documento y el índice nunca se desacoplen.", "body")]
gov = [["Dimensión", "Regla"],
       ["Cada cuánto se revisa", "<b>Revisión trimestral programada</b> el 1 de enero, 1 de abril, 1 de julio y 1 de octubre (coincide con la revisión del manual). "
                                 "<b>Revisión extraordinaria</b> dentro de las 48 h ante cualquier cambio de precio, de plataforma, de política de reembolsos, lanzamiento de DLC o parche mayor (versión x.0). "
                                 "<b>Chequeo semanal automático</b>: una consulta de prueba al clúster para que el plan gratuito de Qdrant no suspenda la colección por inactividad (se suspende a la semana y se borra a las 4 semanas sin uso)."],
       ["Quién es el responsable", "<b>Juan Manuel Depaoli (fundador)</b>, dueño del manual y del índice: aprueba el contenido, corre la reindexación y firma el registro de cambios. "
                                   "<b>Suplente:</b> la persona de soporte de turno, que puede detener el acceso del agente al índice (desactivar la herramienta) pero no publicar una versión nueva. "
                                   "El agente JUMA nunca escribe en la colección: sólo lee."],
       ["Cuándo se elimina o reemplaza un documento", "Se <b>reemplaza</b> cuando: (a) contradice un precio, plataforma o política vigente en la tienda o en la web; (b) queda más de una versión atrás del manual oficial (p. ej. índice en v2.1 y manual en v2.3); "
                                                    "(c) el set de regresión arroja 2 o más respuestas incorrectas o \"No sé\" injustificados. "
                                                    "Se <b>elimina</b> sin reemplazo cuando el documento deja de ser fuente oficial (producto discontinuado, política derogada) o duplica contenido ya cubierto por otro fragmento más nuevo."],
       ["Cómo se reemplaza (procedimiento)", "1) Actualizar el PDF y subir una versión nueva (v2.x) con fecha de vigencia en la portada. 2) Parsear en LlamaCloud y limpiar tablas. 3) Regenerar los fragmentos con metadatos "
                                             "<font face='Mono'>version</font> y <font face='Mono'>vigencia</font>. 4) <b>Vaciar la colección e indexar de cero</b> (nunca mezclar versiones: un índice = una versión); si cambia el modelo de embeddings, además recrear la colección con la dimensión nueva y recalibrar el Min Score con el set de 7 consultas. "
                                             "5) Correr el set de regresión (las 5 preguntas ciegas + la consulta fuera de dominio) y exigir 5/5 con cita correcta. 6) Anotar en el CHANGELOG del repositorio: versión, fecha, responsable, cantidad de puntos y resultado del set."],
       ["Trazabilidad y control", "Cada fragmento lleva <font face='Mono'>documento</font>, <font face='Mono'>version</font>, <font face='Mono'>seccion</font> y <font face='Mono'>fuente</font>; toda respuesta del agente cita la sección, "
                                  "así que un error se rastrea al fragmento exacto. El log del Manager en Google Sheets permite auditar qué fragmentos se usaron en cada conversación. "
                                  "Si un jugador o el equipo reportan una respuesta incorrecta, se abre una revisión extraordinaria aunque no toque la fecha trimestral."],
       ["Qué NO se indexa", "Conversaciones de usuarios, datos personales, borradores internos, hojas de ruta no publicadas ni documentos de terceros sin permiso. La base de conocimiento es sólo documentación institucional aprobada y vigente."]]
story += [tbl(gov, [CW * 0.17, CW * 0.83])]
story += [Spacer(1, 4),
          P("Archivos en el repositorio <font face='Mono'>jumade-ai-automation-soporte/modulo5/</font>: manual fuente (PDF y Markdown limpio), <font face='Mono'>chunks_manual.json</font>, "
            "workflows exportados (<font face='Mono'>rag_tool_buscar_manual.json</font>, <font face='Mono'>rag_indexar_manual.json</font>, Workers y Manager con Gemini), capturas y este PDF.", "small")]

doc = BaseDocTemplate(OUT, pagesize=PAGE, leftMargin=M, rightMargin=M, topMargin=10 * mm, bottomMargin=14 * mm,
                      title="Pre-entrega Módulo 5 — Agente con conocimiento organizacional (JUMA)", author="Juan Manuel Depaoli")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(M, 14 * mm, CW, H - 24 * mm, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=footer)])
doc.build(story)
print("OK", OUT)
