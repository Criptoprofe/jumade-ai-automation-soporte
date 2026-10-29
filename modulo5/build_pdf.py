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
            "Curso AI Automation Avanzado (Coderhouse) · n8n Cloud + LlamaCloud (LlamaParse) + Qdrant Cloud + OpenAI embeddings · "
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
           "se montó en <b>Qdrant Cloud</b> (colección <font face='Mono'>manual_jumade</font>, 23 puntos, 1536 dimensiones, métrica coseno) con "
           "embeddings <font face='Mono'>text-embedding-3-small</font>. La arquitectura y los parámetros son los mismos que pide la consigna.", "body")]
story += [side(img(CAP + "01_llamacloud_parse.png", width=CW * 0.5), p1txt, 0.5),
          P("Figura 1. LlamaCloud › Parse › job pjb-4fcb… con Manual_Soporte_y_Ventas_Jumade_v2.pdf: vista Markdown del resultado con la jerarquía de títulos y la tabla 1.1 como celdas.", "cap")]

# ================= PIEZA 2 =================
story += [PageBreak(), P("Pieza 2 · Vector Store Retrieve Tool: Top-K = 4 y Minimum Score = 0,35", "h2"),
          P("La herramienta <font face='Mono'>buscar_manual_jumade</font> es un sub-workflow (<i>JUMA - RAG: Vector Store Retrieve Tool</i>) acoplado al "
            "AI Agent del Worker de Soporte (modo Tools Agent) y al Worker de Ventas. Los dos parámetros viven en un único nodo Set para calibrarlos en un solo "
            "lugar; el nodo Qdrant Vector Store (Get Many) toma el Top-K por expresión y un Filter descarta todo fragmento por debajo del Minimum Score.", "body")]
story += [side(img(CAP + "03_set_topk_minscore.png", width=CW * 0.5), img(CAP + "04_qdrant_retrieve_node.png", width=CW * 0.5), 0.5), Spacer(1, 2),
          P("Figura 2 (izq.). Nodo <b>Parámetros de recuperación (Top-K y Min Score)</b>: top_k = 4, min_score = 0.35. "
            "Figura 3 (der.). Nodo <b>Qdrant Vector Store (Retrieve: Get Many)</b>: colección manual_jumade, Prompt = {{ $json.query }}, Limit = {{ $json.top_k }}.", "cap")]
just = [["Decisión", "Por qué"],
        ["Top-K = 4", "Cada fragmento es una sección completa del manual (≈ 150–300 tokens). Con K = 4 el contexto inyectado ronda 800–1.100 tokens: alcanza para que "
                      "una pregunta que cruza dos secciones (p. ej. precio de la Deluxe + qué incluye, o plataformas + requisitos) tenga las dos a mano, y cuesta "
                      "centavos con gpt-5-mini. K = 2 dejó afuera la sección correcta en la calibración (la Deluxe apareció en 3.ª posición); K ≥ 6 sólo agregaba "
                      "ruido (glosario, reembolsos) sin cambiar la respuesta."],
        ["Minimum Score = 0,35", "En la calibración previa con 7 consultas, los fragmentos realmente pertinentes puntuaron entre 0,39 y 0,70 de similitud coseno, "
                                 "mientras que una consulta fuera de dominio (\"¿qué clima hace en Tandil?\") no superó 0,315. El umbral 0,35 queda en el hueco entre "
                                 "ambos grupos: filtra lo irrelevante (la herramienta devuelve SIN_RESULTADOS y el agente responde \"No sé\") sin recortar aciertos "
                                 "con puntaje bajo como 1.1 Catálogo (0,392) o 1.2 Plataformas (0,466)."],
        ["Balance precisión / costo", "Prioricé precisión contextual sobre ahorro extremo: el costo marginal de 2 fragmentos más es despreciable frente al costo de una "
                                      "respuesta inventada a un jugador. El tope de 4 y el umbral evitan el otro extremo (pegar el manual entero en cada consulta)."]]
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
            "respuesta citada. Columna \"Fragmento recuperado\": fragmentos que pasaron el Min Score, con su similitud coseno. Ejecuciones n8n n.º 204–216 del 29/10/2026 "
            "(la pregunta 5 corresponde a la ronda anterior, n.º 201–203, porque en la ronda final se agotaron los créditos gratuitos de OpenAI en n8n antes de ese turno).", "body")]
