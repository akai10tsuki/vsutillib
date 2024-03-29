"""
Multithreading Class base on QThread
"""


import logging
import traceback
import sys

from typing import Any, Callable, Optional

from PySide2.QtCore import QThread, QRunnable


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class QthThread(QThread):
    """
    QThread generic class send function and arguments to start in thread

    :param function: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type function: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    log = False

    def __init__(self, function: Callable[..., None], *args: Any, **kwargs: Any) -> None:
        super().__init__(self)

        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self) -> None:
        self.wait()

    def run(self) -> None:
        """Override run and start function from argument"""

        self.function(*self.args, **self.kwargs)


class QthThreadWorker(QRunnable):
    """
    Worker thread

    Inherits from threading.Tread to handle worker thread setup, signals and wrap-up.

    Args:
        function (function): Function to submit to Thread.
        funcFinished (function): Call back function when thread finishes.
        funcError (function): Call back function when an error occurs.
        funcResult (function): Call back function with the result of the execution.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    log = False

    def __init__(
        self,
        function: Callable[..., None],
        *args: Any,
        funcFinished: Optional[Callable[..., None]] = None,
        funcError: Optional[Callable[..., None]] = None,
        funcResult: Optional[Callable[..., None]] = None,
        **kwargs: Any
    ):
        super().__init__()

        # Store constructor arguments (re-used for processing)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = funcFinished
        self.error = funcError
        self.result = funcResult

    def run(self) -> None:
        """
        Override run initialise and starts the worker function
        with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        # pylint: disable-msg=W0702
        # have to capture all exceptions using sys.exc_info()
        # to sort out what is happening
        try:
            result = self.function(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            excepttype, value = sys.exc_info()[:2]
            if callable(self.error):
                self.error((excepttype, value, traceback.format_exc()))
        else:
            if callable(self.result):
                self.result(result)  # Return the result of the processing
        finally:
            if callable(self.finished):
                self.finished()  # Done
