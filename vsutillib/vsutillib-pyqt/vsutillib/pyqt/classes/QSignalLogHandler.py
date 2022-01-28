""" QLogHandler """

import logging

from typing import Any, Callable, Optional

from PySide2.QtCore import QObject, Signal


class Communicate(QObject):
    logRecord: Signal = Signal(object)


class QSignalLogHandler(logging.Handler):

    """
    logging using Qt for Python Signal to register records via signal to logger
    slot function

    Args:
        slotFunction (function):

        **kwargs (dict): variable number of key value parameters
            that are passed to the super class on
            initialization
    """

    def __init__(self, slotFunction: Optional[Callable[..., None]] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.signal = Communicate()

        if slotFunction is not None:
            self.connect(slotFunction)

    def emit(self, record: str) -> None:
        msg = self.format(record)
        self.signal.logRecord.emit(msg)

    def connect(self, slotFunction: Callable[..., None]) -> None:

        self.signal.logRecord.connect(slotFunction)
