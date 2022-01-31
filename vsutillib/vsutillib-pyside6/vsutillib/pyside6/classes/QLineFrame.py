"""
 QFrame Lines for separators
"""

from typing import Optional

from PySide6.QtWidgets import QFrame, QWidget


class HorizontalLine(QFrame):
    """QFrame for an horizontal line"""
    def __init__(
            self,
            parent: Optional[QWidget] = None,
            width: int = 1) -> None:
        super().__init__(parent)

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(width)


class VerticalLine(QFrame):
    """QFrame for a vertical line"""
    def __init__(
            self,
            parent: Optional[QWidget] = None,
            width: int = 1) -> None:
        super().__init__(parent)

        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(width)
