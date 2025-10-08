from flask import Flask, request, jsonify
from flasgger import Swagger
from uuid import uuid4
from datetime import datetime
import os
# from huggingface_hub import InferenceClient   # si vas a usar Hugging Face client

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Chatbot Orchestrator API',
    'uiversion': 3
}
swagger = Swagger(app)

# ---- Configuration / secrets via env ----
HF_TOKEN = os.environ.get("HF_TOKEN", "dummy")
# SMTP settings, DB connection, etc. via env

# ---- thresholds ----
THRESHOLD_HIGH = 0.85
THRESHOLD_MODERATE = 0.5

# ---- In-memory store (demo). En producción usar DB ----
CONVERSATIONS = {}
CONSENTS = {}
ESCALATIONS = {}

# ---- Mock / stub functions (replace with real calls) ----
def call_bert(text, metadata=None):
    """
    Replace this with your real BERT classifier call.
    Return: dict {'risk_score': float, 'risk_label': 'none'|'low'|'moderate'|'high', 'explanation': str}
    """
    # Dummy rule-based stub for demo:
    score = 0.0
    lower = text.lower()
    if "suicid" in lower or "no quiero" in lower or "ya no" in lower:
        score = 0.95
        label = "high"
    elif "triste" in lower or "estres" in lower:
        score = 0.6
        label = "moderate"
    else:
        score = 0.1
        label = "none"
    return {"risk_score": score, "risk_label": label, "explanation": "heuristic stub"}

def call_mistral(messages):
    """
    Replace with actual call to Mistral (Hugging Face InferenceClient or HTTP).
    messages: list of {"role":..,"content":..}
    Return assistant text.
    """
    # Simple echo stub for demo
    last_user = next((m['content'] for m in reversed(messages) if m['role']=='user'), '')
    return f"Entiendo. Has dicho: {last_user}. Estoy aquí para escucharte."

# ---- Endpoints ----
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok","time": datetime.utcnow().isoformat() + "Z"})

@app.route("/classify", methods=["POST"])
def classify():
    """
    Classify message with BERT
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              conversation_id: {type: string}
              message: {type: string}
    responses:
      200:
        description: classification result
    """
    body = request.get_json() or {}
    message = body.get("message","")
    conversation_id = body.get("conversation_id") or str(uuid4())
    result = call_bert(message)
    # minimal persistence demo:
    CONVERSATIONS.setdefault(conversation_id, {"messages":[],"created_at": datetime.utcnow().isoformat()})
    CONVERSATIONS[conversation_id]["messages"].append({
        "role":"user","content":message,"timestamp":datetime.utcnow().isoformat(),
        "risk_score": result["risk_score"], "risk_label": result["risk_label"]
    })
    return jsonify({
        "conversation_id": conversation_id,
        "risk_score": result["risk_score"],
        "risk_label": result["risk_label"],
        "explanation": result["explanation"]
    })

@app.route("/message", methods=["POST"])
def message():
    """
    Main orchestrator: classify then chat/respond
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              conversation_id: {type: string}
              message: {type: string}
              user_session: {type: object}
    responses:
      200:
        description: response
    """
    body = request.get_json() or {}
    message = body.get("message","")
    conversation_id = body.get("conversation_id") or str(uuid4())
    anon = body.get("user_session", {}).get("anonymous_id")
    # 1) classify
    classification = call_bert(message)
    # store user message
    CONVERSATIONS.setdefault(conversation_id, {"messages":[], "created_at": datetime.utcnow().isoformat()})
    CONVERSATIONS[conversation_id]["messages"].append({
        "role":"user","content":message,"timestamp":datetime.utcnow().isoformat(),
        "risk_score": classification["risk_score"], "risk_label": classification["risk_label"]
    })

    # 2) logic
    if classification["risk_label"] == "high":
        # immediate supportive reply template OR generate with Mistral using system prompt
        system_prompt = {
            "role":"system",
            "content":"Eres un chatbot de apoyo emocional en español, responde con empatía. Si detectas riesgo alto, ofrece ayuda y pregunta si la persona desea pedir ayuda humana."
        }
        messages = [system_prompt] + CONVERSATIONS[conversation_id]["messages"]
        # call Mistral to generate empathetic message
        reply = call_mistral(messages)
        # flag for frontend to open consent flow
        response = {
            "conversation_id": conversation_id,
            "risk_label": classification["risk_label"],
            "risk_score": classification["risk_score"],
            "reply": reply,
            "escalation_required": True,
            "next_action": "offer_consent"
        }
        return jsonify(response)

    elif classification["risk_label"] == "moderate":
        # reply via Mistral
        system_prompt = {"role":"system","content":"Eres un chatbot de apoyo emocional para estudiantes en Colombia, responde en español."}
        messages = [system_prompt] + CONVERSATIONS[conversation_id]["messages"]
        reply = call_mistral(messages)
        CONVERSATIONS[conversation_id]["messages"].append({"role":"assistant","content":reply,"timestamp":datetime.utcnow().isoformat()})
        return jsonify({
            "conversation_id": conversation_id,
            "risk_label": classification["risk_label"],
            "reply": reply,
            "escalation_required": False
        })
    else:
        # none -> normal chat
        system_prompt = {"role":"system","content":"Eres un chatbot de apoyo emocional para estudiantes universitarios en Colombia. Responde en español."}
        messages = [system_prompt] + CONVERSATIONS[conversation_id]["messages"]
        reply = call_mistral(messages)
        CONVERSATIONS[conversation_id]["messages"].append({"role":"assistant","content":reply,"timestamp":datetime.utcnow().isoformat()})
        return jsonify({
            "conversation_id":conversation_id,
            "risk_label":"none",
            "reply":reply,
            "escalation_required": False
        })

@app.route("/consent", methods=["POST"])
def consent():
    """
    Store consent before sending PII
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              conversation_id: {type: string}
              user_name: {type: string}
              user_email: {type: string}
              consent: {type: boolean}
    """
    body = request.get_json() or {}
    conv = body.get("conversation_id")
    consent_flag = body.get("consent", False)
    cid = str(uuid4())
    CONSENTS[cid] = {
        "conversation_id": conv,
        "user_name": body.get("user_name"),
        "user_email": body.get("user_email"),
        "consent": consent_flag,
        "timestamp": datetime.utcnow().isoformat()
    }
    # attach consent to conversation
    if conv in CONVERSATIONS:
        CONVERSATIONS[conv]["consent_id"] = cid
    return jsonify({"status":"ok","consent_id":cid})

@app.route("/escalate", methods=["POST"])
def escalate():
    """
    Trigger escalation to coordination (requires consent or policy override)
    """
    body = request.get_json() or {}
    conv = body.get("conversation_id")
    consent_id = body.get("consent_id")
    summary = body.get("summary") or "Extracto automático"
    esc_id = str(uuid4())
    ESCALATIONS[esc_id] = {
        "conversation_id": conv,
        "consent_id": consent_id,
        "summary": summary,
        "delivered": False,
        "created_at": datetime.utcnow().isoformat()
    }
    # In production: send email/webhook to coordination; here just mark delivered
    ESCALATIONS[esc_id]["delivered"] = True
    ESCALATIONS[esc_id]["delivered_at"] = datetime.utcnow().isoformat()
    return jsonify({"status":"sent","escalation_id":esc_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
