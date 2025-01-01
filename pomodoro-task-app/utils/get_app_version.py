import tomllib
from pathlib import Path

from utils.is_nuitka import is_nuitka


def get_app_version():
    """Get version from pyproject.toml"""
    if is_nuitka():
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    else:
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)
    return pyproject["tool"]["poetry"]["version"]