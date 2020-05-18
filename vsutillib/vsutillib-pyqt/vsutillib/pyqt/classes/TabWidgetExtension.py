"""
 TabWidgetExtension
"""

class TabWidgetExtension:

    def __init__(self, tabWidgetChild=None, tabWidget=None, **kwargs):
        super().__init__(**kwargs)

        self.__tabWidgetChild = tabWidgetChild
        self.__tabWidget = tabWidget
        self.__tab = None
        self.__oldTab = (-1)
        self.__title = None
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
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value
        if self.tab >= 0:
            self.tabWidget.setTabText(self.tab, self.title)

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

        self.title = self.tabWidget.tabText(self.tab)
        self.toolTip = self.tabWidget.tabToolTip(self.tab)
        self.tabWidget.removeTab(self.tab)
        self.tab = (-1)

    def unHideTab(self):

        if self.tabWidget is not None:
            tabIndex = self.tabWidget.addTab(self.__tabWidgetChild, self.title)
            self.tabWidget.setTabToolTip(tabIndex, self.toolTip)
            self.tab = tabIndex
