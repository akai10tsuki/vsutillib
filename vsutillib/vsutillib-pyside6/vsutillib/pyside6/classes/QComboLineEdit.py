"""
ComboBox sub-class of QComboBox permits removal of highlighted item in the popup
    list with Del key
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal, Slot, QObject, QEvent
from PySide6.QtWidgets import QApplication, QComboBox, QWidget


class QComboLineEdit(QComboBox):
    """
    ComboBox removes highlighted item in popup with Del key

    Args:
        parent (QWidget): parent widget
        popup (bool): confirm removal if True. No confirmation otherwise.
    """

    itemsChangeSignal = Signal()

    def __init__(
            self,
            parent: Optional[QWidget] = None,
            popup: bool = False) -> None:
        super().__init__()

        self.__tab = None
        self.__popup = None
        self.__doPopup = popup
        self.__highlighted = None
        self.parent = parent
        self.view().installEventFilter(self)
        self.highlighted.connect(self.saveHighlighted)
        self.setEditable(True)
        self.lineEdit().setClearButtonEnabled(True)

    def isPopup(self) -> bool:
        return self.__popup

    def showPopup(self) -> None:

        self.__popup = True
        super().showPopup()

    def hidePopup(self) -> None:

        self.__popup = False
        super().hidePopup()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:

        if obj == self.view():
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Delete:
                    if self.__highlighted is not None:
                        index = self.__highlighted
                        self.removeItem(index)
                        self.itemsChangeSignal.emit()
                        return True
            return False

        return QObject.eventFilter(self, obj, event)

    def keyPressEvent(self, event: QEvent) -> None:

        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ControlModifier:
                QComboBox.keyPressEvent(self, event)
                self.itemsChangeSignal.emit()
        else:
            QComboBox.keyPressEvent(self, event)

    @Slot(int)
    def saveHighlighted(self, index: int) -> None:

        self.__highlighted = index
