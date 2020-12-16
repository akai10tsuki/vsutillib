"""
subclass of QAction to save text, shortcut and tooltip
this information is used for internationalization
"""

from PySide2.QtWidgets import QAction


class QActionWidget(QAction):
    """
    QActionWidget subclass of QAction save original shortcut and tooltip for locale application

    Args:
        shortcut (str, optional): original shortcut string representation. Defaults to None.
        tooltip (str, optional): original tooltip. Defaults to None.
    """

    def __init__(self, *args, **kwargs):

        textPrefix = kwargs.pop("textPrefix", None)
        textSuffix = kwargs.pop("textSuffix", None)
        shortcut = kwargs.pop("shortcut", None)
        toolTip = kwargs.pop("toolTip", None)
        statusTip = kwargs.pop("statusTip", None)

        super().__init__(*args, **kwargs)

        for p in args:
            if isinstance(p, str):
                self.originalText = p

        self.shortcut = shortcut
        self.toolTip = toolTip
        self.statusTip = statusTip
        self.textPrefix = "" if textPrefix is None else textPrefix
        self.textSuffix = "" if textSuffix is None else textSuffix

        if shortcut is not None:
            self.setShortcut(shortcut)

        if toolTip is not None:
            self.setToolTip(toolTip)

        if statusTip is not None:
            self.setStatusTip(statusTip)

    def setShortcut(self, shortcut, *args, **kwargs):

        if self.shortcut is None:
            self.shortcut = shortcut

        super().setShortcut(shortcut, *args, **kwargs)

    def setStatusTip(self, statusTip, *args, **kwargs):

        if self.statusTip is None:
            self.statusTip = statusTip

        super().setStatusTip(statusTip, *args, **kwargs)

    def setText(self, text, *args, **kwargs):

        if self.originalText is None:
            self.originalText = text

        super().setText(text, *args, **kwargs)

    def setToolTip(self, toolTip, *args, **kwargs):

        if self.toolTip is None:
            self.toolTip = toolTip

        super().setToolTip(toolTip, *args, **kwargs)