G = "<font face='Inter-B' color='#1B7F3B'>✔</font>"; Y = "<font face='Inter-B' color='#B4650A'>⚠</font>"
rows = [["#", "Pregunta (informal / sinónimo)", "Intención", "Fragmento recuperado (sección · score)", "Respuesta del agente (resumida)", "Veredicto"],
        ["1", "\"Hola, ¿el juego anda en la Steam Deck?\" (<i>anda</i> = funciona / compatibilidad)", "Ventas",
         "1.2 Plataformas confirmadas y no confirmadas · 0,605 (tabla: Linux/SteamOS, «Funciona en Steam Deck con la calificación Verificado»); 5.1 Diagnóstico · 0,551; 7. Hoja de ruta · 0,487; 11. Glosario · 0,483",
         "\"Sí: el juego funciona en Steam Deck (se ejecuta vía Proton y tiene la calificación «Verificado»)…\" (Fuente: …, sección \"1.2 Plataformas confirmadas y no confirmadas\")",
         G + " Correcto (cita fuente)"],
        ["2", "\"mandé un mail por un bug ayer, ¿cuánto tardan en contestar?\" (<i>mail/bug/tardan</i> ≠ vocabulario del manual: correo, incidencia, tiempo de primera respuesta)", "Soporte técnico",
         "6. Niveles de prioridad y tiempos de respuesta · 0,702 (Alta 4 h hábiles · Normal 1 día hábil · Baja 3 días hábiles; atención lunes a viernes 9 a 18); 4. Reembolsos · 0,530; Portada · 0,525; 6. (2.ª parte) · 0,513",
         "\"Atendemos correos de lunes a viernes de 9 a 18 (hora Argentina); la primera respuesta depende de la prioridad: Alta 4 horas hábiles, Normal 1 día hábil y Baja 3 días hábiles…\" (Fuente: …, sección \"6. Niveles de prioridad y tiempos de respuesta\")",
         G + " Correcto (cita fuente)"],
        ["3", "\"¿hay versión para Mac o para el celular?\" (<i>Mac/celular</i> vs. macOS / iOS y Android en el manual)", "Ventas",
         "1.2 Plataformas confirmadas y no confirmadas · 0,466 (macOS: «No disponible, sin planes anunciados»; iOS/Android: «No disponible»); 1.1 Catálogo · 0,361",
         "\"Actualmente no hay versión para macOS ni para celulares; no hay planes anunciados…\" (Fuente: …, sección \"1.2 Plataformas confirmadas y no confirmadas\")",
         G + " Correcto (negativo confirmado por el manual)"],
        ["4", "\"¿cuánto sale la edición Deluxe y qué trae?\" (<i>sale/trae</i> = precio / contenido del bundle)", "Ventas",
         "7. Actualizaciones y DLC · 0,444; 11. Glosario · 0,418 (Edición Deluxe = bundle con juego base, banda sonora e «Islas del Norte»); 1.1 Catálogo vigente · 0,392 (22,99 USD); 8. Descuentos · 0,343 → descartado por Min Score",
         "\"La Edición Deluxe cuesta 22,99 USD e incluye el juego base, la banda sonora y la expansión «Islas del Norte»…\" (Fuente: …, sección \"1. Sobre Jumade y catálogo de productos › 1.1 Catálogo vigente\")",
         G + " Correcto (cruza 2 fragmentos y cita el del precio)"],
        ["5", "\"¿venden remeras o merchandising de Jumade?\" (tema <b>ausente</b> del manual: caso diseñado para la regla \"No sé\")", "Ventas",
         "8. Descuentos, bundles y promociones · 0,525; 1. Sobre Jumade y catálogo · 0,515; Portada · 0,506; 4. Reembolsos · 0,467 — todos pasan el umbral pero ninguno habla de merchandising",
         "\"No sé, no tengo ese dato confirmado. ¿Querés que lo consulte con el equipo y te confirme si vendemos remeras o merchandising de Jumade?\" (Fuente: …, sección \"Merchandising\")",
         Y + " Correcto en contenido (aplicó \"No sé\" y no inventó); falla menor: agregó una cita a una sección inexistente"]]
