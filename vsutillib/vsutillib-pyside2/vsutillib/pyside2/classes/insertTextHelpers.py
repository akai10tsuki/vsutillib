"""
qtUtils:

utility functions that use PySide2
"""

from PySide2.QtGui import QColor

from vsutillib.system import isMacDarkMode

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

        if isMacDarkMode() or isDarkMode:
            color = SvgColor.white
        else:
            color = SvgColor.black

    elif isMacDarkMode():

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
