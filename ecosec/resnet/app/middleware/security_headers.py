# ======================================================
# SECURITY HEADERS
# ======================================================

def apply_security_headers(response):

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "Cache-Control"
    ] = "no-store"

    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000"

    return response