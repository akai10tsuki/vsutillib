"""
subclass of QMenu to save title
used in internationalization
"""

from PySide2.QtWidgets import QMenu

class QMenuWidget(QMenu):
    """Override QMenu __init__ to save title"""

    # title=None, titlePrefix=None, titleSuffix=None):
    def __init__(self, *args, **kwargs):

        titlePrefix = kwargs.pop("textPrefix", None)
        titleSuffix = kwargs.pop("textSuffix", None)

        super().__init__(*args, **kwargs)

        for p in args:
            if isinstance(p, str):
                self.originalTitle = p

        #self.originalTitle = title

        self.titlePrefix = "" if titlePrefix is None else titlePrefix
        self.titleSuffix = "" if titleSuffix is None else titleSuffix

    def setTitle(self, title, *args, **kwargs):

        if self.originalTitle is None:
            self.originalTitle = title

        super().setTitle(title, *args, **kwargs)
