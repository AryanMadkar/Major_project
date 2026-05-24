import json
from pathlib import Path


EMBEDDING_DIR = Path(
    "embeddings"
)

EMBEDDING_DIR.mkdir(
    exist_ok=True
)


def save_identity(
    user_id,
    embedding
):

    save_path = (
        EMBEDDING_DIR /
        f"{user_id}.json"
    )

    with open(
        save_path,
        "w"
    ) as f:

        json.dump({
            "user_id": user_id,
            "embedding": embedding
        }, f)


def load_identity(
    user_id
):

    save_path = (
        EMBEDDING_DIR /
        f"{user_id}.json"
    )

    if not save_path.exists():
        return None

    with open(
        save_path,
        "r"
    ) as f:

        return json.load(f)