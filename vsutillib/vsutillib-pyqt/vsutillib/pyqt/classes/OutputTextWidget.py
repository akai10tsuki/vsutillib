"""
OutputTextWidget:

Output widget form just to output text in color

"""
# OTW0004 Next log ID

import logging
import platform

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtGui import QTextCursor
from PySide2.QtWidgets import QTextEdit

import vsutillib.macos as macos

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class OutputTextWidget(QTextEdit):
    """Output for running queue"""

    # log state
    __log = False
    insertTextSignal = Signal(str, dict)

    @classmethod
    def classLog(cls, setLogging=None):
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

    def __init__(self, parent=None):
        super(OutputTextWidget, self).__init__(parent)

        self.parent = parent
        self.__log = None

        self.insertTextSignal.connect(self.insertText)

    def connectToInsertText(self, objSignal):
        """Connect to signal"""

        objSignal.connect(self.insertText)

    @Slot(str, dict)
    def insertText(self, strText, kwargs):
        """
        insertText - Insert text in output window.
        Cannot use standard keyword arguments on
        emit calls using a dictionary argument instead

        Args:
            strText (str): text to insert on output window
            kwargs (dict): additional arguments in dictionary
                           used like **kwargs
        """

        strTmp = ""

        color = kwargs.pop("color", None)
        replaceLine = kwargs.pop("replaceLine", False)
        appendLine = kwargs.pop("appendLine", False)

        # still no restore to default the ideal configuration
        # search will continue considering abandoning color

        if color is None:
            if macos.isMacDarkMode() or (platform.system() == "Windows"):
                color = Qt.white
            else:
                color = Qt.black
        elif macos.isMacDarkMode() or (platform.system() == "Windows"):
            if color == Qt.red:
                color = Qt.magenta
            elif color == Qt.darkGreen:
                color = Qt.green
            elif color == Qt.blue:
                color = Qt.cyan

        if color is not None:
            self.setTextColor(color)

        if replaceLine:
            self.moveCursor(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            self.insertPlainText(strText)
        elif appendLine:
            self.append(strText)
        else:
            self.insertPlainText(strText)

        self.ensureCursorVisible()

        if self.log:
            strTmp = strTmp + strText
            strTmp = strTmp.replace("\n", " ")
            if strTmp != "" and strTmp.find(u"Progress:") != 0:
                if strTmp.find(u"Warning") == 0:
                    MODULELOG.warning("OTW0001: %s", strTmp)
                elif strTmp.find(u"Error") == 0 or color == Qt.red:
                    MODULELOG.error("OTW0002: %s", strTmp)
                else:
                    MODULELOG.info("OTW0003: %s", strTmp)

    @property
    def log(self):
        """
        class property can be used to override the class global
        logging setting

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return OutputTextWidget.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value
