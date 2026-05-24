import uuid
from pathlib import Path

from flask import (
    Blueprint,
    jsonify,
    request
)

from werkzeug.utils import secure_filename


upload_bp = Blueprint(
    "upload_bp",
    __name__
)

BASE_UPLOAD_DIR = Path("uploaded_videos")

ALLOWED_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv"
}


def validate_extension(filename):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return None

    return extension


def save_uploaded_video(
    video_file,
    upload_type
):
    original_filename = secure_filename(
        video_file.filename
    )

    extension = validate_extension(
        original_filename
    )

    if not extension:
        return {
            "success": False,
            "message": "Invalid video format"
        }, 400

    video_id = str(uuid.uuid4())

    save_dir = (
        BASE_UPLOAD_DIR / upload_type
    )

    save_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    saved_filename = f"{video_id}{extension}"

    save_path = save_dir / saved_filename

    video_file.save(save_path)

    file_size_mb = round(
        save_path.stat().st_size / (1024 * 1024),
        2
    )

    return {
        "success": True,
        "video_id": video_id,
        "filename": saved_filename,
        "size_mb": file_size_mb,
        "status": "uploaded"
    }, 200


@upload_bp.route(
    "/register",
    methods=["POST"]
)
def register_video():

    if "video" not in request.files:
        return jsonify({
            "success": False,
            "message": "No video uploaded"
        }), 400

    video_file = request.files["video"]

    response, status_code = save_uploaded_video(
        video_file=video_file,
        upload_type="registration"
    )

    return jsonify(response), status_code


@upload_bp.route(
    "/verify",
    methods=["POST"]
)
def verify_video():

    if "video" not in request.files:
        return jsonify({
            "success": False,
            "message": "No video uploaded"
        }), 400

    video_file = request.files["video"]

    response, status_code = save_uploaded_video(
        video_file=video_file,
        upload_type="verification"
    )

    return jsonify(response), status_code