from flask import Flask, jsonify, request

from main import graph


app = Flask(__name__)


def _messages_to_text(messages):
    if messages is None:
        return None

    if isinstance(messages, str):
        return messages.strip() or None

    if isinstance(messages, list):
        parts = []
        for message in messages:
            if isinstance(message, dict):
                content = message.get("content")
                if content is None:
                    content = message.get("text")
                if content is None:
                    content = message.get("message")
                if content is None:
                    content = str(message)
                parts.append(str(content).strip())
            else:
                parts.append(str(message).strip())

        joined = "\n".join(part for part in parts if part)
        return joined or None

    return str(messages).strip() or None


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/extract")
def extract():
    payload = request.get_json(silent=True) or {}
    messages = payload.get("messages")
    user_input = _messages_to_text(messages)

    if not user_input:
        return jsonify({"error": "messages is required"}), 400

    result = graph.invoke(
        {
            "user_input": user_input,
            "iteration_count": 0,
            "verification_history": [],
        }
    )

    return jsonify(
        {
            "response_output": result.get("response_output"),
            "validation_report": result.get("validation_report"),
            "raw_result": result,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)