story += [tbl(rows, [CW * 0.025, CW * 0.19, CW * 0.085, CW * 0.26, CW * 0.29, CW * 0.15])]
story += [Spacer(1, 4),
          P("<b>Métrica de precisión: 5/5 respuestas correctas en contenido (100 %); 4/5 impecables en formato (80 %).</b> Ninguna respuesta afirmó algo que no "
            "estuviera en el manual; el único defecto fue una cita fabricada acompañando un \"No sé\" (caso 5). Recall de recuperación: en los 4 casos con respuesta en el "
            "manual, la sección correcta estuvo entre los K = 4 fragmentos (en el caso 4 en 3.ª posición, con 0,392: a 0,04 del umbral).", "body")]

story += [PageBreak(), P("Pieza 4 (cont.) · Análisis crítico, fallas encontradas y acciones correctivas", "h2")]
an = [["Hallazgo", "Qué pasó", "Causa raíz", "Acción correctiva (aplicada / pendiente)"],
      ["Falsos negativos en la 1.ª ronda (casos 3 y 4)",
       "En la primera batería el Worker de Ventas contestó \"No sé\" a Mac/celular y a la Deluxe, aunque la herramienta había recuperado 1.2 Plataformas (0,466) y 1.1 Catálogo (0,392).",
       "Bug de configuración, no de recuperación: el System Message de ambos Workers no empezaba con \"=\", así que n8n no evaluaba la expresión <font face='Mono'>{{ $json.contexto }}</font> y el modelo recibía el texto literal en lugar de los fragmentos.",
       "<b>Aplicada.</b> Se antepuso \"=\" a los System Messages; en la ronda final los dos casos pasaron a correctos con cita. Lección: validar siempre con la vista de ejecución que el prompt final contenga los fragmentos (rama Tool en verde + tokens de entrada &gt; 1.500)."],
      ["Cita inventada al responder \"No sé\" (caso 5)",
       "El agente aplicó bien la contención pero cerró con <i>(Fuente: …, sección \"Merchandising\")</i>, una sección que no existe.",
       "El prompt exigía citar \"siempre\" y el modelo resolvió la tensión fabricando la sección. Además, los 4 fragmentos superaron el umbral (0,47–0,53) por compartir vocabulario comercial (\"venden\", \"Jumade\"), así que la herramienta no devolvió SIN_RESULTADOS.",
       "<b>Aplicada.</b> Nueva regla: \"Cuando respondas 'No sé', no agregues ninguna cita de fuente\". <b>Pendiente de verificar</b> con una nueva corrida (la ronda final se quedó sin créditos de modelo en ese turno). Alternativa evaluada: subir Min Score a 0,45 no sirve, dejaría afuera los casos 3 y 4."],
      ["Puntajes bajos en aciertos legítimos (0,39–0,47)",
       "Las secciones en formato tabla (catálogo, plataformas) puntúan menos que las de prosa, aunque contienen la respuesta exacta.",
       "El embedding de una tabla Markdown diluye la señal semántica: muchas celdas cortas con nombres propios y números.",
       "<b>Pendiente (mejora para la entrega final).</b> Agregar a cada fila de tabla una oración en prosa (\"La Edición Deluxe cuesta 22,99 USD e incluye…\") antes de indexar, o duplicar esas filas como fragmentos cortos tipo FAQ."],
      ["Reformulación de la consulta por el agente (caso 2)",
       "El Worker de Soporte reescribió \"mandé un mail por un bug\" como \"tiempos de respuesta soporte por email … plazo\" y obtuvo 0,702 (vs. 0,574 con la consulta literal).",
       "La regla 0 del prompt (\"reformulá en términos del manual\") funciona como un query rewriting barato dentro del ciclo ReAct.",
       "Mantener. Es el motivo por el que el Worker de Soporte (Tools Agent) recupera mejor que el Worker de Ventas, que hoy pasa la consulta literal: <b>pendiente</b> migrar Ventas al mismo esquema de Tools Agent."],
      ["Consulta fuera de dominio (prueba extra)",
       "\"¿qué clima hace en Tandil?\" → mejor fragmento 0,315 &lt; 0,35 → SIN_RESULTADOS → \"No sé\" sin cita.",
       "El umbral cumple su función de contención para temas ajenos a la empresa.",
       "Ninguna. Se incorpora al set de regresión del plan de gobernanza."]]
