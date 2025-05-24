def is_nuitka():
    # Check if the code is being run by Nuitka
    return globals().get("__compiled__", False)
