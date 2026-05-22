from flask import Blueprint, jsonify

import torch

from app.monitoring.system import (
    get_ram_usage,
    get_cpu_usage,
    get_gpu_usage
)

health = Blueprint("health", __name__)

# ======================================================
# HEALTH
# ======================================================

@health.route("/health", methods=["GET"])
def health_check():

    return jsonify({

        "status": "healthy",

        "gpu_available":
            torch.cuda.is_available(),

        "cpu_percent":
            get_cpu_usage(),

        "ram":
            get_ram_usage(),

        "gpu":
            get_gpu_usage()
    })