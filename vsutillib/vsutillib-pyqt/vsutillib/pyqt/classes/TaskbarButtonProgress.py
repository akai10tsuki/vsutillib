"""
 Task bar icon progress
"""

import platform

from PySide2.QtCore import Slot

if platform.system() == "Windows":
    from PySide2.QtWinExtras import QWinTaskbarButton #, QWinTaskbarProgress


class TaskbarButtonProgress(QWinTaskbarButton):
    """
    TaskbarProgress taskbar icon progress indicator
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.platform = platform.system()
        self.parent = parent
        self.button = None
        self.progress = None

        if self.platform == "Windows":
            self.button = QWinTaskbarButton(parent)

    def __bool__(self):
        if (self.button is None) or (self.progress is None):
            return False
        return True

    def initTaskbarButton(self):
        """
        initTaskbarButton for late init QWinTaskbarButton
        """

        if self.platform == "Windows":
            self.button.setWindow(self.parent.windowHandle())
            self.progress = self.button.progress()
            self.progress.setRange(0, 100)
            self.progress.setVisible(True)

    @Slot(int, int)
    def setValue(self, init, total):

        self.progress.setValue(total)
