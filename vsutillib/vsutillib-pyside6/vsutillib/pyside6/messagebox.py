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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractButton, QMessageBox, QWidget


def messageBox(
        widget: QWidget,
        title: str,
        text: str,
        icon: QIcon = QMessageBox.Information) -> QAbstractButton:
    """
    Working on generic message box
    """

    m = QMessageBox(widget)
    m.setWindowTitle(title)
    m.setText(text)
    m.setIcon(icon)
    m.setDefaultButton(QMessageBox.Ok)
    m.setFont(widget.font())
    m.exec()

    return QMessageBox.Ok


def messageBoxYesNo(
        widget: QWidget,
        title: str,
        text: str,
        icon: QIcon) -> QAbstractButton:
    """
    Yes | No message box
    """

    m = QMessageBox(widget)
    m.setWindowTitle(title)
    m.setText(text)
    m.setIcon(icon)
    yesButton = m.addButton(_("Yes"), QMessageBox.ButtonRole.YesRole)
    noButton = m.addButton(_("No"), QMessageBox.ButtonRole.NoRole)
    m.setDefaultButton(noButton)
    m.setFont(widget.font())
    m.exec()

    if m.clickedButton() == yesButton:
        return QMessageBox.Yes

    return QMessageBox.No


def _(dummy):
    return dummy


del _
