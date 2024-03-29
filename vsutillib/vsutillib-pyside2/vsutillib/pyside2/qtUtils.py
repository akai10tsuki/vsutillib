"""
qtUtils:

utility functions that use PySide2
"""


import logging

from typing import Any, Callable, Optional

from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QPushButton,
    QWidget,
    QToolTip,
)

from vsutillib.system import isMacDarkMode

from .classes import QRunInThread, SvgColor

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


# def centerWidget(widget: QWidget, parent: Optional[QWidget] = None) -> None:
def centerWidget(widget: QWidget, parent: Optional[QWidget] = None) -> None:
    """center widget based on parent or screen geometry"""

    if parent is None:
        parent = widget.parentWidget()

    if parent:
        widget.move(parent.frameGeometry().center() - widget.frameGeometry().center())

    else:
        widget.move(
            QDesktopWidget().availableGeometry().center()
            - widget.frameGeometry().center()
        )

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


def pushButton(label: str, function: Callable[..., None], tooltip: str) -> QPushButton:
    """
    pushButton convenience function for QPushButton definitions

    Args:
        label (str): label for push button
        function (func): function to execute when clicked
        tooltip (str): tool tip for push button

    Returns:
        QPushButton: PySide2 QPushButton
    """

    button = QPushButton(label)
    button.resize(button.sizeHint())
    button.clicked.connect(function)
    button.setToolTip(tooltip)

    return button


def darkPalette(app: Optional[QApplication] = None) -> QPalette:

    palette = QPalette()

    darkColor = QColor(45, 45, 45)
    disabledColor = QColor(127, 127, 127)

    palette.setColor(QPalette.AlternateBase, darkColor)
    palette.setColor(QPalette.Background, darkColor)
    palette.setColor(QPalette.Base, QColor(18, 18, 18))
    palette.setColor(QPalette.BrightText, SvgColor.red)
    palette.setColor(QPalette.Button, darkColor)
    palette.setColor(QPalette.ButtonText, SvgColor.white)
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, disabledColor)
    palette.setColor(QPalette.Disabled, QPalette.HighlightedText, disabledColor)
    palette.setColor(QPalette.Disabled, QPalette.Text, disabledColor)
    palette.setColor(QPalette.Disabled, QPalette.WindowText, disabledColor)
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, SvgColor.black)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Text, SvgColor.white)
    palette.setColor(QPalette.ToolTipBase, SvgColor.white)
    palette.setColor(QPalette.ToolTipText, SvgColor.white)
    palette.setColor(QPalette.Window, darkColor)
    palette.setColor(QPalette.WindowText, SvgColor.white)

    if app is not None:
        app.setStyle("Fusion")
        app.setPalette(palette)

        toolTipPalette = QPalette()
        toolTipPalette.setColor(QPalette.Inactive, QPalette.ToolTipText, SvgColor.white)
        toolTipPalette.setColor(
            QPalette.Inactive, QPalette.ToolTipBase, QColor(42, 130, 218)
        )
        QToolTip.setPalette(toolTipPalette)

    return palette


def qtRunFunctionInThread(
    function: Callable[..., None], *args: Any, **kwargs: Any
) -> None:
    """
    Pass the function to execute Other args,
    kwargs are passed to the run function
    """

    #
    # Expected callback functions
    #
    funcStart = kwargs.pop("funcStart", None)
    funcFinished = kwargs.pop("funcFinished", None)
    funcResult = kwargs.pop("funcResult", None)

    worker = QRunInThread(function, *args, **kwargs)

    #
    # Connect expected callbacks with corresponding Signal
    #
    if funcStart is not None:
        worker.startSignal.connect(funcStart)
    if funcFinished is not None:
        worker.finishedSignal.connect(funcFinished)
    if funcResult is not None:
        worker.resultSignal.connect(funcResult)

    # Execute
    worker.run()
