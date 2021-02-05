"""
subclass of QPushButton to save text, shortcut and tooltip
this information is used for internationalization
"""

from PySide2.QtWidgets import QPushButton


class QPushButtonWidget(QPushButton):
    """
    QPushButton subclass of QAction save original shortcut and tooltip for locale application

    Args:
        shortcut (str, optional): original shortcut string representation. Defaults to None.
        tooltip (str, optional): original tooltip. Defaults to None.
    """

    # def __init__(self, *args, function=None, toolTip=None, originalText=None, **kwargs):

    def __init__(self, *args: str, **kwargs: str) -> None:

        function = kwargs.pop("function", None)
        margins = kwargs.pop("margins", None)
        # originalText = kwargs.pop("originalText", None)
        textPrefix = kwargs.pop("textPrefix", None)
        textSuffix = kwargs.pop("textSuffix", None)
        toolTip = kwargs.pop("toolTip", None)

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

        self.toolTip = toolTip

        if function is not None:
            self.clicked.connect(function)

        if toolTip is not None:
            self.setToolTip(toolTip)

    def setToolTip(self, toolTip: str, *args: str, **kwargs: str) -> None:

        if self.toolTip is not None:
            self.toolTip = toolTip

        super().setToolTip(_(toolTip), *args, **kwargs)

    def setText(self, text: str, *args: str, **kwargs: str) -> None:

        if self.originalText is None:
            self.originalText = text

        super().setText(self.lText, *args, **kwargs)

    @property
    def originalText(self) -> str:
        return self.__originalText

    @originalText.setter
    def originalText(self, value: str) -> None:
        if isinstance(value, str):
            self.__originalText = value

    @property
    def lText(self) -> str:
        return (
            self.margins
            + self.textPrefix
            + _(self.originalText)
            + self.textSuffix
            + self.margins
        )

    def setLanguage(self) -> None:
        if self.toolTip is not None:
            super().setToolTip(_(self.toolTip))

        if self.originalText is not None:
            super().setText(self.lText)

# This if for Pylance _() is not defined
def _(dummy: str) -> str:
    return dummy


del _
