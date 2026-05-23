import os

from flask import Flask

from app.api.routes import api
from app.core.logger import logger
from app.monitoring.health import health
from app.middleware.security_headers import (
    apply_security_headers
)

from app.middleware.request_id import (
    assign_request_id
)
from app.middleware.rate_limiter import (
    enforce_rate_limit
)
# ======================================================
# CREATE FLASK APP
# ======================================================

app = Flask(__name__)

# ======================================================
# REGISTER ROUTES
# ======================================================

app.register_blueprint(api)
app.register_blueprint(health)

@app.before_request
def before_request():

    assign_request_id()

    rate_limit_response = enforce_rate_limit()

    if rate_limit_response is not None:
        return rate_limit_response
    
@app.after_request
def after_request(response):

    return apply_security_headers(
        response
    )

# ======================================================
# RUN SERVER
# ======================================================

if __name__ == "__main__":
    
    # Clean up temp folder on startup
    from app.core.config import TEMP_DIR
    if TEMP_DIR.exists():
        for item in TEMP_DIR.iterdir():
            try:
                if item.is_file():
                    item.unlink()
            except Exception:
                pass

    logger.info("Started ECAPA Server")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("ESPACA_PORT", "8000")),
        debug=True,
        use_reloader=False
    )
    