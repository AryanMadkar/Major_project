from flask import Flask

from app.api.routes import api
from app.core.logger import logger
# ======================================================
# CREATE FLASK APP
# ======================================================

app = Flask(__name__)

# ======================================================
# REGISTER ROUTES
# ======================================================

app.register_blueprint(api)


# ======================================================
# RUN SERVER
# ======================================================

if __name__ == "__main__":
    
    logger.info("Started ECAPA Server")

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
    