story += [tbl(an, [CW * 0.15, CW * 0.27, CW * 0.29, CW * 0.29])]
story += [Spacer(1, 4), img(CAP + "07_exec_worker_soporte_208.png", height=78 * mm),
          P("Figura 5. Ejecución n.º 208 del Worker de Soporte (pregunta 2): la rama <b>Tool → buscar_manual_jumade</b> en verde (1 ítem), 2 llamadas al modelo (ReAct) y la salida final con la cita a la sección 6 del manual.", "cap")]

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
                                             "<font face='Mono'>version</font> y <font face='Mono'>vigencia</font>. 4) <b>Vaciar la colección e indexar de cero</b> (nunca mezclar versiones: un índice = una versión). "
                                             "5) Correr el set de regresión (las 5 preguntas ciegas + la consulta fuera de dominio) y exigir 5/5 con cita correcta. 6) Anotar en el CHANGELOG del repositorio: versión, fecha, responsable, cantidad de puntos y resultado del set."],
       ["Trazabilidad y control", "Cada fragmento lleva <font face='Mono'>documento</font>, <font face='Mono'>version</font>, <font face='Mono'>seccion</font> y <font face='Mono'>fuente</font>; toda respuesta del agente cita la sección, "
                                  "así que un error se rastrea al fragmento exacto. El log del Manager en Google Sheets permite auditar qué fragmentos se usaron en cada conversación. "
                                  "Si un jugador o el equipo reportan una respuesta incorrecta, se abre una revisión extraordinaria aunque no toque la fecha trimestral."],
       ["Qué NO se indexa", "Conversaciones de usuarios, datos personales, borradores internos, hojas de ruta no publicadas ni documentos de terceros sin permiso. La base de conocimiento es sólo documentación institucional aprobada y vigente."]]
story += [tbl(gov, [CW * 0.17, CW * 0.83])]
story += [Spacer(1, 4),
          P("Archivos en el repositorio <font face='Mono'>jumade-ai-automation-soporte/modulo5/</font>: manual fuente (PDF y Markdown limpio), <font face='Mono'>chunks_manual.json</font>, "
            "workflows exportados (<font face='Mono'>rag_tool_buscar_manual.json</font>, <font face='Mono'>rag_indexar_manual.json</font>, Workers actualizados), capturas y este PDF.", "small")]

doc = BaseDocTemplate(OUT, pagesize=PAGE, leftMargin=M, rightMargin=M, topMargin=10 * mm, bottomMargin=14 * mm,
                      title="Pre-entrega Módulo 5 — Agente con conocimiento organizacional (JUMA)", author="Juan Manuel Depaoli")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(M, 14 * mm, CW, H - 24 * mm, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=footer)])
doc.build(story)
print("OK", OUT)
