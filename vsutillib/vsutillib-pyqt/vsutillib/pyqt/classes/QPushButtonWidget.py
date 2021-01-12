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

    def __init__(self, *args, function=None, toolTip=None, originalText=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.__originalText = None

        if originalText is not None:
            self.originalText = originalText
        else:
            for p in args:
                if isinstance(p, str):
                    # Save first string found assume is the button label
                    self.originalText = p
                    break

        self.toolTip = toolTip

        if function is not None:
            self.clicked.connect(function)

        if toolTip is not None:
            self.setToolTip(toolTip)

    def setToolTip(self, toolTip, *args, **kwargs):

        if self.toolTip is None:
            self.toolTip = toolTip

        super().setToolTip(toolTip, *args, **kwargs)

    def setText(self, text, *args, **kwargs):

        if self.originalText is None:
            self.originalText = text

        super().setText(text, *args, **kwargs)

    @property
    def originalText(self):
        return self.__originalText

    @originalText.setter
    def originalText(self, value):
        if isinstance(value, str):
            self.__originalText = value
