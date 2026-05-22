import psutil
from pynvml import *

# ======================================================
# RAM USAGE
# ======================================================

def get_ram_usage():

    memory = psutil.virtual_memory()

    return {

        "total_gb": round(memory.total / (1024**3), 2),

        "used_gb": round(memory.used / (1024**3), 2),

        "percent": memory.percent
    }

# ======================================================
# CPU USAGE
# ======================================================

def get_cpu_usage():

    return psutil.cpu_percent(interval=0.5)


# ======================================================
# GPU INFO
# ======================================================

def get_gpu_usage():

    try:

        nvmlInit()

        handle = nvmlDeviceGetHandleByIndex(0)

        memory = nvmlDeviceGetMemoryInfo(handle)

        utilization = nvmlDeviceGetUtilizationRates(
            handle
        )

        return {

            "gpu_percent": utilization.gpu,

            "memory_percent": utilization.memory,

            "memory_used_mb":
                round(memory.used / (1024**2), 2),

            "memory_total_mb":
                round(memory.total / (1024**2), 2)
        }

    except:

        return {

            "gpu_available": False
        }