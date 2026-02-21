__author__ = "Lars B. Rollik"

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

try:
    __version__ = version(Path(__file__).parent.name)
except PackageNotFoundError:
    __version__ = "0.2.9"


def run():
    """Example `run` function for entrypoint defined in `pyproject.toml`."""
    print("Hello, world!")
