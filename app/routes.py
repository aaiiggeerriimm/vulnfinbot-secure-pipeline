import re
from flask import Blueprint, request, jsonify

main_bp = Blueprint("main", __name__)

MAX_MESSAGE_LENGTH = 500
SYSTEM_SECRET_KEY = "SUPER_SECRET_INTERNAL_KEY_DO_NOT_LEAK"

BLOCKED_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt",
    r"reveal\s+(your\s+)?(secrets|instructions|api\s*key)",
    r"execute\s+command",
    r"drop\s+table",
]

def generate_ai_response(user_message: str) -> str:
    lowered = user_message.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, lowered):
            return (
                "I cannot process requests that attempt to alter system instructions "
                "or access restricted internal information. How can I help with your budget?"
            )

    if "budget" in lowered:
        return "You can start by tracking your monthly income and categorizing fixed vs. variable expenses."
    if "save" in lowered or "saving" in lowered:
        return "Consider the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings."
    return "I am Mini-VulnFinBot. Ask me about budgeting, saving, or personal expense tracking."

def sanitize_output(text: str) -> str:
    if SYSTEM_SECRET_KEY in text:
        return "Response blocked by output security filter."
    return text.replace("<", "&lt;").replace(">", "&gt;")

@main_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@main_bp.route("/api/chat", methods=["POST"])
def chat():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    if "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    message = data["message"]
    if not isinstance(message, str):
        return jsonify({"error": "'message' must be a string"}), 400

    cleaned_message = message.strip()
    if not cleaned_message:
        return jsonify({"error": "'message' cannot be empty"}), 400

    if len(cleaned_message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"'message' exceeds maximum length of {MAX_MESSAGE_LENGTH} characters"}), 400

    raw_response = generate_ai_response(cleaned_message)
    safe_response = sanitize_output(raw_response)

    return jsonify({"response": safe_response}), 200