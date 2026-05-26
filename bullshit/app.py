from flask import Flask, jsonify, request

from main import graph


app = Flask(__name__)
# Preserve non-ASCII characters (e.g. currency symbols) in JSON responses
app.config["JSON_AS_ASCII"] = False


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

    response_output = result.get("response_output") or {}
    if isinstance(response_output, dict):
        response_output = {
            key: value
            for key, value in response_output.items()
            if key != "validation_report"
        }

    # If some extractor produced double-escaped Unicode (literal "\\uXXXX"),
    # decode those safely for obvious fields like price display.
    def _decode_escaped_unicode(val):
        import json as _json

        if not isinstance(val, str):
            return val
        if "\\u" in val:
            try:
                return _json.loads(f'"{val}"')
            except Exception:
                return val
        return val

    for k, v in list(response_output.items()):
        # handle common display fields which may contain escaped currency
        if k.endswith("_display") and isinstance(v, str):
            response_output[k] = _decode_escaped_unicode(v)

    return jsonify(response_output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)