"""
qtUtils:

utility functions that use PySide2
"""


import logging

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QDesktopWidget, QPushButton, QToolTip

from .classes import RunInThread

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


def centerWidgets(widget, parent=None):
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


def pushButton(label, function, tooltip):
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


def darkPalette():
    """
    darkPalette palette to change to a dark theme
    """

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.cyan)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, Qt.darkCyan)  # QColor(42, 130, 218)
    palette.setColor(QPalette.HighlightedText, Qt.white)
    palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)

    toolTipPalette = QPalette()
    toolTipPalette.setColor(
        QPalette.Inactive, QPalette.ToolTipBase, Qt.lightGray
    )  # QColor(53, 53, 53)
    toolTipPalette.setColor(QPalette.Inactive, QPalette.ToolTipText, Qt.black)

    QToolTip.setPalette(toolTipPalette)

    return palette


def runFunctionInThread(function, *args, **kwargs):
    """
    Pass the function to execute Other args,
    kwargs are passed to the run function
    """

    worker = RunInThread(function, *args, **kwargs)

    # Execute
    worker.run()
