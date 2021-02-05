"""
QDarkPalette class
"""

from PySide2.QtGui import QBrush, QPalette, QColor
from PySide2.QtWidgets import QApplication


BLACK: QColor = QColor(0, 0, 0)
RED: QColor = QColor(255, 0, 0)
WHITE: QColor = QColor(255, 255, 255)

BASE: QColor = QColor(18, 18, 18)
DISABLED: QColor = QColor(127, 127, 127)
PRIMARY: QColor = QColor(45, 45, 45)
SECONDARY: QColor = QColor(18, 18, 18)
TERTIARY: QColor = QColor(42, 130, 218)


def css_rgb(color: QColor, a: bool = False):
    """Get a CSS `rgb` or `rgba` string from a `QtGui.QColor`."""

    return ("rgba({}, {}, {}, {})" if a else "rgb({}, {}, {})").format(*color.getRgb())


class QDarkPalette(QPalette):
    """Dark palette for a Qt application meant to be used with the Fusion theme."""

    def __init__(self, *args: QBrush) -> None:
        super().__init__(*args)

        # Set all the colors based on the constants in globals
        self.setColor(QPalette.AlternateBase, PRIMARY)
        self.setColor(QPalette.Background, PRIMARY)
        self.setColor(QPalette.Base, SECONDARY)
        self.setColor(QPalette.BrightText, RED)
        self.setColor(QPalette.Button, PRIMARY)
        self.setColor(QPalette.ButtonText, WHITE)
        self.setColor(QPalette.Disabled, QPalette.ButtonText, DISABLED)
        self.setColor(QPalette.Disabled, QPalette.HighlightedText, DISABLED)
        self.setColor(QPalette.Disabled, QPalette.Text, DISABLED)
        self.setColor(QPalette.Disabled, QPalette.WindowText, DISABLED)
        self.setColor(QPalette.Highlight, TERTIARY)
        self.setColor(QPalette.HighlightedText, BLACK)
        self.setColor(QPalette.Link, TERTIARY)
        self.setColor(QPalette.Text, WHITE)
        self.setColor(QPalette.ToolTipBase, WHITE)
        self.setColor(QPalette.ToolTipText, WHITE)
        self.setColor(QPalette.Window, PRIMARY)
        self.setColor(QPalette.WindowText, WHITE)

    @staticmethod
    def setStyleSheet(app: QApplication) -> None:
        """Static method to set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet(
            "QToolTip {{"
            "color: {white};"
            "background-color: {tertiary};"
            "border: 1px solid {white};"
            "}}".format(white=css_rgb(WHITE), tertiary=css_rgb(TERTIARY))
        )

    def setA36pp(self, app: QApplication) -> None:
        """Set the Fusion theme and this palette to a `QtWidgets.QApplication`."""

        app.setStyle("Fusion")
        app.setPalette(self)
        self.set_stylesheet(app)
