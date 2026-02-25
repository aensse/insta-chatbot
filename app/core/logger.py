import logging

from rich.logging import RichHandler

logging.getLogger("uvicorn").handlers.clear()

def setup_logging():
    logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
