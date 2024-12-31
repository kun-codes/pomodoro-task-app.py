import os
from pathlib import Path
import shutil

def is_nuitka():
    # Check if the code is being run by Nuitka
    return globals().get("__compiled__", False)

def get_mitmdump_path():
    print(f"globals: {globals()}")
    if is_nuitka():
        print("Running in Nuitka")
        # Use the __nuitka_binary_dir from globals to find mitmdump
        mitmdump_dir = Path(globals().get("__nuitka_binary_dir", "")).resolve()
        print(f"mitmdump:  {mitmdump_dir}")
        mitmdump_path = mitmdump_dir.joinpath("mitmdump").resolve()
        print(f"mitmdump:  {mitmdump_path}")

        if mitmdump_path.exists():
            print(mitmdump_path)
            return str(mitmdump_path)

    print("Not Running in Nuitka")
    # get the path to the project root
    path = Path(__file__).parent.parent.parent
    print(f"path: {path}")
    # Find the path to the mitmdump executable
    mitmdump_path = shutil.which("mitmdump", path=path)
    print(f"mitmdump: {mitmdump_path}")

    return mitmdump_path