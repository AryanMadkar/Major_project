from io import BytesIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import io
import numpy as np
import contextlib
import wave

from config import (
    AGGREGATION_THRESHOLD,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MODEL_ENDPOINTS,
    ORCHESTRATION_CONSENSUS_FLOOR,
    ORCHESTRATION_MARGIN_TOLERANCE,
    ORCHESTRATION_MIN_SECONDS,
    ORCHESTRATION_MAX_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
)

try:
    import soundfile as sf
except Exception:
    sf = None

try:
    from pydub import AudioSegment
except Exception:
    AudioSegment = None


def process_audio_bytes(raw_bytes: bytes, min_seconds: float, max_seconds: float) -> bytes:
    """Trim or pad audio bytes to be within [min_seconds, max_seconds].

    Returns WAV bytes (PCM 16) when processed; if processing libs are missing,
    returns the original bytes.
    """
    # Try soundfile path
    if sf is not None:
        try:
            bio = io.BytesIO(raw_bytes)
            with sf.SoundFile(bio) as f:
                sr = f.samplerate
                data = f.read(dtype="float32")

            if data.ndim > 1:
                data = np.mean(data, axis=1)

            duration = len(data) / float(sr)

            # Trim if too long
            if duration > max_seconds:
                target_samples = int(max_seconds * sr)
                start = max(0, (len(data) - target_samples) // 2)
                data = data[start : start + target_samples]
            # Pad if too short
            elif duration < min_seconds:
                target_samples = int(min_seconds * sr)
                pad_len = target_samples - len(data)
                data = np.concatenate([data, np.zeros(pad_len, dtype=data.dtype)])

            out = io.BytesIO()
            sf.write(out, data, sr, format="WAV", subtype="PCM_16")
            return out.getvalue()
        except Exception:
            pass

    # Try pydub fallback
    if AudioSegment is not None:
        try:
            bio = io.BytesIO(raw_bytes)
            seg = AudioSegment.from_file(bio)
            dur = len(seg) / 1000.0
            if dur > max_seconds:
                target_ms = int(max_seconds * 1000)
                start_ms = max(0, (len(seg) - target_ms) // 2)
                seg = seg[start_ms : start_ms + target_ms]
            elif dur < min_seconds:
                target_ms = int(min_seconds * 1000)
                pad_ms = target_ms - len(seg)
                seg = seg + AudioSegment.silent(duration=pad_ms)

            out = io.BytesIO()
            seg.export(out, format="wav")
            return out.getvalue()
        except Exception:
            pass

    return raw_bytes

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

    # Read original bytes
    audio1_bytes = audio1.read()
    audio2_bytes = audio2.read()

    # Normalize durations before sending to models. If processing is unavailable
    # this will be a no-op and original bytes will be used.
    audio1_bytes = process_audio_bytes(audio1_bytes, ORCHESTRATION_MIN_SECONDS, ORCHESTRATION_MAX_SECONDS)
    audio2_bytes = process_audio_bytes(audio2_bytes, ORCHESTRATION_MIN_SECONDS, ORCHESTRATION_MAX_SECONDS)

    # reset file pointers for compatibility
    try:
        audio1.seek(0)
        audio2.seek(0)
    except Exception:
        pass

    # Accumulators for Standard Weighted Voting
    total_standard_weight = 0.0
    standard_vote_sum = 0.0
    standard_similarity_sum = 0.0
    standard_threshold_sum = 0.0

    # Accumulators for Power Weighted Voting (Exponential scaling)
    POWER_EXPONENT = 2.0
    total_power_weight = 0.0
    power_vote_sum = 0.0
    power_similarity_sum = 0.0
    power_threshold_sum = 0.0

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
                    threshold = model_result.get("threshold")

                    model_results.append({
                        "model": model_result.get("model", endpoint_config["name"]),
                        "weight": weight,
                        "similarity": similarity,
                        "same_speaker": same_speaker,
                        "threshold": threshold,
                        "status": "ok",
                        "raw": model_result.get("raw", {}),
                    })

                    # Calculate standard weighted voting stats
                    if same_speaker is not None:
                        standard_vote_sum += weight * (1.0 if same_speaker else 0.0)
                        total_standard_weight += weight
                    if similarity is not None:
                        standard_similarity_sum += weight * float(similarity)
                    if threshold is not None:
                        standard_threshold_sum += weight * float(threshold)

                    # Calculate power weighted voting stats (raises weights to a power)
                    power_weight = weight ** POWER_EXPONENT
                    if same_speaker is not None:
                        power_vote_sum += power_weight * (1.0 if same_speaker else 0.0)
                        total_power_weight += power_weight
                    if similarity is not None:
                        power_similarity_sum += power_weight * float(similarity)
                    if threshold is not None:
                        power_threshold_sum += power_weight * float(threshold)

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
    standard_threshold = standard_threshold_sum / total_standard_weight if total_standard_weight > 0 else 0.0

    power_vote = power_vote_sum / total_power_weight
    power_similarity = power_similarity_sum / total_power_weight
    power_threshold = power_threshold_sum / total_power_weight

    power_margin = power_similarity - power_threshold
    standard_margin = standard_similarity - standard_threshold

    # Prefer the soft similarity margin; use consensus only when the score is close to the boundary.
    consensus_override = power_vote >= ORCHESTRATION_CONSENSUS_FLOOR and power_margin >= -ORCHESTRATION_MARGIN_TOLERANCE
    final_same_speaker = power_margin >= 0.0 or consensus_override

    if power_margin >= 0.0:
        final_decision_basis = "soft_margin"
    elif consensus_override:
        final_decision_basis = "consensus_override"
    else:
        final_decision_basis = "margin_reject"

    return {
        "final_same_speaker": final_same_speaker,
        "final_decision": "same_speaker" if final_same_speaker else "different_speaker",
        "final_decision_basis": final_decision_basis,
        
        # Power weighted scoring results (Used for final decision)
        "power_weighted_vote": round(power_vote, 4),
        "power_weighted_similarity": round(power_similarity, 4),
        "power_weighted_threshold": round(power_threshold, 4),
        "power_weighted_margin": round(power_margin, 4),
        "power_exponent": POWER_EXPONENT,

        # Standard weighted voting comparison
        "standard_weighted_vote": round(standard_vote, 4),
        "standard_weighted_similarity": round(standard_similarity, 4),
        "standard_weighted_threshold": round(standard_threshold, 4),
        "standard_weighted_margin": round(standard_margin, 4),
        
        "aggregation_threshold": AGGREGATION_THRESHOLD,
        "consensus_floor": ORCHESTRATION_CONSENSUS_FLOOR,
        "margin_tolerance": ORCHESTRATION_MARGIN_TOLERANCE,
        "models": model_results,
        "errors": model_errors,
        "weights_used": {
            endpoint["name"]: endpoint["weight"] for endpoint in MODEL_ENDPOINTS
        },
    }
