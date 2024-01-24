"""
subclass of QMenu to save text
used in internationalization
"""

from typing import Any

from PySide2.QtWidgets import QLabel


class QLabelWidget(QLabel):
    """Override QLabel __init__ to save text"""

    # text=None, textPrefix=None, textSuffix=None):
    def __init__(self, *args: str, **kwargs: str) -> None:

        textPrefix = kwargs.pop("textPrefix", None)
        textSuffix = kwargs.pop("textSuffix", None)
        margins = kwargs.pop("margins", None)
        # originalText = kwargs.pop("originalText", None)

        self.__originalText = None
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

    def setText(self, text: str, *args: str, **kwargs: str) -> None:

        if self.originalText is None:
            self.originalText = text

        super().setText(self.lText, *args, **kwargs)

    @property
    def lText(self) -> str:
        return (
            self.margins
            + self.textPrefix
            + _(self.originalText)
            + self.textSuffix
            + self.margins
        )

    @property
    def originalText(self) -> str:
        return self.__originalText

    @originalText.setter
    def originalText(self, value: str) -> None:
        if isinstance(value, str):
            self.__originalText = value

    def setLanguage(self) -> None:
        if self.originalText is not None:
            super().setText(self.lText)


# This if for Pylance _() is not defined
def _(dummy: str) -> str:
    return dummy


del _
