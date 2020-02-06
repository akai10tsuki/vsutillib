"""
qtUtils:

utility functions that use PySide2
"""


import platform


from PySide2.QtCore import Qt


from vsutillib.macos import isMacDarkMode


def checkColor(color):

    if color is None:

        if isMacDarkMode() or (platform.system() == "Windows"):
            color = Qt.white
        else:
            color = Qt.black

    # elif isMacDarkMode() or (platform.system() == "Windows"):

    #    if color == Qt.red:
    #        color = Qt.magenta
    #    elif color == Qt.darkGreen:
    #        color = Qt.green
    #    elif color == Qt.blue:
    #        color = Qt.cyan

    return color
