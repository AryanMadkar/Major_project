import time
from collections import defaultdict, deque
from threading import Lock

from flask import request

from app.core.config import RATE_LIMIT_PER_MINUTE
from app.core.logger import logger
from app.utils.responses import error_response

_WINDOW_SECONDS = 60
_REQUEST_TIMES = defaultdict(deque)
_LOCK = Lock()


def _get_client_ip():

    forwarded = request.headers.get("X-Forwarded-For", "")

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.remote_addr or "unknown"


def enforce_rate_limit():

    now = time.monotonic()
    window_start = now - _WINDOW_SECONDS
    client_ip = _get_client_ip()

    with _LOCK:

        timestamps = _REQUEST_TIMES[client_ip]

        while timestamps and timestamps[0] < window_start:
            timestamps.popleft()

        if len(timestamps) >= RATE_LIMIT_PER_MINUTE:

            logger.warning(
                f"[RATE_LIMIT] IP={client_ip} LIMIT={RATE_LIMIT_PER_MINUTE}/min"
            )

            return error_response("rate limit exceeded", status=429)

        timestamps.append(now)

    return None
