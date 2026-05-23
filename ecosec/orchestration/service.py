from io import BytesIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from config import (
    AGGREGATION_THRESHOLD,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MODEL_ENDPOINTS,
    REQUEST_TIMEOUT_SECONDS,
)

# ======================================================
# VALIDATION
# ======================================================

def validate_extension(filename):

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise ValueError(f"Unsupported file type: {extension}")


def validate_file_size(file_storage):

    file_storage.seek(0, 2)
    size_mb = file_storage.tell() / (1024 * 1024)
    file_storage.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:

        raise ValueError(f"File exceeds {MAX_FILE_SIZE_MB}MB")

# ======================================================
# MODEL CALLS
# ======================================================

def _extract_model_payload(response_json, fallback_name):

    data = response_json.get("data")

    if isinstance(data, dict) and "verification_result" in data:
        data = data["verification_result"]

    if not isinstance(data, dict):
        data = {}

    return {
        "model": data.get("model", fallback_name),
        "similarity": data.get("similarity"),
        "same_speaker": data.get("same_speaker"),
        "threshold": data.get("threshold"),
        "raw": data,
    }


def _call_model(endpoint_config, audio1_bytes, audio2_bytes, audio1_name, audio2_name):

    files = {
        "audio1": (audio1_name, BytesIO(audio1_bytes), "application/octet-stream"),
        "audio2": (audio2_name, BytesIO(audio2_bytes), "application/octet-stream"),
    }

    response = requests.post(
        endpoint_config["url"],
        files=files,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response.raise_for_status()

    response_json = response.json()

    return _extract_model_payload(response_json, endpoint_config["name"])

# ======================================================
# AGGREGATION
# ======================================================

def orchestrate_verification(audio1, audio2):

    audio1_bytes = audio1.read()
    audio2_bytes = audio2.read()

    audio1.seek(0)
    audio2.seek(0)

    total_weight = 0.0
    weighted_vote_sum = 0.0
    weighted_similarity_sum = 0.0

    model_results = []
    model_errors = []

    futures = {}

    with ThreadPoolExecutor(max_workers=len(MODEL_ENDPOINTS)) as executor:

        for endpoint_config in MODEL_ENDPOINTS:

            futures[executor.submit(
                _call_model,
                endpoint_config,
                audio1_bytes,
                audio2_bytes,
                audio1.filename,
                audio2.filename,
            )] = endpoint_config

        for future in as_completed(futures):

            endpoint_config = futures[future]
            weight = float(endpoint_config["weight"])

            try:

                model_result = future.result()

                similarity = model_result.get("similarity")
                same_speaker = model_result.get("same_speaker")

                model_results.append({
                    "model": model_result.get("model", endpoint_config["name"]),
                    "weight": weight,
                    "similarity": similarity,
                    "same_speaker": same_speaker,
                    "threshold": model_result.get("threshold"),
                    "status": "ok",
                    "raw": model_result.get("raw", {}),
                })

                if same_speaker is not None:
                    weighted_vote_sum += weight * (1.0 if same_speaker else 0.0)
                    total_weight += weight

                if similarity is not None:
                    weighted_similarity_sum += weight * float(similarity)

            except Exception as exc:

                model_errors.append({
                    "model": endpoint_config["name"],
                    "weight": weight,
                    "status": "error",
                    "error": str(exc),
                })

    if total_weight <= 0:

        raise RuntimeError("All model requests failed")

    weighted_vote = weighted_vote_sum / total_weight
    weighted_similarity = weighted_similarity_sum / total_weight

    final_same_speaker = weighted_vote >= AGGREGATION_THRESHOLD

    return {
        "final_same_speaker": final_same_speaker,
        "final_decision": "same_speaker" if final_same_speaker else "different_speaker",
        "weighted_vote": round(weighted_vote, 4),
        "weighted_similarity": round(weighted_similarity, 4),
        "aggregation_threshold": AGGREGATION_THRESHOLD,
        "models": model_results,
        "errors": model_errors,
        "weights_used": {
            endpoint["name"]: endpoint["weight"] for endpoint in MODEL_ENDPOINTS
        },
    }
