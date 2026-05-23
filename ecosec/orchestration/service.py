from io import BytesIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from config import (
    AGGREGATION_THRESHOLD,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MODEL_ENDPOINTS,
    REQUEST_TIMEOUT_SECONDS,
)

# ======================================================
# OPTIMIZED HTTP SESSION POOL WITH KEEPALIVE
# ======================================================

session = requests.Session()
# Create a robust pool with enough connections for concurrent model requests
adapter = HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
    max_retries=Retry(
        total=2,
        backoff_factor=0.05,
        status_forcelist=[502, 503, 504],
        raise_on_status=False
    )
)
session.mount("http://", adapter)
session.mount("https://", adapter)

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

    response = session.post(
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

    # Accumulators for Standard Weighted Voting
    total_standard_weight = 0.0
    standard_vote_sum = 0.0
    standard_similarity_sum = 0.0

    # Accumulators for Power Weighted Voting (Exponential scaling)
    POWER_EXPONENT = 2.0
    total_power_weight = 0.0
    power_vote_sum = 0.0
    power_similarity_sum = 0.0

    model_results = []
    model_errors = []

    futures = {}

    with ThreadPoolExecutor(max_workers=len(MODEL_ENDPOINTS)) as executor:

        # 1. Send all audio requests concurrently at the same time
        for endpoint_config in MODEL_ENDPOINTS:
            futures[executor.submit(
                _call_model,
                endpoint_config,
                audio1_bytes,
                audio2_bytes,
                audio1.filename,
                audio2.filename,
            )] = endpoint_config

        # 2. Wait for all agents with a maximum hard timeout of 60 seconds (1 minute)
        try:
            for future in as_completed(futures, timeout=60.0):
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

                    # Calculate standard weighted voting stats
                    if same_speaker is not None:
                        standard_vote_sum += weight * (1.0 if same_speaker else 0.0)
                        total_standard_weight += weight
                    if similarity is not None:
                        standard_similarity_sum += weight * float(similarity)

                    # Calculate power weighted voting stats (raises weights to a power)
                    power_weight = weight ** POWER_EXPONENT
                    if same_speaker is not None:
                        power_vote_sum += power_weight * (1.0 if same_speaker else 0.0)
                        total_power_weight += power_weight
                    if similarity is not None:
                        power_similarity_sum += power_weight * float(similarity)

                except Exception as exc:
                    model_errors.append({
                        "model": endpoint_config["name"],
                        "weight": weight,
                        "status": "error",
                        "error": str(exc),
                    })
        except TimeoutError:
            # Handle orchestration timeout: cancel pending requests and report them as timeouts
            for future, endpoint_config in futures.items():
                if not future.done():
                    future.cancel()
                    model_errors.append({
                        "model": endpoint_config["name"],
                        "weight": float(endpoint_config["weight"]),
                        "status": "error",
                        "error": "Request timed out (exceeded the maximum 60 seconds limit)",
                    })

    if total_power_weight <= 0:
        raise RuntimeError("All model requests failed or timed out")

    # 3. Final calculations
    standard_vote = standard_vote_sum / total_standard_weight if total_standard_weight > 0 else 0.0
    standard_similarity = standard_similarity_sum / total_standard_weight if total_standard_weight > 0 else 0.0

    power_vote = power_vote_sum / total_power_weight
    power_similarity = power_similarity_sum / total_power_weight

    # Give final result using the Power Weighted Vote
    final_same_speaker = power_vote >= AGGREGATION_THRESHOLD

    return {
        "final_same_speaker": final_same_speaker,
        "final_decision": "same_speaker" if final_same_speaker else "different_speaker",
        
        # Power weighted voting results (Used for final decision)
        "power_weighted_vote": round(power_vote, 4),
        "power_weighted_similarity": round(power_similarity, 4),
        "power_exponent": POWER_EXPONENT,

        # Standard weighted voting comparison
        "standard_weighted_vote": round(standard_vote, 4),
        "standard_weighted_similarity": round(standard_similarity, 4),
        
        "aggregation_threshold": AGGREGATION_THRESHOLD,
        "models": model_results,
        "errors": model_errors,
        "weights_used": {
            endpoint["name"]: endpoint["weight"] for endpoint in MODEL_ENDPOINTS
        },
    }
