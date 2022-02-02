"""
subclass of QAction to save text, shortcut and tooltip
this information is used for internationalization
"""

from PySide6.QtGui import QAction


class QActionWidget(QAction):
    """
    QActionWidget subclass of QAction save original shortcut and tooltip for
    locale application

    Args:
        shortcut (str, optional): original shortcut string representation.
        Defaults to None.

        tooltip (str, optional): original tooltip. Defaults to None.
    """

    def __init__(self, *args: str, **kwargs: str) -> None:

        textPrefix = kwargs.pop("textPrefix", None)
        textSuffix = kwargs.pop("textSuffix", None)
        shortcut = kwargs.pop("shortcut", None)
        toolTip = kwargs.pop("toolTip", None)
        statusTip = kwargs.pop("statusTip", None)
        margins = kwargs.pop("margins", None)

        self.textPrefix = "" if textPrefix is None else textPrefix
        self.textSuffix = "" if textSuffix is None else textSuffix
        self.margins = "" if margins is None else margins

        newArgs = []
        for p in args:
            if isinstance(p, str):
                self.originalText = p
                p = self.lText
            newArgs.append(p)
        newArgs = tuple(newArgs)

        super().__init__(*newArgs, **kwargs)

        self.shortcut = shortcut
        self.toolTip = toolTip
        self.statusTip = statusTip

        if shortcut is not None:
            self.setShortcut(shortcut)

        if toolTip is not None:
            self.setToolTip(toolTip)

        if statusTip is not None:
            self.setStatusTip(statusTip)

    def setShortcut(self, shortcut: str, *args: str, **kwargs: str) -> str:

        if self.shortcut is None:
            self.shortcut = shortcut

        super().setShortcut(_(shortcut), *args, **kwargs)

    def setStatusTip(self, statusTip: str, *args: str, **kwargs: str) -> None:

        if self.statusTip is None:
            self.statusTip = statusTip

        super().setStatusTip(_(statusTip), *args, **kwargs)

    def setText(self, text: str, *args: str, **kwargs: str) -> str:

        if self.originalText is None:
            self.originalText = text

        super().setText(self.lText, *args, **kwargs)

    def setToolTip(self, toolTip: str, *args: str, **kwargs: str) -> None:

        if self.toolTip is None:
            self.toolTip = toolTip

        super().setToolTip(_(toolTip), *args, **kwargs)

    @property
    def lText(self) -> str:
        return (
            self.margins
            + self.textPrefix
            + _(self.originalText)
            + self.textSuffix
            + self.margins
        )

    def translate(self) -> None:
        """Set language for widget labels"""

        if self.toolTip is not None:
            super().setToolTip(_(self.toolTip))

        if self.originalText is not None:
            super().setText(self.lText)

        if self.statusTip is not None:
            super().setStatusTip(_(self.statusTip))

        if self.shortcut is not None:
            super().setShortcut(_(self.shortcut))


# This if for Pylance _() is not defined
def _(dummy: str) -> str:
    return dummy


del _
