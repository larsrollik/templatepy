__author__ = "Lars B. Rollik"

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("subject_weight_db")
except PackageNotFoundError:
    __version__ = "0.2.8.dev0"


def run():
    """Example `run` function for entrypoint defined in `pyproject.toml`."""
    print("Hello, world!")
