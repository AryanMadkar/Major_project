from flask import Flask, jsonify, request

from main import graph
from cache import get as cache_get, set as cache_set, has as cache_has


app = Flask(__name__)
# Preserve non-ASCII characters in JSON responses by default
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

    # Use cache to avoid repeated expensive graph invocations
    cache_key = f"graph:{hash(user_input)}"
    if cache_has(cache_key):
        result = cache_get(cache_key)
    else:
        result = graph.invoke({
            "user_input": user_input,
            "iteration_count": 0,
            "verification_history": [],
        })
        cache_set(cache_key, result)

    response_output = result.get("response_output") or {}
    if isinstance(response_output, dict):
        response_output = {
            key: value
            for key, value in response_output.items()
            if key != "validation_report"
        }

    # If some extractor produced double-escaped Unicode (literal "\\uXXXX"),
    # decode those safely for obvious fields like price display, then strip
    # currency symbols and return a clean numeric display string.
    import json as _json
    import re as _re

    def _decode_escaped_unicode(val):
        if not isinstance(val, str):
            return val
        if "\\u" in val:
            try:
                return _json.loads(f'"{val}"')
            except Exception:
                return val
        return val

    def _strip_currency_symbols(s: str) -> str:
        # Remove common currency symbols and keep digits, commas, periods, and spaces
        return _re.sub(r"[\u00A2-\u00BF\u20A0-\u20CF$£€¥₹¢¤₪₩₽฿]+", "", s).strip()

    # Remove any '*_display' presentation fields recursively so responses only
    # contain canonical numeric values like `price`, `price_min`, `price_max`, etc.
    def _remove_display_fields(obj):
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key.endswith("_display"):
                    obj.pop(key, None)
                else:
                    _remove_display_fields(obj.get(key))
        elif isinstance(obj, list):
            for item in obj:
                _remove_display_fields(item)

    _remove_display_fields(response_output)

    return jsonify(response_output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)