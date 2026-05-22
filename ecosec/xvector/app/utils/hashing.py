import hashlib

# ======================================================
# FILE HASH
# ======================================================

def get_file_hash(path):

    """
    Generates MD5 hash for audio file.

    Used for embedding cache lookup.
    """

    md5 = hashlib.md5()

    with open(path, "rb") as f:

        while chunk := f.read(8192):

            md5.update(chunk)

    return md5.hexdigest()