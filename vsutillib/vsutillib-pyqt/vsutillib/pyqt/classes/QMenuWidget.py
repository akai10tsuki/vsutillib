"""
subclass of QMenu to save title
used in internationalization
"""

from PySide2.QtWidgets import QMenu


class QMenuWidget(QMenu):
    """Override QMenu __init__ to save title"""

    # title=None, titlePrefix=None, titleSuffix=None):
    def __init__(self, *args: str, **kwargs: str) -> None:

        titlePrefix = kwargs.pop("titlePrefix", None)
        titleSuffix = kwargs.pop("titleSuffix", None)
        margins = kwargs.pop("margins", None)
        # originalTitle = kwargs.pop("originalTitle", None)

        self.__originalTitle = None
        self.titlePrefix = "" if titlePrefix is None else titlePrefix
        self.titleSuffix = "" if titleSuffix is None else titleSuffix
        self.margins = "" if margins is None else margins

        newArgs = []
        for p in args:
            if isinstance(p, str):
                self.originalTitle = p
                p = self.lTitle
            newArgs.append(p)
        newArgs = tuple(newArgs)

        super().__init__(*newArgs, **kwargs)

    def setTitle(self, title: str, *args: str, **kwargs: str) -> None:

        if self.originalTitle is None:
            self.originalTitle = title

        super().setTitle(self.lTitle, *args, **kwargs)

    @property
    def lTitle(self) -> str:
        return (
            self.margins
            + self.titlePrefix
            + _(self.originalTitle)
            + self.titleSuffix
            + self.margins
        )

    @property
    def originalTitle(self) -> str:
        return self.__originalTitle

    @originalTitle.setter
    def originalTitle(self, value: str) -> None:
        if isinstance(value, str):
            self.__originalTitle = value

    def setLanguage(self) -> None:
        if self.originalTitle is not None:
            super().setTitle(self.lTitle)


# This if for Pylance _() is not defined
def _(dummy: str) -> str:
    return dummy


del _
