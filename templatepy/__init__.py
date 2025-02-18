__author__ = "Lars B. Rollik"
__version__ = "0.2.7"

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("templatepy")
except PackageNotFoundError:
    # package is not installed
    pass

def run():
    """Example `run` function for entrypoint in `setup.cfg`"""
    print("Hello, world!")
