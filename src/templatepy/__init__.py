from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("templatepy")
except PackageNotFoundError:
    __version__ = "unknown"
