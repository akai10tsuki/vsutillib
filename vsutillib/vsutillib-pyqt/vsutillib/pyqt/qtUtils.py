"""
qtUtils:

utility functions that use PySide2
"""


import logging

from PySide2.QtWidgets import QDesktopWidget


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
