import platform
import shutil
from pathlib import Path

from loguru import logger

from utils.is_nuitka import is_nuitka


def get_mitmdump_path():
    if is_nuitka():
        # Use the __nuitka_binary_dir from globals to find mitmdump
        mitmdump_dir = Path(globals().get("__nuitka_binary_dir", "")).resolve()
        mitmdump_path = mitmdump_dir.joinpath("mitmdump").resolve()

        if platform.system() == "Windows":
            mitmdump_path = mitmdump_path.with_suffix(".exe")

        if mitmdump_path.exists():
            logger.debug(f"mitmdump path: {mitmdump_path}")
            return str(mitmdump_path)

    # get the path to the project root
    path = Path(__file__).parent.parent.parent
    # Find the path to the mitmdump executable
    mitmdump_path = shutil.which("mitmdump", path=path)

    if platform.system() == "Windows" and mitmdump_path is None:
        mitmdump_path = shutil.which("mitmdump.exe", path=path)

    logger.debug(f"mitmdump path: {mitmdump_path}")
    return mitmdump_path
