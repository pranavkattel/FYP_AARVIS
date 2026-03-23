"""Run the FastAPI server for AARVIS."""

import os
import sys

import uvicorn

# If run as `python .\main.py` from inside final_fyp_aarvis,
# add the parent folder so absolute package imports work.
if __package__ in (None, ""):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from final_fyp_aarvis.api.server import app


def run() -> None:
    """Start the server on port 8000."""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    run()
