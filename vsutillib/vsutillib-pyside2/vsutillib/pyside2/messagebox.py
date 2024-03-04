"""
function for QMessageBox Yes|No needed for change
font on the fly and localization

Args:
    self (QWidget): parent QWidget
    tittle (str): tittle for QMessageBox
    text (str): text for QMessageBox
    icon (QIcon): standard icons for QMessageBox
        question mark, warning ...
Returns:
    QMessageBox.button: standard QMessageBox button

"""

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAbstractButton, QWidget, QMessageBox


def messageBox(
    self: QWidget, title: str, text: str, icon: QIcon = QMessageBox.Information
) -> QAbstractButton:
    """
    Working on generic message box
    """

    m = QMessageBox(self)
    m.setWindowTitle(title)
    m.setText(text)
    m.setIcon(icon)
    m.setDefaultButton(QMessageBox.Ok)
    m.setFont(self.font())
    m.exec()

    return QMessageBox.Ok


def messageBoxYesNo(
    self: QWidget, title: str, text: str, icon: QIcon
) -> QAbstractButton:
    """
    Yes | No message box
    """

    m = QMessageBox(self)
    m.setWindowTitle(title)
    m.setText(text)
    m.setIcon(icon)
    yesButton = m.addButton("Yes", QMessageBox.ButtonRole.YesRole)
    noButton = m.addButton("No", QMessageBox.ButtonRole.NoRole)
    m.setDefaultButton(noButton)
    m.setFont(self.font())
    m.exec()

    if m.clickedButton() == yesButton:
        return QMessageBox.Yes

    return QMessageBox.No
