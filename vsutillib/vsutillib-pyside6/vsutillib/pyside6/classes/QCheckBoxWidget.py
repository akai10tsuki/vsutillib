"""
subclass of QCheckBox to save text
used in internationalization
"""

from PySide6.QtWidgets import QCheckBox


class QCheckBoxWidget(QCheckBox):
    """Override QCheckBox __init__ to save text"""

    # text=None, textPrefix=None, textSuffix=None):
    def __init__(self, *args: str, **kwargs: str) -> None:

        textPrefix = kwargs.pop("textPrefix", None)
        textSuffix = kwargs.pop("textSuffix", None)
        margins = kwargs.pop("margins", None)

        self.__originalText = None
        self.textPrefix = "" if textPrefix is None else textPrefix
        self.textSuffix = "" if textSuffix is None else textSuffix
        self.margins = "" if margins is None else margins

        newArgs = []
        for p in args:
            if isinstance(p, str):
                self.originalText = p
                p = self.ckbText
            newArgs.append(p)
        newArgs = tuple(newArgs)

        super().__init__(*newArgs, **kwargs)

    def setText(self, text: str, *args: str, **kwargs: str) -> None:

        if self.originalText is None:
            self.originalText = text

        super().setText(self.ckbText, *args, **kwargs)

    @property
    def ckbText(self) -> str:
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

    def translate(self) -> None:
        if self.originalText is not None:
            super().setText(self.ckbText)


# This if for Pylance _() is not defined
def _(dummy: str) -> str:
    return dummy


del _
