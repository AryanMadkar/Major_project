from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

import uuid

from app.core.config import TEMP_DIR

# ======================================================
# BLUEPRINT
# ======================================================

api = Blueprint("api", __name__)

# ======================================================
# ROUTE
# ======================================================

@api.route("/verify", methods=["POST"])
def verify():
    try:
                # --------------------------------------------------
        # CHECK FILES
        # --------------------------------------------------

        if "audio1" not in request.files:
            return jsonify({
                "error": "audio1 missing"
            }), 400

        if "audio2" not in request.files:
            return jsonify({
                "error": "audio2 missing"
            }), 400

        audio1 = request.files["audio1"]
        audio2 = request.files["audio2"]

        # --------------------------------------------------
        # GENERATE SAFE TEMP NAMES
        # --------------------------------------------------

        file1_name = f"{uuid.uuid4()}_{secure_filename(audio1.filename)}"
        file2_name = f"{uuid.uuid4()}_{secure_filename(audio2.filename)}"

        path1 = TEMP_DIR / file1_name
        path2 = TEMP_DIR / file2_name

        # --------------------------------------------------
        # SAVE FILES
        # --------------------------------------------------

        audio1.save(path1)
        audio2.save(path2)

        # --------------------------------------------------
        # RETURN RESPONSE
        # --------------------------------------------------

        return jsonify({
            "message": "files uploaded successfully",
            "audio1_path": str(path1),
            "audio2_path": str(path2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500