from app.core.logger import logger

# ======================================================
# SUSPICIOUS ACTIVITY
# ======================================================

def log_suspicious_activity(ip, reason):

    logger.warning(

        f"[SUSPICIOUS] "

        f"IP={ip} "

        f"REASON={reason}"
    )