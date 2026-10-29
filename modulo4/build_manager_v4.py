# -*- coding: utf-8 -*-
"""Construye el Manager v4 (Módulo 4) a partir del Manager v3 (Módulo 3).

Agrega:
- Entrada por casilla de soporte (Gmail Trigger) con IF anti auto-reply.
- Look up de contacto en HubSpot antes del Create (evita duplicados / Error 409).
- Entrada normalizada común para chat y email.
- Salida por email exclusivamente como Create Draft (Human-in-the-loop).
- Set de limpieza de payload antes de Slack (canal #operaciones-jumade).
- Alerta a supervisor humano migrada de Gmail Send a Slack (con Set de limpieza).
"""
import json, uuid, copy

SRC = "/home/user/workspace/jumade-ai-automation/modulo3/manager.json"
OUT = "/home/user/workspace/jumade-ai-automation/modulo4/checkpoint4_juan_manuel_depaoli.json"

HUB_CRED = {"id": "0zzbdHHTbTDVUDp3", "name": "HubSpot CRM Jumade (OAuth2)"}
SLACK_CRED = {"id": "eYNRqCfXDbzzrGc8", "name": "Slack Operaciones Jumade (OAuth2)"}
GMAIL_CRED = {"id": "UDNPuSr4w91CsZ0b", "name": "Gmail account"}
SLACK_CHANNEL = "C0CDCCHT1C1"  # #operaciones-jumade

nid = lambda: str(uuid.uuid4())

wf = json.load(open(SRC))
raw = json.dumps(wf, ensure_ascii=False)
# Todas las referencias al Chat Trigger pasan por la entrada normalizada (sirve para chat y email)
raw = raw.replace("$('Chat Trigger')", "$('Entrada normalizada')")
wf = json.loads(raw)
nodes = {n["name"]: n for n in wf["nodes"]}
conn = wf["connections"]

def set_node(name, pos, assignments, include_other=False):
    return {"id": nid(), "name": name, "type": "n8n-nodes-base.set", "typeVersion": 3.4, "position": pos,
            "parameters": {"assignments": {"assignments": [
                {"id": nid(), "name": k, "value": v, "type": t} for k, v, t in assignments]},
                "includeOtherFields": include_other, "options": {}}}

def if_node(name, pos, conditions, combinator="and", loose=True):
    return {"id": nid(), "name": name, "type": "n8n-nodes-base.if", "typeVersion": 2.2, "position": pos,
            "parameters": {"conditions": {"options": {"caseSensitive": False, "leftValue": "", "typeValidation": "loose", "version": 2},
                                          "conditions": conditions, "combinator": combinator},
                           "looseTypeValidation": loose, "options": {}}}

def cond(left, op_type, op, right=None, single=False):
    c = {"id": nid(), "leftValue": left, "rightValue": right if right is not None else "", "operator": {"type": op_type, "operation": op}}
    if single: c["operator"]["singleValue"] = True
    return c

# ---------------------------------------------------------------- reposicionar
nodes["Chat Trigger"]["position"] = [-260, 200]
for n in wf["nodes"]:
    if n["position"][0] >= 3160:
        n["position"][0] += 1000

# ---------------------------------------------------------------- entrada por email
gmail_trigger = {"id": nid(), "name": "Casilla de soporte (Gmail Trigger)", "type": "n8n-nodes-base.gmailTrigger", "typeVersion": 1.4,
                 "position": [-1820, -300],
                 "parameters": {"pollTimes": {"item": [{"mode": "everyMinute"}]}, "simple": False, "maxResults": 10,
                                "filters": {"readStatus": "unread", "labelIds": ["INBOX"]}, "options": {}},
                 "credentials": {"gmailOAuth2": GMAIL_CRED}}

