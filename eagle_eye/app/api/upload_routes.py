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


def get_identity_key(payload):
    return payload.get("email") or payload.get("user_id")


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


def cleanup_artifacts(
    save_path=None,
    frames_dir=None,
    faces_dir=None,
    aligned_dir=None
):
    cleanup_path(save_path)
    cleanup_path(frames_dir)
    cleanup_path(faces_dir)
    cleanup_path(aligned_dir)


def fail_response(
    message,
    status_code,
    stage,
    **details
):
    response = {
        "success": False,
        "message": message,
        "stage": stage
    }

    if details:
        response["details"] = details

    return response, status_code


def build_embedding_data(detected_faces, aligned_directory):
    detector_embeddings = []

    for face_item in detected_faces.get("faces", []):
        embedding = face_item.get("embedding")

        if embedding:
            detector_embeddings.append({
                "face_file": face_item.get("face_file"),
                "embedding": embedding,
                "source": "detector"
            })

    if detector_embeddings:
        return {
            "success": True,
            "total_embeddings": len(detector_embeddings),
            "embeddings": detector_embeddings,
            "source": "detector"
        }

    embedding_data = extract_embeddings(
        aligned_faces_dir=aligned_directory
    )

    if embedding_data.get("success"):
        embedding_data["source"] = "aligned_faces"

    return embedding_data


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
    if video_file is None or not getattr(video_file, "filename", None):
        return fail_response(
            "No video file provided",
            400,
            "request"
        )

    original_filename = secure_filename(
        video_file.filename
    )

    extension = validate_extension(
        original_filename
    )

    if not extension:
        return fail_response(
            "Invalid video format",
            400,
            "validation",
            allowed_extensions=sorted(ALLOWED_EXTENSIONS),
            filename=original_filename
        )

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
        cleanup_path(save_path)
        return fail_response(
            "Failed to save uploaded video",
            500,
            "save_video",
            error=str(e)
        )

    file_size_mb = round(
        save_path.stat().st_size / (1024 * 1024),
        2
    )

    try:
        metadata = extract_video_metadata(str(save_path))
    except Exception as e:
        cleanup_path(save_path)
        return fail_response(
            "Failed to extract video metadata",
            400,
            "metadata",
            error=str(e)
        )

    # Ensure the video meets validation requirements before expensive frame extraction
    if not metadata.get("success") or not metadata.get("is_valid"):
        cleanup_path(save_path)
        return fail_response(
            "Corrupted or invalid video",
            422,
            "metadata",
            metadata=metadata
        )

    try:
        frames = extract_frames(
            video_path=str(save_path),
            video_id=video_id
        )
    except Exception as e:
        cleanup_path(save_path)
        return fail_response(
            "Failed to extract frames from video",
            500,
            "frame_extraction",
            error=str(e)
        )

    # If frame extraction returned a failure dict, clean up and return error
    if isinstance(frames, dict) and not frames.get("success"):
        frames_dir = frames.get("frames_directory")
        cleanup_artifacts(save_path, frames_dir=frames_dir)
        return fail_response(
            "Failed to extract frames from video",
            422,
            "frame_extraction",
            frames_error=frames.get("message")
        )

    liveness_data = None

    if upload_type == "verification":
        try:
            liveness_data = analyze_liveness(
                frames["frames_directory"]
            )
        except Exception as e:
            cleanup_artifacts(save_path, frames_dir=frames.get("frames_directory"))
            return fail_response(
                "Failed to analyze liveness",
                500,
                "liveness",
                error=str(e)
            )

        if not liveness_data.get("is_live"):
            cleanup_artifacts(save_path, frames_dir=frames.get("frames_directory"))
            return fail_response(
                "Liveness check failed",
                401,
                "liveness",
                liveness=liveness_data
            )

    try:
        detected_faces = detect_faces(
            frames_directory=frames[
                "frames_directory"
            ],
            video_id=video_id
        )
    except Exception as e:
        cleanup_artifacts(save_path, frames_dir=frames.get("frames_directory"))
        return fail_response(
            "Failed to detect faces in extracted frames",
            500,
            "face_detection",
            error=str(e)
        )

    aligned_directory = detected_faces.get(
        "aligned_directory"
    )

    try:
        embedding_data = build_embedding_data(
            detected_faces,
            aligned_directory
        )
    except Exception as e:
        cleanup_artifacts(
            save_path,
            frames_dir=frames.get("frames_directory"),
            faces_dir=detected_faces.get("faces_directory"),
            aligned_dir=aligned_directory
        )
        return fail_response(
            "Failed to extract embeddings from aligned faces",
            500,
            "embedding_extraction",
            error=str(e)
        )

    if not embedding_data.get("success") or not embedding_data.get(
        "total_embeddings"
    ):
        cleanup_artifacts(
            save_path,
            frames_dir=frames.get("frames_directory"),
            faces_dir=detected_faces.get("faces_directory"),
            aligned_dir=aligned_directory
        )
        return fail_response(
            "No usable embeddings were generated",
            422,
            "embedding_extraction",
            embeddings=embedding_data,
            hint="Detector embeddings were unavailable and aligned-face re-extraction also failed"
        )

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
        cleanup_artifacts(
            save_path,
            frames_dir=frames.get("frames_directory"),
            faces_dir=detected_faces.get("faces_directory"),
            aligned_dir=aligned_directory
        )
        return fail_response(
            "Unable to build a master embedding",
            422,
            "embedding_fusion"
        )

    if upload_type == "registration":
        if not user_id:
            cleanup_artifacts(
                save_path,
                frames_dir=frames.get("frames_directory"),
                faces_dir=detected_faces.get("faces_directory"),
                aligned_dir=aligned_directory
            )
            return fail_response(
                "email is required for registration",
                400,
                "request"
            )

        save_identity(
            user_id=user_id,
            embedding=master_embedding.tolist()
        )

        return {
            "success": True,
            "video_id": video_id,
            "email": user_id,
            "user_id": user_id,
            "embedding_count": embedding_data["total_embeddings"],
            "embedding_source": embedding_data.get("source", "unknown"),
            "status": "identity_registered"
        }, 200

    if upload_type == "verification":
        if not user_id:
            cleanup_artifacts(
                save_path,
                frames_dir=frames.get("frames_directory"),
                faces_dir=detected_faces.get("faces_directory"),
                aligned_dir=aligned_directory
            )
            return fail_response(
                "email is required for verification",
                400,
                "request"
            )

        stored_identity = load_identity(
            user_id
        )

        if stored_identity is None:
            cleanup_artifacts(
                save_path,
                frames_dir=frames.get("frames_directory"),
                faces_dir=detected_faces.get("faces_directory"),
                aligned_dir=aligned_directory
            )
            return fail_response(
                "User not found",
                404,
                "identity_lookup",
                email=user_id
            )

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
            "liveness": liveness_data,
            "email": stored_identity["user_id"],
            "embedding_source": embedding_data.get("source", "unknown")
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
    identity_key = get_identity_key(payload)

    response, status_code = save_uploaded_video(
        video_file=video_file,
        upload_type="registration",
        user_id=identity_key
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
    payload = get_request_payload()
    identity_key = get_identity_key(payload)

    response, status_code = save_uploaded_video(
        video_file=video_file,
        upload_type="verification",
        user_id=identity_key
    )

    return jsonify(response), status_code