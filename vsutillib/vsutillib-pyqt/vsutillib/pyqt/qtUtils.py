"""
qtUtils:

utility functions that use PySide2
"""


import logging

from PySide2.QtWidgets import QDesktopWidget, QPushButton


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


def centerWidgets(widget, parent=None):
    """center widget based on parent or screen geometry"""

    if parent is None:
        parent = widget.parentWidget()

    if parent:
        widget.move(parent.frameGeometry().center() - widget.frameGeometry().center())

    else:
        widget.move(QDesktopWidget().availableGeometry().center() - widget.frameGeometry().center())

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
