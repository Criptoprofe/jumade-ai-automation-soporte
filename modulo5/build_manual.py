# -*- coding: utf-8 -*-
"""Genera el documento maestro institucional de Jumade:
Manual_Soporte_y_Ventas_Jumade_v2.pdf (A4 vertical, títulos jerárquicos y tablas reales)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Inter", "/tmp/fonts/Inter.ttf"))
pdfmetrics.registerFont(TTFont("Inter-I", "/tmp/fonts/Inter-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

OUT = "/home/user/workspace/jumade-ai-automation/modulo5/Manual_Soporte_y_Ventas_Jumade_v2.pdf"
TEAL = colors.HexColor("#01696F"); TEXT = colors.HexColor("#28251D"); LINE = colors.HexColor("#C9C7C0")
HEAD = colors.HexColor("#01696F"); ALT = colors.HexColor("#F3F2EE")
W, H = A4; M = 18 * mm; CW = W - 2 * M

S = dict(
    title=ParagraphStyle("t", fontName="DejaVu-B", fontSize=22, leading=27, textColor=TEAL, spaceAfter=6),
    sub=ParagraphStyle("s", fontName="Inter", fontSize=11, leading=15, textColor=TEXT, spaceAfter=14),
    h1=ParagraphStyle("h1", fontName="DejaVu-B", fontSize=15, leading=19, textColor=TEAL, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    h2=ParagraphStyle("h2", fontName="DejaVu-B", fontSize=11.5, leading=15, textColor=TEXT, spaceBefore=9, spaceAfter=4, keepWithNext=1),
    body=ParagraphStyle("b", fontName="Inter", fontSize=9.6, leading=13.5, textColor=TEXT, spaceAfter=5),
    bullet=ParagraphStyle("bl", fontName="Inter", fontSize=9.6, leading=13.5, textColor=TEXT, leftIndent=12, bulletIndent=2, spaceAfter=2),
    cell=ParagraphStyle("c", fontName="Inter", fontSize=8.6, leading=11.5, textColor=TEXT),
    cellh=ParagraphStyle("ch", fontName="DejaVu-B", fontSize=8.6, leading=11.5, textColor=colors.white),
    note=ParagraphStyle("n", fontName="Inter-I", fontSize=8.6, leading=12, textColor=colors.HexColor("#5A5953"), spaceAfter=6),
)
def P(t, s="body"): return Paragraph(t, S[s])
def B(t): return Paragraph(t, S["bullet"], bulletText="•")
def T(rows, widths):
    data = [[Paragraph(c, S["cellh"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), HEAD), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for i in range(2, len(rows), 2): st.append(("BACKGROUND", (0, i), (-1, i), ALT))
    t.setStyle(TableStyle(st)); return t

def footer(c, d):
    c.saveState(); c.setFont("Inter", 7.5); c.setFillColor(colors.HexColor("#7A7974"))
    c.drawString(M, 11 * mm, "Jumade · Manual de Soporte y Ventas · v2.1 · octubre 2026")
    c.drawRightString(W - M, 11 * mm, f"Página {d.page}"); c.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=16 * mm, bottomMargin=18 * mm,
                        title="Manual de Soporte y Ventas de Jumade v2.1", author="Jumade")
F = []
F += [P("Manual de Soporte y Ventas de Jumade", "title"),
      P("Versión 2.1 · Vigente desde el 1 de octubre de 2026 · Responsable: Juan Manuel Depaoli (fundador) · Próxima revisión: 1 de enero de 2027", "sub")]
F += [P("Este manual es la única fuente oficial de información para responder consultas de jugadores, tiendas, prensa y colaboradores. "
        "Lo usa el equipo humano y el asistente de IA JUMA. Si una situación no está contemplada acá, la respuesta correcta es "
        "no inventar: derivar el caso a una persona del equipo.")]

# 1
F += [P("1. Sobre Jumade y catálogo de productos", "h1"),
      P("Jumade es un estudio independiente de videojuegos con base en Tandil, provincia de Buenos Aires, Argentina. Desarrolla juegos 2D de acción, "
        "plataformas y estrategia liviana para PC y consolas. Vende de forma directa en su web y a través de tiendas digitales."),
      P("1.1 Catálogo vigente", "h2"),
      T([["Producto", "Género", "Plataformas disponibles", "Precio de lista (USD)", "Estado"],
         ["Jumade (juego base)", "Acción y plataformas 2D", "PC (Steam, itch.io, web de Jumade) · Nintendo Switch", "14,99", "Lanzado el 12 de marzo de 2026"],
         ["Jumade – Banda sonora original", "DLC de audio (24 pistas, MP3 y FLAC)", "Steam · web de Jumade", "4,99", "Lanzado"],
         ["Jumade – Expansión «Islas del Norte»", "DLC de contenido (6 niveles nuevos, 2 jefes)", "PC (Steam, itch.io, web) · Nintendo Switch", "6,99", "Lanzado el 20 de agosto de 2026"],
         ["Jumade – Edición Deluxe (juego + los 2 DLC)", "Bundle", "Steam · web de Jumade", "22,99 (ahorro del 14 % frente a comprar por separado)", "Disponible"],
         ["Pela Rush (juego anterior, marca Pela Games)", "Arcade", "itch.io", "Gratis", "Sin soporte activo"]],
        [CW * 0.24, CW * 0.17, CW * 0.27, CW * 0.17, CW * 0.15]),
      P("Los precios en pesos argentinos y en otras monedas regionales los fija cada tienda según su propia conversión; el equipo no puede "
        "confirmar un precio regional exacto, siempre se remite a la página de la tienda.", "note"),
      P("1.2 Plataformas confirmadas y no confirmadas", "h2"),
      T([["Plataforma", "Situación oficial", "Qué se le puede decir al jugador"],
         ["PC con Windows 10 u 11 (64 bits)", "Disponible", "Compra en Steam, itch.io o la web de Jumade."],
         ["PC con Linux (SteamOS / Steam Deck)", "Disponible vía Proton, verificado en Steam Deck", "Funciona en Steam Deck con la calificación «Verificado»."],
         ["Nintendo Switch", "Disponible en la eShop de América y Europa", "Compra directa en la eShop; las claves de Switch no las vende Jumade."],
         ["PlayStation 5 y Xbox Series", "En evaluación, sin fecha ni precio confirmados", "No se puede prometer fecha ni precio. Ofrecer suscripción al boletín para avisar."],
         ["macOS", "No disponible, sin planes anunciados", "Informar que no hay versión para Mac."],
         ["Celulares (Android / iOS)", "No disponible, sin planes anunciados", "Informar que no hay versión móvil."]],
        [CW * 0.28, CW * 0.32, CW * 0.40])]

# 2
F += [P("2. Requisitos del sistema (PC)", "h1"),
      T([["Componente", "Mínimo", "Recomendado"],
         ["Sistema operativo", "Windows 10 de 64 bits", "Windows 11 de 64 bits"],
         ["Procesador", "Intel Core i3-6100 o AMD FX-6300", "Intel Core i5-8400 o AMD Ryzen 5 2600"],
         ["Memoria RAM", "4 GB", "8 GB"],
         ["Placa de video", "Intel UHD 620 o cualquier GPU con 1 GB de VRAM y soporte DirectX 11", "NVIDIA GTX 1050 o AMD RX 560 (2 GB)"],
         ["Espacio en disco", "1,8 GB", "2,5 GB (juego base + los dos DLC)"],
         ["Otros", "DirectX 11, resolución mínima 1280×720", "Control (gamepad) compatible con XInput, pantalla 1080p a 60 Hz"]],
        [CW * 0.22, CW * 0.39, CW * 0.39]),
      P("El juego no requiere conexión a internet para jugar: la conexión solo se usa para descargar actualizaciones y sincronizar logros en Steam.")]

# 3
F += [P("3. Compra, claves de activación y cuentas", "h1"),
      P("3.1 Dónde se compra y cómo se activa", "h2"),
      T([["Canal de compra", "Qué recibe el jugador", "Cómo se activa"],
         ["Steam", "El juego queda en la biblioteca de Steam", "No hace falta clave: aparece en Biblioteca → Instalar."],
         ["itch.io", "Descarga directa (instalador .exe o .zip) y, opcionalmente, una clave de Steam", "Descargar desde la página de compra de itch.io; la clave de Steam se canjea en Steam → Juegos → Activar un producto."],
         ["Web de Jumade (jumade.games/tienda)", "Correo con una clave de Steam de 15 caracteres (formato XXXXX-XXXXX-XXXXX)", "Canjear en Steam → Juegos → Activar un producto en Steam. La clave llega en menos de 10 minutos."],
         ["Nintendo eShop", "El juego queda asociado a la cuenta Nintendo", "Descarga automática en la consola."]],
        [CW * 0.24, CW * 0.36, CW * 0.40]),
      P("3.2 Problemas frecuentes con claves", "h2"),
      T([["Situación", "Qué revisar", "Resolución"],
         ["La clave no llegó por correo", "Carpeta de spam o promociones; que el pago figure como aprobado", "Si pasaron más de 30 minutos y el pago está aprobado, el equipo reenvía la clave a la misma dirección de compra. Nunca a otra dirección."],
         ["La clave dice «ya utilizada»", "Que no se haya canjeado en otra cuenta de Steam del jugador", "Pedir el número de pedido y la captura del error; el equipo verifica en el panel de Steamworks y, si corresponde, emite una clave nueva (plazo: 2 días hábiles)."],
         ["La clave dice «inválida» o «no reconocida»", "Errores de tipeo: 0 por O, 1 por I", "Pedir que la copie y pegue; si persiste, mismo procedimiento que la clave usada."],
         ["Compró en la web y quiere la versión de Switch", "—", "No es posible: la web solo vende claves de Steam. No se hacen cambios de plataforma."]],
        [CW * 0.26, CW * 0.30, CW * 0.44]),
      P("Por seguridad, el equipo nunca pide datos completos de la tarjeta ni contraseñas. Solo se piden el número de pedido, el correo de compra y, si hace falta, una captura de pantalla del error.", "note")]

# 4
F += [P("4. Política de reembolsos y cancelaciones", "h1"),
      P("Los reembolsos los procesa la tienda donde se hizo la compra. Jumade solo gestiona directamente las compras hechas en su propia web."),
      T([["Tienda", "Plazo para pedir el reembolso", "Condición", "Quién lo procesa y cuánto tarda"],
         ["Steam", "Hasta 14 días desde la compra", "Menos de 2 horas de juego registradas", "Steam, desde help.steampowered.com. Acreditación en 7 días."],
         ["itch.io", "Hasta 7 días desde la compra", "Falla técnica no resuelta por soporte", "Jumade aprueba el pedido y itch.io devuelve el dinero. Plazo de 5 a 10 días hábiles."],
         ["Web de Jumade", "Hasta 7 días desde la compra", "La clave de Steam no debe haber sido canjeada", "Jumade, por el mismo medio de pago. Plazo de 10 días hábiles."],
         ["Nintendo eShop", "No admite reembolsos", "—", "Nintendo no procesa devoluciones de contenido digital, salvo casos excepcionales definidos por Nintendo."]],
        [CW * 0.16, CW * 0.22, CW * 0.28, CW * 0.34]),
      P("4.1 Reglas que el equipo y JUMA deben respetar", "h2"),
      B("Nunca se promete un reembolso por chat o correo. Se explica la política, se registra el caso y una persona del equipo lo confirma."),
      B("Un cobro duplicado se reintegra siempre, sin importar el plazo, contra el comprobante del banco o de la tienda."),
      B("Los DLC comprados en la web siguen la misma regla que el juego base: 7 días y clave sin canjear."),
      B("El arrepentimiento de compra (sin falla técnica) en la web de Jumade se acepta dentro de los 7 días si la clave no fue canjeada; fuera de ese plazo no corresponde reembolso."),
      B("Si el jugador menciona contracargo (chargeback), estafa, abogado o denuncia, el caso pasa directamente a una persona del equipo con prioridad Alta.")]

# 5
F += [P("5. Soporte técnico: problemas frecuentes", "h1"),
      P("5.1 Guía de diagnóstico por síntoma", "h2"),
      T([["Síntoma", "Causa más frecuente", "Pasos en orden"],
         ["El juego se cierra al iniciar (muestra el logo y vuelve al escritorio)", "Driver de video desactualizado o overlay de terceros", "1) Actualizar el driver de la placa de video. 2) Desactivar los overlays de Steam, Discord y GeForce Experience. 3) Verificar la integridad de los archivos en Steam. 4) Ejecutar como administrador. 5) Si persiste, enviar el archivo de registro (ver 5.2)."],
         ["Pantalla negra con sonido", "Resolución guardada no compatible con el monitor", "Borrar el archivo settings.json de la carpeta de guardado (ver 5.2) para que el juego vuelva a 1280×720 en ventana."],
         ["Bajo rendimiento o tirones (menos de 30 FPS)", "Sincronización vertical o uso de la GPU integrada", "1) Desactivar VSync en Opciones → Video. 2) Forzar la GPU dedicada en el panel de NVIDIA o AMD. 3) Bajar la escala de resolución a 80 %."],
         ["El control (gamepad) no responde", "Steam Input desactivado o control no XInput", "Activar Steam Input para el juego en Propiedades → Controlador. Los controles de PlayStation funcionan solo a través de Steam Input."],
         ["Se perdió la partida guardada", "Steam Cloud desactivado o cambio de PC", "Revisar Steam → Configuración → Nube. Las partidas locales están en la carpeta de guardado (ver 5.2). Jumade no puede recuperar partidas que no estén en la nube."],
         ["No aparece el DLC «Islas del Norte» dentro del juego", "DLC no instalado en Steam", "Biblioteca → Jumade → Propiedades → DLC → marcar la casilla y reiniciar el juego. Las islas aparecen en el mapa después del nivel 2-4."],
         ["Texto en inglés aunque el sistema está en español", "Idioma de Steam distinto del idioma del sistema", "Propiedades → Idioma → Español (Latinoamérica). El juego incluye textos en español, inglés y portugués; no tiene doblaje de voces."]],
        [CW * 0.26, CW * 0.24, CW * 0.50]),
      P("5.2 Rutas de archivos útiles", "h2"),
      T([["Sistema", "Carpeta de guardado y configuración", "Archivo de registro (log)"],
         ["Windows", "%USERPROFILE%\\AppData\\LocalLow\\Jumade\\Jumade\\", "%USERPROFILE%\\AppData\\LocalLow\\Jumade\\Jumade\\Player.log"],
         ["Linux / Steam Deck", "~/.config/unity3d/Jumade/Jumade/", "~/.config/unity3d/Jumade/Jumade/Player.log"]],
        [CW * 0.2, CW * 0.42, CW * 0.38]),
      P("Para abrir un caso de soporte técnico el equipo pide: sistema operativo, placa de video, tienda de compra, descripción del problema y el archivo Player.log adjunto.")]

# 6
F += [P("6. Niveles de prioridad y tiempos de respuesta", "h1"),
      P("Soporte se atiende por correo (soporte@jumade.games), por el chat de la web y por Telegram, de lunes a viernes de 9 a 18 h (hora de Argentina). Fuera de ese horario el asistente JUMA responde de forma automática con la información de este manual y deja el caso registrado."),
      T([["Prioridad", "Cuándo se asigna", "Primera respuesta", "Resolución objetivo"],
         ["Alta", "Cobros duplicados, claves no entregadas con pago aprobado, menciones de contracargo o reclamo legal, prensa con fecha de publicación", "4 horas hábiles", "2 días hábiles"],
         ["Normal", "Problemas técnicos que impiden jugar, claves inválidas, consultas de preventa con intención de compra", "1 día hábil", "5 días hábiles"],
         ["Baja", "Sugerencias, pedidos de funcionalidades, consultas generales, bugs menores sin bloqueo", "3 días hábiles", "Sin plazo comprometido; se revisa en la planificación mensual"]],
        [CW * 0.12, CW * 0.48, CW * 0.18, CW * 0.22]),
      P("Todos los casos quedan registrados con fecha, canal, intención, prioridad y estado (Abierto, En espera, Escalado o Resuelto).")]

# 7
F += [P("7. Actualizaciones, DLC y hoja de ruta pública", "h1"),
      T([["Versión", "Fecha", "Contenido principal"],
         ["1.0", "12 de marzo de 2026", "Lanzamiento en PC y Nintendo Switch."],
         ["1.1", "30 de abril de 2026", "Modo asistido (dificultad reducida), corrección de 40 errores, soporte para Steam Deck."],
         ["1.2", "20 de agosto de 2026", "Expansión «Islas del Norte», nuevo jefe final opcional, textos en portugués."],
         ["1.3 (planificada)", "Primer trimestre de 2027", "Modo contrarreloj y tablas de clasificación en línea. Fecha no comprometida."]],
        [CW * 0.18, CW * 0.24, CW * 0.58]),
      B("Las actualizaciones son gratuitas para quienes tienen el juego base. Los DLC se venden por separado o en la Edición Deluxe."),
      B("No se anuncian fechas de lanzamiento que no figuren en esta tabla. Para la versión 1.3 solo se puede decir «primer trimestre de 2027, sin fecha confirmada»."),
      B("No está prevista una versión física en cartucho o disco.")]

# 8
F += [P("8. Descuentos, bundles y promociones", "h1"),
      P("Jumade no otorga descuentos individuales ni códigos de descuento a pedido. Las rebajas se publican únicamente durante los eventos de cada tienda."),
      T([["Evento", "Período aproximado", "Descuento sobre el juego base", "Descuento sobre los DLC"],
         ["Rebajas de verano de Steam", "Fines de junio a principios de julio", "25 %", "15 %"],
         ["Rebajas de otoño de Steam", "Fines de noviembre", "30 %", "20 %"],
         ["Rebajas de invierno de Steam", "Fines de diciembre a principios de enero", "35 %", "25 %"],
         ["Aniversario de Jumade (web propia)", "Del 12 al 19 de marzo", "40 %", "30 %"],
         ["Promociones de la eShop de Nintendo", "Las define Nintendo", "Hasta 30 %", "Hasta 20 %"]],
        [CW * 0.30, CW * 0.28, CW * 0.21, CW * 0.21]),
      B("Descuento educativo: escuelas y universidades pueden pedir licencias con 50 % de descuento escribiendo a hola@jumade.games con un correo institucional (mínimo 10 licencias)."),
      B("Compras al por mayor para empresas o eventos: se cotizan caso por caso; no hay lista de precios publicada.")]

# 9
F += [P("9. Prensa, creadores de contenido y colaboraciones", "h1"),
      P("9.1 Claves de prensa y de creadores", "h2"),
      T([["Perfil", "Requisito mínimo", "Qué se entrega", "Plazo de respuesta"],
         ["Medio de prensa o sitio especializado", "Correo institucional del medio y enlace a 3 notas publicadas", "Clave de Steam del juego base y de la expansión, kit de prensa con capturas y logos", "3 días hábiles"],
         ["Streamer o youtuber", "Al menos 1.000 seguidores o suscriptores y actividad en los últimos 30 días", "Clave de Steam del juego base", "5 días hábiles"],
         ["Podcast o newsletter", "Enlace a episodios o ediciones anteriores", "Entrevista con el fundador y material gráfico", "5 días hábiles"]],
        [CW * 0.22, CW * 0.30, CW * 0.30, CW * 0.18]),
      B("Las claves de prensa se piden exclusivamente desde el formulario de jumade.games/prensa o por correo a prensa@jumade.games. No se entregan claves por mensaje directo en redes."),
      B("El contenido en video del juego se puede monetizar libremente en YouTube y Twitch; la banda sonora original está libre de reclamos de derechos (Content ID)."),
      P("9.2 Publishers, portings y acuerdos comerciales", "h2"),
      P("Las propuestas de publishing, porting a otras consolas, localización o distribución física se derivan siempre al fundador. El equipo de soporte solo registra el contacto y la propuesta; no negocia condiciones ni comparte cifras de ventas.")]

# 10
F += [P("10. Privacidad y datos de los jugadores", "h1"),
      B("El juego no recopila datos personales. Steam y Nintendo gestionan las cuentas y los pagos con sus propias políticas."),
      B("La web de Jumade guarda el correo de compra y el número de pedido durante 5 años por razones fiscales. El jugador puede pedir la eliminación de sus datos de marketing escribiendo a privacidad@jumade.games; se procesa en 15 días hábiles."),
      B("El boletín de novedades se envía como máximo 2 veces por mes y cada envío incluye un enlace para darse de baja."),
      B("El asistente JUMA registra las conversaciones de soporte para dar seguimiento a los casos; esos registros se conservan 12 meses.")]

# 11
F += [P("11. Glosario", "h1"),
      T([["Término", "Significado en este manual"],
         ["Clave de Steam", "Código de 15 caracteres que agrega el juego a una cuenta de Steam."],
         ["DLC", "Contenido descargable adicional que se compra por separado del juego base."],
         ["Edición Deluxe", "Bundle con el juego base, la banda sonora y la expansión «Islas del Norte»."],
         ["Steam Input", "Sistema de Steam que traduce cualquier control a un control compatible con el juego."],
         ["Player.log", "Archivo de registro que el juego genera en cada ejecución; sirve para diagnosticar errores."],
         ["Caso", "Registro de una consulta con fecha, canal, intención, prioridad y estado."],
         ["Escalar", "Pasar una consulta del asistente automático a una persona del equipo."]],
        [CW * 0.25, CW * 0.75])]

F += [Spacer(1, 10), P("Fin del documento. Cualquier información que no figure en este manual debe tratarse como no confirmada.", "note")]

doc.build(F, onFirstPage=footer, onLaterPages=footer)
print("OK", OUT)
