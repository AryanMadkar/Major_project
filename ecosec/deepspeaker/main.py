import os

from flask import Flask

from app.api.routes import api
from app.core.logger import logger
from app.monitoring.health import health
from app.middleware.request_id import assign_request_id
from app.middleware.rate_limiter import enforce_rate_limit
from app.middleware.security_headers import apply_security_headers

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

    return apply_security_headers(response)


# ======================================================
# RUN SERVER
# ======================================================

if __name__ == "__main__":

    logger.info("Started DeepSpeaker Server")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("DEEPSPEAKER_PORT", "8006")),
        debug=True,
    )
