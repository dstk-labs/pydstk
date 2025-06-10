import pathlib

# Get the directory of the current file (__init__.py)
_PACKAGE_DIR = pathlib.Path(__file__).resolve().parent

try:
    with open(_PACKAGE_DIR / "VERSION") as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = "0.0.0.dev0"  # Fallback version if VERSION file is not found
