"""Application entrypoint for Streamlit UI."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from dco_project.config.logging import get_logger, setup_logging
from dco_project.ui.streamlit_app import run_app

setup_logging()
logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info("Starting DCO application")
    run_app()
