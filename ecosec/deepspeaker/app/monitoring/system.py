import psutil

try:
    from pynvml import *
except Exception:
    pass

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_gpu_usage():
    return None
