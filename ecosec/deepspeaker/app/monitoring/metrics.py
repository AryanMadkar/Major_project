from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("verify_requests_total", "Total verification requests")
REQUEST_LATENCY = Histogram("verify_request_latency_seconds", "Verification latency")
