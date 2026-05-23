import os
import time
import gc

# ======================================================
# DELETE TEMP FILE WITH RETRIES AND FORCE GC
# ======================================================

def cleanup_file(path):
    if not path:
        return

    # Try deleting the file with a retry loop to handle Windows file locking
    for attempt in range(5):
        try:
            if os.path.exists(path):
                os.remove(path)
            return  # Successfully removed or file doesn't exist
        except Exception as exc:
            # Force garbage collection to release any lingering handles (e.g. from torchaudio/soundfile)
            gc.collect()
            time.sleep(0.1)

    # Final attempt to delete, letting any exception raise or print
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as exc:
        print(f"[CLEANUP ERROR] Failed to delete temporary file {path} after retries: {exc}")