AUTO_SUBJECT = r"(auto[\s-]?reply|automatic reply|respuesta automática|out of office|fuera de (la )?oficina|undeliverable|delivery status notification|mail delivery (failed|subsystem)|no se pudo entregar|no-?reply)"
AUTO_SENDER = r"^(no-?reply|noreply|do-?not-?reply|mailer-daemon|postmaster|bounce|notifications?)@"
if_auto = if_node("¿Es correo automático?", [-1580, -300], [
    cond("={{ $json.subject || '' }}", "string", "regex", "=/" + AUTO_SUBJECT + "/i"),
    cond("={{ ($json.from && $json.from.value && $json.from.value[0] ? $json.from.value[0].address : '') }}", "string", "regex", "=/" + AUTO_SENDER + "/i"),
    cond("={{ String($json.headers && $json.headers['auto-submitted'] || 'no') }}", "string", "notEquals", "no"),
    cond("={{ String($json.headers && ($json.headers['x-autoreply'] || $json.headers['x-autorespond']) || '') }}", "string", "notEmpty", single=True),
    cond("={{ String($json.headers && $json.headers['precedence'] || '') }}", "string", "regex", "=/^(bulk|auto_reply|list|junk)$/i"),
], combinator="or")

descartar = {"id": nid(), "name": "Descartar correo automático (corta el bucle)", "type": "n8n-nodes-base.noOp", "typeVersion": 1,
             "position": [-1340, -520], "parameters": {}}

hub_search = {"id": nid(), "name": "Buscar contacto en CRM (Look up)", "type": "n8n-nodes-base.hubspot", "typeVersion": 2.2,
              "position": [-1340, -300], "alwaysOutputData": True,
              "parameters": {"authentication": "oAuth2", "resource": "contact", "operation": "search", "returnAll": False, "limit": 1,
                             "filterGroupsUi": {"filterGroupsValues": [{"filtersUi": {"filterValues": [
                                 {"propertyName": "email|string", "type": "string", "operator": "EQ",
                                  "value": "={{ ($json.from.value[0].address || '').toLowerCase().trim() }}"}]}}]},
                             "additionalFields": {"properties": ["email", "firstname", "lastname", "lifecyclestage"]}},
              "credentials": {"hubspotOAuth2Api": HUB_CRED}}

if_exists = if_node("¿Contacto existe en CRM?", [-1100, -300], [cond("={{ $json.id }}", "string", "notEmpty", single=True)])

hub_create = {"id": nid(), "name": "Crear contacto en CRM (Create)", "type": "n8n-nodes-base.hubspot", "typeVersion": 2.2,
              "position": [-860, -120],
              "parameters": {"authentication": "oAuth2", "resource": "contact", "operation": "upsert",
                             "email": "={{ ($('Casilla de soporte (Gmail Trigger)').item.json.from.value[0].address || '').toLowerCase().trim() }}",
                             "additionalFields": {
                                 "firstName": "={{ (($('Casilla de soporte (Gmail Trigger)').item.json.from.value[0].name || '').split(' ')[0]) || '' }}",
                                 "lastName": "={{ (($('Casilla de soporte (Gmail Trigger)').item.json.from.value[0].name || '').split(' ').slice(1).join(' ')) || '' }}",
                                 "lifeCycleStage": "lead"},
                             "options": {"resolveData": True}},
              "credentials": {"hubspotOAuth2Api": HUB_CRED}}

norm_email = set_node("Normalizar entrada de email", [-620, -300], [
    ("sessionId", "={{ 'email-' + ($('Casilla de soporte (Gmail Trigger)').item.json.from.value[0].address || 'desconocido').toLowerCase().trim() }}", "string"),
    ("chatInput", "={{ 'Asunto: ' + ($('Casilla de soporte (Gmail Trigger)').item.json.subject || '(sin asunto)') + '\\n\\n' + String($('Casilla de soporte (Gmail Trigger)').item.json.text || $('Casilla de soporte (Gmail Trigger)').item.json.snippet || '').replace(/\\r/g,'').trim().slice(0, 4000) }}", "string"),
    ("canal", "email", "string"),
    ("email_from", "={{ ($('Casilla de soporte (Gmail Trigger)').item.json.from.value[0].address || '').toLowerCase().trim() }}", "string"),
    ("email_nombre", "={{ $('Casilla de soporte (Gmail Trigger)').item.json.from.value[0].name || '' }}", "string"),
    ("email_subject", "={{ $('Casilla de soporte (Gmail Trigger)').item.json.subject || '(sin asunto)' }}", "string"),
    ("email_threadId", "={{ $('Casilla de soporte (Gmail Trigger)').item.json.threadId }}", "string"),
    ("email_messageId", "={{ $('Casilla de soporte (Gmail Trigger)').item.json.id }}", "string"),
    ("crm_contact_id", "={{ String($json.id ?? $json.vid ?? '') }}", "string"),
    ("crm_contacto_nuevo", "={{ !$('¿Contacto existe en CRM?').item.json.id }}", "boolean"),
])

