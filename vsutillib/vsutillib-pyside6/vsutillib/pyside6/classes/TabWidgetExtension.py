"""
 TabWidgetExtension
"""

from typing import Any, Optional

from PySide6.QtWidgets import QTabWidget


class TabWidgetExtension:
    """Class to help manipulate widget in a QTabWidget"""

    def __init__(
            self,
            tabWidgetChild: Optional[object] = None,
            tabWidget: Optional[QTabWidget] = None,
            **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.__tabWidgetChild = tabWidgetChild
        self.__tabWidget = tabWidget
        self.__tab = None
        self.__oldTab = -1
        self.__tabText = None
        self.__toolTip = None

    @property
    def tab(self):
        return self.__tab

    @tab.setter
    def tab(self, value):
        self.__tab = value

    @property
    def tabWidget(self):
        return self.__tabWidget

    @tabWidget.setter
    def tabWidget(self, value):
        self.__tabWidget = value

    @property
    def tabText(self):
        return self.__tabText

    @tabText.setter
    def tabText(self, value):
        self.__tabText = value
        if self.tab >= 0:
            self.tabWidget.setTabText(self.tab, self.tabText)

    @property
    def toolTip(self):
        return self.__toolTip

    @toolTip.setter
    def toolTip(self, value):
        self.__toolTip = value
        if self.tab >= 0:
            self.tabWidget.setTabToolTip(self.tab, self.toolTip)

    def setAsCurrentTab(self):
        if self.tab >= 0:
            self.tabWidget.setCurrentIndex(self.tab)

    def hideTab(self):
        """Hide the tab"""

        tabIndex = self.tabWidget.indexOf(self.__tabWidgetChild)
        self.__oldTab = tabIndex
        self.tabWidget.removeTab(tabIndex)
        self.tab = -1

    def unHideTab(self):
        """Unhide the tab"""

        if self.tabWidget is not None:
            if self.__oldTab >= 0:
                tabIndex = self.tabWidget.insertTab(
                    self.__oldTab, self.__tabWidgetChild, self.title
                )
            else:
                tabIndex = self.tabWidget.addTab(
                    self.__tabWidgetChild, self.title)
            self.tabWidget.setTabToolTip(tabIndex, self.toolTip)
            self.tab = tabIndex
