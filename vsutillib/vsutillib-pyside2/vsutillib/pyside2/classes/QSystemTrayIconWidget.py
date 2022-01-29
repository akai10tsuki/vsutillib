"""
 SystemTrayIcon utility class
"""
import platform

from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon, QWidget

# from PySide2 import QtWidgets


class QSystemTrayIconWidget(QSystemTrayIcon):
    """
    QSystemTrayIconWidget System tray icon utility class

    Args:
        icon (QIcon): icon to use
    """

    def __init__(self, parent: QWidget, icon: QIcon, seconds: int = 5) -> None:
        super().__init__(parent)

        self.__isTrayIcon = False
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.__isTrayIcon = True

            self.parent = parent
            self.__seconds = seconds

            self.minimizeAction = QAction()
            self.maximizeAction = QAction()
            self.restoreAction = QAction()
            self.quitAction = QAction()

            self._trayIconActionsCreate()
            self._trayIconCreate(icon)

            self.activated.connect(self.iconActivated)

    def _trayIconActionsCreate(self) -> None:
        self.minimizeAction = QAction("Minimize", self.parent)
        self.minimizeAction.triggered.connect(self.parent.hide)

        self.maximizeAction = QAction("Maximize", self)
        self.maximizeAction.triggered.connect(self.parent.showMaximized)

        self.restoreAction = QAction("Restore", self.parent)
        self.restoreAction.triggered.connect(self.parent.showNormal)

        self.quitAction = QAction("Quit", self.parent)
        self.quitAction.triggered.connect(QApplication.quit)

    def _trayIconCreate(self, icon: QIcon) -> None:

        if QSystemTrayIcon.isSystemTrayAvailable():

            from PySide2.QtWidgets import QStyleFactory

            self.__isTrayIcon = True

            trayIconMenu = QMenu(self.parent)
            trayIconMenu.addAction(self.minimizeAction)
            trayIconMenu.addAction(self.maximizeAction)
            trayIconMenu.addAction(self.restoreAction)
            trayIconMenu.addSeparator()
            trayIconMenu.addAction(self.quitAction)

            if platform.system() == "Windows":
                style = QStyleFactory.create("windowsvista")
                trayIconMenu.setStyle(style)

            self.setContextMenu(trayIconMenu)
            self.setIcon(icon)

    def __bool__(self):
        return self.__isTrayIcon

    @property
    def isTrayIcon(self) -> bool:
        return self.__isTrayIcon

    @property
    def seconds(self) -> int:
        return self.__seconds

    @seconds.setter
    def seconds(self, value: int) -> None:
        self.__seconds = value

    @Slot(str)
    def iconActivated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        print("iconActivated")
        if reason == QSystemTrayIcon.Trigger:
            print("Trigger")
        if reason == QSystemTrayIcon.DoubleClick:
            print("DoubleClick")
        if reason == QSystemTrayIcon.MiddleClick:
            print("MiddleClick")
        if reason == QSystemTrayIcon.Context:
            print("Context Request")

    @Slot(int)
    def setVisible(self, visible: bool) -> None:
        print("Visible")
        super().visible(visible)

    @Slot(int)
    def setMenuEnabled(self, visible: bool) -> None:
        """ Override setVisible """
        if self.__isTrayIcon:
            self.minimizeAction.setEnabled(visible)
            self.maximizeAction.setEnabled(not self.parent.isMaximized())
            self.restoreAction.setEnabled(self.parent.isMaximized() or not visible)

    @Slot(str, str)
    @Slot(str, str, object)
    @Slot(str, str, object, int)
    def showMessage(
        self,
        title: str,
        msg: str,
        icon: QIcon = QSystemTrayIcon.Information,
        mSecs: int = 1000,
    ) -> None:

        super().showMessage(title, msg, icon, self.__seconds + 1000)