entrada = set_node("Entrada normalizada", [0, 0], [
    ("sessionId", "={{ $json.sessionId }}", "string"),
    ("chatInput", "={{ $json.chatInput }}", "string"),
    ("canal", "={{ $json.canal || 'chat' }}", "string"),
    ("email_from", "={{ $json.email_from || '' }}", "string"),
    ("email_nombre", "={{ $json.email_nombre || '' }}", "string"),
    ("email_subject", "={{ $json.email_subject || '' }}", "string"),
    ("email_threadId", "={{ $json.email_threadId || '' }}", "string"),
    ("email_messageId", "={{ $json.email_messageId || '' }}", "string"),
    ("crm_contact_id", "={{ $json.crm_contact_id || '' }}", "string"),
    ("crm_contacto_nuevo", "={{ $json.crm_contacto_nuevo === true }}", "boolean"),
])

# Canal real en el log
nodes["Log de trazabilidad (Sheets)"]["parameters"]["columns"]["value"]["Canal"] = "={{ $('Entrada normalizada').item.json.canal }}"

# ---------------------------------------------------------------- alerta a supervisor: Gmail Send -> Slack
alerta_old = nodes.pop("Alerta a supervisor humano")
wf["nodes"] = [n for n in wf["nodes"] if n["name"] != "Alerta a supervisor humano"]
limp_alerta = set_node("Limpieza de alerta (Slack)", [2372, 300], [
    ("traceId", "={{ $('Limpieza de payload').item.json.traceId }}", "string"),
    ("session_id", "={{ $('Limpieza de payload').item.json.session_id }}", "string"),
    ("canal", "={{ $('Entrada normalizada').item.json.canal }}", "string"),
    ("intencion", "={{ $('Limpieza de payload').item.json.intencion }}", "string"),
    ("motivo", "={{ String($('Limpieza de payload').item.json.motivo || '').replace(/\\s+/g,' ').slice(0, 200) }}", "string"),
    ("mensaje", "={{ String($('Limpieza de payload').item.json.mensaje || '').replace(/<[^>]*>/g,'').replace(/\\s+/g,' ').slice(0, 300) }}", "string"),
    ("error_worker", "={{ $json.status && $json.status !== 'success' ? String($json.error || $json.message || 'error en Worker').slice(0, 200) : '' }}", "string"),
])
alerta_slack = {"id": nid(), "name": "Alerta a supervisor humano (Slack)", "type": "n8n-nodes-base.slack", "typeVersion": 2.3,
                "position": [2600, 300],
                "parameters": {"authentication": "oAuth2", "resource": "message", "operation": "post", "select": "channel",
                               "channelId": {"__rl": True, "mode": "id", "value": SLACK_CHANNEL},
                               "messageType": "text",
                               "text": "=:rotating_light: *JUMA · Caso escalado a supervisor humano* · `{{ $json.traceId }}`\n*Canal:* {{ $json.canal }} · *Intención:* {{ $json.intencion }}\n*Motivo:* {{ $json.motivo }}{{ $json.error_worker ? '\\n*Error del Worker:* ' + $json.error_worker : '' }}\n*Mensaje del usuario:* {{ $json.mensaje }}\n_Session_ID: {{ $json.session_id }}_",
                               "otherOptions": {"includeLinkToWorkflow": False}},
                "credentials": {"slackOAuth2Api": SLACK_CRED}}
