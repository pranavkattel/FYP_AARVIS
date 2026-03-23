"""Project paths."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
FACE_DB_FILE = BASE_DIR / "face_database.pkl"
