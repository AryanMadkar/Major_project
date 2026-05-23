import time

class Timer:

    def __init__(self, name="Timer"):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        print(f"[{self.name}] {(end - self.start):.4f} sec")
