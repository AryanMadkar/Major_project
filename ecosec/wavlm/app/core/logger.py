import logging

from logging.handlers import RotatingFileHandler

from app.core.config import LOG_DIR

# ======================================================
# LOGGER
# ======================================================

logger = logging.getLogger("wavlm_server")

logger.setLevel(logging.INFO)

# ======================================================
# FORMATTER
# ======================================================

formatter = logging.Formatter(

    "[%(asctime)s] "
    "[%(levelname)s] "
    "%(message)s"
)

# ======================================================
# FILE HANDLER
# ======================================================

file_handler = RotatingFileHandler(

    LOG_DIR / "server.log",

    maxBytes=10 * 1024 * 1024,

    backupCount=5
)

file_handler.setFormatter(formatter)

# ======================================================
# CONSOLE HANDLER
# ======================================================

console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)

# ======================================================
# ADD HANDLERS
# ======================================================

logger.addHandler(file_handler)

logger.addHandler(console_handler)