from flask import Blueprint, request

from werkzeug.utils import secure_filename

import uuid

from app.core.config import TEMP_DIR

from app.services.verification_service import (
    verify_wavlm
)

from app.utils.cleanup import cleanup_file

from app.utils.validators import (
    validate_extension,
    validate_file_size
)

from app.utils.responses import (
    success_response,
    error_response
)

api = Blueprint("api", __name__)

# ======================================================
# VERIFY
# ======================================================

@api.route("/verify", methods=["POST"])
def verify():

    path1 = None
    path2 = None

    try:

        # --------------------------------------------------
        # CHECK FILES
        # --------------------------------------------------

        if "audio1" not in request.files:
            return error_response(
                "audio1 missing",
                status=400
            )

        if "audio2" not in request.files:
            return error_response(
                "audio2 missing",
                status=400
            )

        audio1 = request.files["audio1"]
        audio2 = request.files["audio2"]

        # --------------------------------------------------
        # VALIDATE
        # --------------------------------------------------

        validate_extension(audio1.filename)
        validate_extension(audio2.filename)

        validate_file_size(audio1)
        validate_file_size(audio2)

        # --------------------------------------------------
        # SAVE TEMP FILES
        # --------------------------------------------------

        file1_name = (
            f"{uuid.uuid4()}_"
            f"{secure_filename(audio1.filename)}"
        )

        file2_name = (
            f"{uuid.uuid4()}_"
            f"{secure_filename(audio2.filename)}"
        )

        path1 = TEMP_DIR / file1_name
        path2 = TEMP_DIR / file2_name

        audio1.save(path1)
        audio2.save(path2)

        # --------------------------------------------------
        # VERIFY
        # --------------------------------------------------

        result = verify_wavlm(
            path1,
            path2
        )

        return success_response(
            "verification completed",
            result
        )

    except (ValueError, RuntimeError) as e:

        return error_response(
            str(e),
            status=400
        )

    except Exception as e:

        return error_response(
            str(e),
            status=500
        )

    finally:

        if path1 is not None:
            cleanup_file(path1)

        if path2 is not None:
            cleanup_file(path2)