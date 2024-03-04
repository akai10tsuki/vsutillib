"""
Tabs Widget

Central widget holds:

    - ListViewWidget
    - TableViewWidget
    - TreeViewWidget

Todo: Hide and un hide at current position.  Possibly the widget itself do
      the hiding
"""
# TWG0001

import logging

from typing import ClassVar, List, Tuple, Optional

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QTabWidget, QWidget


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


TabElement = Tuple[QWidget, str, str]


class TabWidget(QTabWidget):
    """Main Widget"""

    # Class logging state
    __log = False

    setCurrentIndexSignal = Signal(int)
    setCurrentWidgetSignal = Signal(object)

    # region Initialization

    def __init__(
            self,
            parent: Optional[QWidget] = None,
            tabWidgets: Optional[List[TabElement]] = None,
            doTranslation: Optional[bool] = False
        ) -> None:

        super().__init__()

        self.parent = parent
        self.__tabWidgets = []

        self.__log = False
        self.__doTranslation = doTranslation

        self._initUI(tabWidgets)

        self.setCurrentIndexSignal.connect(super().setCurrentIndex)
        self.setCurrentWidgetSignal.connect(super().setCurrentWidget)

    def _initUI(self, tabWidgets: List[TabElement]) -> None:
        """Setup Widget Layout"""

        if tabWidgets is not None:
            self.__tabWidgets.extend(tabWidgets)

            for tw in tabWidgets:
                tabIndex = self.addTab(tw[Key.Widget], tw[Key.Title])
                self.setTabToolTip(tabIndex, tw[Key.ToolTip])
                widget = tw[Key.Widget]

                try:
                    widget.tab = tabIndex
                except:
                    MODULELOG.error("[TabWidget] Error initializing tab.")
                try:
                    widget.title = tw[Key.Title]
                except:
                    MODULELOG.error("[TabWidget] Error initializing title.")
                try:
                    widget.tabWidget = self
                except:  # pylint: disable=bare-except
                    MODULELOG.error("[TabWidget] Error initializing tabWidget.")

    # endregion Initialization

    # region Logging

    @classmethod
    def classLog(cls, setLogging: Optional[bool] = None) -> bool:
        """
        get/set logging at class level
        every class instance will log
        unless overwritten

        Args:
            setLogging (bool):
                - True class will log
                - False turn off logging
                - None returns current Value

        Returns:
            bool:
                returns the current value set
        """

        if setLogging is not None:
            if isinstance(setLogging, bool):
                cls.__log = setLogging

        return cls.__log

    @property
    def log(self) -> bool:
        """
        class property can be used to override the class global
        logging setting

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return TabWidget.classLog()

    @log.setter
    def log(self, value: bool) -> None:
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value

    @Slot(bool)
    def setLog(self, bLogging: bool) -> None:
        """Slot for setting through signal"""
        self.log = bLogging

    # endregion Logging

    def tabInserted(self, index: int) -> None:
        """update tab index on widgets"""
        for tabIndex in range(self.count()):
            widget = self.widget(tabIndex)
            widget.tab = tabIndex

    def tabRemoved(self, index: int) -> None:
        """update tab index on widgets"""
        for tabIndex in range(self.count()):
            widget = self.widget(tabIndex)
            widget.tab = tabIndex

    def addTabs(self, tabWidgets: List[TabElement]) -> None:
        self._initUI(tabWidgets)

    def translate(self) -> None:
        """
        translate set tabs labels according to locale
        """

        for i, (widget, label, tooltip) in enumerate(self.__tabWidgets):
            if self.__doTranslation:
                widget.translation()

            self.setTabText(i, _(label))
            self.setTabToolTip(i, _(tooltip))


class Key:

    Widget: ClassVar[int] = 0
    Title: ClassVar[int] = 1
    ToolTip: ClassVar[int] = 2


def _(dummy: str) -> str:
    return dummy


del _
