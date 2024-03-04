"""
qtUtils:

utility functions that use PySide2
"""

from PySide6.QtGui import QColor

from vsutillib.system import isSystemInDarkMode

from .SvgColor import SvgColor


def checkColor(color: QColor, isDarkMode: bool = False) -> QColor:
    """
    checkColor change color according to dark or light mode

    Args:
        color (SvgColor): color code
        isDarkMode (bool, optional): True if using dark mode on Windows. Defaults to False.

    Returns:
        [type]: [description]
    """

    if color is None:

        if isSystemInDarkMode() or isDarkMode:
            color = SvgColor.white
        else:
            color = SvgColor.black

    elif isSystemInDarkMode():

        if color == SvgColor.red:
            color = SvgColor.magenta
        elif color == SvgColor.darkgreen:
            color = SvgColor.green
        elif color == SvgColor.blue:
            color = SvgColor.cyan

    elif not isDarkMode:

        if color == SvgColor.cyan:
            color = SvgColor.dodgerblue
        elif color == QColor(42, 130, 218):
            color = SvgColor.dodgerblue

    return color


class LineOutput:

    Color: str = "color"
    ReplaceLine: str = "replaceLine"
    AppendLine: str = "appendLine"
    AppendEnd: str = "appendEnd"
    LogOnly: str = "logOnly"
