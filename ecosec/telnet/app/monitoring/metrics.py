from prometheus_client import (
    Counter,
    Histogram
)

# ======================================================
# REQUEST COUNT
# ======================================================

REQUEST_COUNT = Counter(

    "verify_requests_total",

    "Total verification requests"
)

# ======================================================
# REQUEST LATENCY
# ======================================================

REQUEST_LATENCY = Histogram(

    "verify_request_latency_seconds",

    "Verification latency"
)