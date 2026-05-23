import os

# ======================================================
# DELETE TEMP FILE
# ======================================================

def cleanup_file(path):

    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as exc:
        print(f"[CLEANUP ERROR] {exc}")
