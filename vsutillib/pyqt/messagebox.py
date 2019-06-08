from PySide2.QtWidgets import QMessageBox

def messageBoxYesNo(self, title, text, icon):

    """
    Save window state before exit
    """

    m = QMessageBox(self)
    m.setWindowTitle(title)
    m.setText(text)
    m.setIcon(icon)
    yesButton = m.addButton('Yes', QMessageBox.ButtonRole.YesRole)
    noButton = m.addButton(' No ', QMessageBox.ButtonRole.NoRole)
    m.setDefaultButton(noButton)
    m.setFont(self.font())
    m.exec_()

    if m.clickedButton() == yesButton:
        return QMessageBox.Yes

    return QMessageBox.No
