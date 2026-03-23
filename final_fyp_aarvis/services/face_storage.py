"""Face embedding storage."""

from __future__ import annotations

import pickle
from pathlib import Path

from final_fyp_aarvis.config.settings import FACE_DB_FILE


def load_face_database(file_path: Path = FACE_DB_FILE) -> dict:
    """Load face embeddings."""
    if file_path.exists():
        try:
            with open(file_path, "rb") as file_obj:
                return pickle.load(file_obj)
        except Exception:
            return {}
    return {}


def save_face_database(database: dict, file_path: Path = FACE_DB_FILE) -> None:
    """Save face embeddings."""
    with open(file_path, "wb") as file_obj:
        pickle.dump(database, file_obj)
