import sys


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000
