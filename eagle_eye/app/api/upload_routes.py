import uuid
from pathlib import Path
from shutil import rmtree
from app.services.video_metadata import (
    extract_video_metadata
)
from app.services.frame_extractor import (
    extract_frames
)
from flask import (
    Blueprint,
    jsonify,
    request
)
from app.services.face_detector import (
    detect_faces
)
from app.services.liveness_detector import (
    analyze_liveness
)
from werkzeug.utils import secure_filename

from app.services.embedding_extractor import (
    extract_embeddings
)

from app.services.embedding_fusion import (
    fuse_embeddings
)

from app.services.identity_storage import (
    save_identity,
    load_identity
)

from app.services.similarity_engine import (
    compare_embeddings
)
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


def get_request_payload():
    payload = {}

    form_data = request.form.to_dict()

    if form_data:
        payload.update(form_data)

    json_data = request.get_json(silent=True)

    if isinstance(json_data, dict):
        payload.update(json_data)

    return payload


def average_embeddings(embeddings):
    if not embeddings:
        return None

    dimensions = len(embeddings[0])

    return [
        sum(embedding[index] for embedding in embeddings) / len(embeddings)
        for index in range(dimensions)
    ]


def cleanup_path(path_value):
    if not path_value:
        return

    path = Path(path_value)

    if path.is_dir():
        rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)


def validate_extension(filename):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return None

    return extension


def save_uploaded_video(
    video_file,
    upload_type,
    user_id=None
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

    try:
        video_file.save(str(save_path))
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to save uploaded video",
            "error": str(e)
        }, 500

    file_size_mb = round(
        save_path.stat().st_size / (1024 * 1024),
        2
    )

    try:
        metadata = extract_video_metadata(str(save_path))
    except Exception as e:
        save_path.unlink(missing_ok=True)
        return {
            "success": False,
            "message": "Failed to extract video metadata",
            "error": str(e)
        }, 400

    # Ensure the video meets validation requirements before expensive frame extraction
    if not metadata.get("success") or not metadata.get("is_valid"):
        save_path.unlink(missing_ok=True)
        return {
            "success": False,
            "message": "Corrupted or invalid video",
            "metadata": metadata
        }, 400

    try:
        frames = extract_frames(
            video_path=str(save_path),
            video_id=video_id
        )
    except Exception as e:
        save_path.unlink(missing_ok=True)
        return {
            "success": False,
            "message": "Failed to extract frames from video",
            "error": str(e)
        }, 400

    # If frame extraction returned a failure dict, clean up and return error
    if isinstance(frames, dict) and not frames.get("success"):
        # remove saved video
        save_path.unlink(missing_ok=True)
        # attempt to remove any partially written frames directory
        frames_dir = frames.get("frames_directory")
        if frames_dir:
            try:
                # remove files inside dir if present
                from shutil import rmtree

                rmtree(frames_dir, ignore_errors=True)
            except Exception:
                pass

        return {
            "success": False,
            "message": "Failed to extract frames from video",
            "frames_error": frames.get("message")
        }, 400

    liveness_data = None

    if upload_type == "verification":
        try:
            liveness_data = analyze_liveness(
                frames["frames_directory"]
            )
        except Exception as e:
            cleanup_path(save_path)
            return {
                "success": False,
                "message": "Failed to analyze liveness",
                "error": str(e)
            }, 400

        if not liveness_data.get("is_live"):
            cleanup_path(save_path)
            return {
                "success": False,
                "message": "Liveness check failed",
                "liveness": liveness_data
            }, 401

    try:
        detected_faces = detect_faces(
            frames_directory=frames[
                "frames_directory"
            ],
            video_id=video_id
        )
    except Exception as e:
        cleanup_path(save_path)
        return {
            "success": False,
            "message": "Failed to detect faces in extracted frames",
            "error": str(e)
        }, 400

    aligned_directory = detected_faces.get(
        "aligned_directory"
    )

    try:
        embedding_data = extract_embeddings(
            aligned_faces_dir=aligned_directory
        )
    except Exception as e:
        cleanup_path(save_path)
        cleanup_path(detected_faces.get("faces_directory"))
        cleanup_path(aligned_directory)
        return {
            "success": False,
            "message": "Failed to extract embeddings from aligned faces",
            "error": str(e)
        }, 400

    if not embedding_data.get("success") or not embedding_data.get(
        "total_embeddings"
    ):
        cleanup_path(save_path)
        cleanup_path(detected_faces.get("faces_directory"))
        cleanup_path(aligned_directory)
        return {
            "success": False,
            "message": "No usable embeddings were generated",
            "embeddings": embedding_data
        }, 400

    all_embeddings = []

    for item in embedding_data[
        "embeddings"
    ]:

        all_embeddings.append(
            item["embedding"]
        )

    master_embedding = fuse_embeddings(
        all_embeddings
    )

    if master_embedding is None:
        cleanup_path(save_path)
        cleanup_path(detected_faces.get("faces_directory"))
        cleanup_path(aligned_directory)
        return {
            "success": False,
            "message": "Unable to build a master embedding"
        }, 400

    if upload_type == "registration":
        if not user_id:
            cleanup_path(save_path)
            cleanup_path(detected_faces.get("faces_directory"))
            cleanup_path(aligned_directory)
            return {
                "success": False,
                "message": "user_id is required for registration"
            }, 400

        save_identity(
            user_id=user_id,
            embedding=master_embedding.tolist()
        )

        return {
            "success": True,
            "video_id": video_id,
            "user_id": user_id,
            "embedding_count": embedding_data["total_embeddings"],
            "status": "identity_registered"
        }, 200

    if upload_type == "verification":
        stored_identity = load_identity(
            request.form.get(
                "user_id"
            )
        )

        if stored_identity is None:
            cleanup_path(save_path)
            cleanup_path(detected_faces.get("faces_directory"))
            cleanup_path(aligned_directory)
            return {
                "success": False,
                "message": "User not found"
            }, 404

        verification_embeddings = []

        for item in embedding_data[
            "embeddings"
        ]:

            verification_embeddings.append(
                item["embedding"]
            )

        new_embedding = fuse_embeddings(
            verification_embeddings
        )

        similarity = compare_embeddings(
            stored_identity["embedding"],
            new_embedding.tolist()
        )

        matched = similarity > 0.75

        embedding_count = len(
            verification_embeddings
        )

        return {
            "success": True,
            "similarity": round(
                similarity,
                4
            ),
            "authenticated": matched,
            "embedding_count": embedding_count,
            "liveness": liveness_data
        }, 200

    cleanup_path(save_path)
    cleanup_path(detected_faces.get("faces_directory"))
    cleanup_path(aligned_directory)

    return {
        "success": True,
        "video_id": video_id,
        "filename": saved_filename,
        "size_mb": file_size_mb,
        "status": "uploaded",
        "metadata": metadata,
        "frames": frames,
        "faces": detected_faces,
        "embeddings": embedding_data
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
    payload = get_request_payload()

    response, status_code = save_uploaded_video(
        video_file=video_file,
        upload_type="registration",
        user_id=payload.get("user_id")
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
        upload_type="verification",
        user_id=request.form.get("user_id")
    )

    return jsonify(response), status_code