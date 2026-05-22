from flask import Blueprint, request
from werkzeug.utils import secure_filename
from app.utils.timers import Timer
import uuid
from app.utils.cleanup import cleanup_file
import time
from app.monitoring.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY
)
from app.core.config import TEMP_DIR
from app.services.verification_service import verify_speaker
# ======================================================
# BLUEPRINT
# ======================================================
from app.utils.validators import (
    validate_extension,
    validate_file_size
)
from flask  import g
from app.utils.responses import (
    success_response,
    error_response
)
from app.core.logger import logger
api = Blueprint("api", __name__)

# ======================================================
# ROUTE
# ======================================================

@api.route("/verify", methods=["POST"])
def verify():
    start_time = time.perf_counter()
    REQUEST_COUNT.inc()
    with Timer("Verification Request"):
        path1 = None
        path2 = None
        try:
            request_id = getattr(g, "request_id", "-")
            logger.info(
                f"[{request_id}] "
                f"Verification request started"
            )
            # --------------------------------------------------
            # CHECK FILES
            # --------------------------------------------------

            if "audio1" not in request.files:
                logger.warning(f"[{request_id}] Missing audio1 in request")
                return error_response("audio1 missing", status=400)

            if "audio2" not in request.files:
                logger.warning(f"[{request_id}] Missing audio2 in request")
                return error_response("audio2 missing", status=400)

            audio1 = request.files["audio1"]
            audio2 = request.files["audio2"]

            # --------------------------------------------------
            # VALIDATE INPUTS
            # --------------------------------------------------

            try:
                validate_extension(audio1.filename)
            except ValueError as exc:
                logger.warning(f"[{request_id}] Invalid extension for audio1: {exc}")
                return error_response(str(exc), status=400)

            try:
                validate_extension(audio2.filename)
            except ValueError as exc:
                logger.warning(f"[{request_id}] Invalid extension for audio2: {exc}")
                return error_response(str(exc), status=400)

            try:
                validate_file_size(audio1)
            except ValueError as exc:
                logger.warning(f"[{request_id}] audio1 exceeds size limit: {exc}")
                return error_response(str(exc), status=413)

            try:
                validate_file_size(audio2)
            except ValueError as exc:
                logger.warning(f"[{request_id}] audio2 exceeds size limit: {exc}")
                return error_response(str(exc), status=413)

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


            
            result = verify_speaker(path1, path2)
            # --------------------------------------------------
            # RETURN RESPONSE
            # --------------------------------------------------
            latency = (time.perf_counter() - start_time)
            REQUEST_LATENCY.observe(latency)
            logger.info(
                f"[{request_id}] Verification request completed in {latency:.4f} seconds"
            )
            return success_response(
                "verification completed",
                {
                    "audio1_path": str(path1),
                    "audio2_path": str(path2),
                    "verification_result": result,
                },
            )
        except ValueError as exc:
            logger.warning(f"[{request_id}] Audio validation failed: {exc}")
            return error_response(str(exc), status=400)
        except Exception as e:
            logger.exception(f"[{request_id}] Verification request failed")
            return error_response("verification failed", status=500)
        finally:
            if path1 is not None:
                cleanup_file(path1)
            if path2 is not None:
                cleanup_file(path2)