nodes["Respuesta fallback"]["position"] = [2830, 300]

# ---------------------------------------------------------------- salida por email: Draft + Slack
if_email = if_node("¿Llegó por email?", [3160, 0], [cond("={{ $('Entrada normalizada').item.json.canal }}", "string", "equals", "email")])

limp_salida = set_node("Limpieza de payload de salida", [3400, -400], [
    ("traceId", "={{ $('Limpieza de payload').item.json.traceId }}", "string"),
    ("canal", "email", "string"),
    ("intencion", "={{ $('Limpieza de payload').item.json.intencion }}", "string"),
    ("estado", "={{ $json.Estado }}", "string"),
    ("worker", "={{ $json.Worker_invocado }}", "string"),
    ("destinatario", "={{ $('Entrada normalizada').item.json.email_from }}", "string"),
    ("nombre", "={{ $('Entrada normalizada').item.json.email_nombre || 'cliente' }}", "string"),
    ("asunto_original", "={{ String($('Entrada normalizada').item.json.email_subject || '').replace(/\\s+/g,' ').slice(0, 120) }}", "string"),
    ("asunto_respuesta", "={{ (/^re:/i.test($('Entrada normalizada').item.json.email_subject || '') ? '' : 'Re: ') + String($('Entrada normalizada').item.json.email_subject || 'Tu consulta a Jumade').slice(0, 120) }}", "string"),
    ("respuesta", "={{ (()=>{ let r=''; try { r = JSON.parse($json.Respuesta_worker || '{}').respuesta || ''; } catch(e) { r=''; } r = String(r).replace(/<[^>]*>/g,'').trim(); return (r || 'Gracias por escribir a Jumade. Tu consulta quedó registrada y una persona del equipo te va a responder a la brevedad.').slice(0, 3000); })() }}", "string"),
    ("resumen_slack", "={{ String($('Entrada normalizada').item.json.chatInput || '').replace(/<[^>]*>/g,'').replace(/\\s+/g,' ').slice(0, 220) }}", "string"),
    ("threadId", "={{ $('Entrada normalizada').item.json.email_threadId }}", "string"),
    ("crm_contact_id", "={{ $('Entrada normalizada').item.json.crm_contact_id }}", "string"),
    ("crm_contacto_nuevo", "={{ $('Entrada normalizada').item.json.crm_contacto_nuevo }}", "boolean"),
])

draft = {"id": nid(), "name": "Borrador de respuesta (Create Draft)", "type": "n8n-nodes-base.gmail", "typeVersion": 2.1,
         "position": [3640, -400],
         "parameters": {"resource": "draft", "operation": "create",
                        "subject": "={{ $json.asunto_respuesta }}",
                        "emailType": "text",
                        "message": "={{ $json.respuesta }}\n\nSaludos,\nEquipo de Soporte y Ventas de Jumade\n\n---\nBorrador generado por JUMA (asistente IA). Una persona del equipo lo revisa antes de enviarlo.\ntraceId: {{ $json.traceId }}",
                        "options": {"sendTo": "={{ $json.destinatario }}", "threadId": "={{ $json.threadId }}"}},
         "credentials": {"gmailOAuth2": GMAIL_CRED}}

