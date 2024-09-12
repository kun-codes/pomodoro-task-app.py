import os
import sys
import shutil

def get_mitmdump_path():
    # Get the path to the Python interpreter in the virtual environment
    venv_path = os.path.dirname(sys.executable)

    # Find the path to the mitmdump executable within the virtual environment
    mitmdump_path = shutil.which("mitmdump", path=venv_path)

    return mitmdump_path