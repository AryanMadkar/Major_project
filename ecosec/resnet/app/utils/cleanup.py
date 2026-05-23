import os

# ======================================================
# DELETE TEMP FILE
# ======================================================

def cleanup_file(path):

    try:

        if os.path.exists(path):

            os.remove(path)

    except Exception as e:

        print(f"[CLEANUP ERROR] {e}")