slack_aviso = {"id": nid(), "name": "Aviso al canal de operaciones (Slack)", "type": "n8n-nodes-base.slack", "typeVersion": 2.3,
               "position": [3880, -400],
               "parameters": {"authentication": "oAuth2", "resource": "message", "operation": "post", "select": "channel",
                              "channelId": {"__rl": True, "mode": "id", "value": SLACK_CHANNEL},
                              "messageType": "text",
                              "text": "=:incoming_envelope: *JUMA · Nuevo caso por email* · `{{ $('Limpieza de payload de salida').item.json.traceId }}`\n*De:* {{ $('Limpieza de payload de salida').item.json.nombre }} <{{ $('Limpieza de payload de salida').item.json.destinatario }}> · *CRM:* contacto #{{ $('Limpieza de payload de salida').item.json.crm_contact_id }}{{ $('Limpieza de payload de salida').item.json.crm_contacto_nuevo ? ' (nuevo)' : ' (existente)' }}\n*Asunto:* {{ $('Limpieza de payload de salida').item.json.asunto_original }}\n*Intención:* {{ $('Limpieza de payload de salida').item.json.intencion }} · *Estado:* {{ $('Limpieza de payload de salida').item.json.estado }} · *Worker:* {{ $('Limpieza de payload de salida').item.json.worker }}\n*Resumen:* {{ $('Limpieza de payload de salida').item.json.resumen_slack }}\n:page_facing_up: Borrador de respuesta guardado en Gmail (revisar y enviar).",
                              "otherOptions": {"includeLinkToWorkflow": False}},
               "credentials": {"slackOAuth2Api": SLACK_CRED}}

# ---------------------------------------------------------------- ensamblar
wf["nodes"] += [gmail_trigger, if_auto, descartar, hub_search, if_exists, hub_create, norm_email, entrada,
                limp_alerta, alerta_slack, if_email, limp_salida, draft, slack_aviso]

def link(a, b, out=0, inp=0):
    conn.setdefault(a, {"main": []})
    while len(conn[a]["main"]) <= out: conn[a]["main"].append([])
    conn[a]["main"][out].append({"node": b, "type": "main", "index": inp})

# Entradas
conn["Chat Trigger"] = {"main": [[{"node": "Entrada normalizada", "type": "main", "index": 0}]]}
link("Casilla de soporte (Gmail Trigger)", "¿Es correo automático?")
link("¿Es correo automático?", "Descartar correo automático (corta el bucle)", 0)
link("¿Es correo automático?", "Buscar contacto en CRM (Look up)", 1)
link("Buscar contacto en CRM (Look up)", "¿Contacto existe en CRM?")
link("¿Contacto existe en CRM?", "Normalizar entrada de email", 0)
link("¿Contacto existe en CRM?", "Crear contacto en CRM (Create)", 1)
link("Crear contacto en CRM (Create)", "Normalizar entrada de email")
link("Normalizar entrada de email", "Entrada normalizada")
link("Entrada normalizada", "Buscar memoria por Session_ID")

# Alerta: reemplazar destino "Alerta a supervisor humano" por el Set de limpieza
for src, c in conn.items():
    for outs in c.get("main", []):
        for e in outs:
            if e["node"] == "Alerta a supervisor humano":
                e["node"] = "Limpieza de alerta (Slack)"
conn.pop("Alerta a supervisor humano", None)
link("Limpieza de alerta (Slack)", "Alerta a supervisor humano (Slack)")
link("Alerta a supervisor humano (Slack)", "Respuesta fallback")

# Salida
conn["Log de trazabilidad (Sheets)"] = {"main": [[{"node": "¿Llegó por email?", "type": "main", "index": 0}]]}
link("¿Llegó por email?", "Limpieza de payload de salida", 0)
link("¿Llegó por email?", "¿Más de 5 mensajes?", 1)
link("Limpieza de payload de salida", "Borrador de respuesta (Create Draft)")
link("Borrador de respuesta (Create Draft)", "Aviso al canal de operaciones (Slack)")
link("Aviso al canal de operaciones (Slack)", "¿Más de 5 mensajes?")

wf["name"] = "JUMA - Manager (multi-agente + memoria + integraciones)"
wf["settings"] = {"executionOrder": "v1", "executionTimeout": 180, "saveExecutionProgress": True, "binaryMode": "separate"}
wf["pinData"] = {}
wf["meta"] = {"instanceId": "jumade", "templateCredsSetupCompleted": True}

json.dump(wf, open(OUT, "w"), ensure_ascii=False, indent=2)
print("OK", OUT, len(wf["nodes"]), "nodos")
