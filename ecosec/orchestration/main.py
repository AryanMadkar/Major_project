from flask import Flask, request

from config import ORCHESTRATION_PORT
from responses import error_response, success_response
from service import (
    orchestrate_verification,
    validate_extension,
    validate_file_size,
)

# ======================================================
# CREATE APP
# ======================================================

app = Flask(__name__)

# ======================================================
# VERIFY
# ======================================================

@app.route("/verify", methods=["POST"])
def verify():

    if "audio1" not in request.files:
        return error_response("audio1 missing", status=400)

    if "audio2" not in request.files:
        return error_response("audio2 missing", status=400)

    audio1 = request.files["audio1"]
    audio2 = request.files["audio2"]

    try:
        validate_extension(audio1.filename)
        validate_extension(audio2.filename)
        validate_file_size(audio1)
        validate_file_size(audio2)
    except ValueError as exc:
        return error_response(str(exc), status=400)

    try:
        result = orchestrate_verification(audio1, audio2)
        return success_response("orchestration completed", result)
    except Exception as exc:
        return error_response(str(exc), status=500)


# ======================================================
# RUN SERVER
# ======================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=ORCHESTRATION_PORT, debug=True, use_reloader=False)
