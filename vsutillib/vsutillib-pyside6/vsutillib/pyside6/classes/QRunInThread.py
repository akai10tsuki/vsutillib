"""
Run a function in a Thread

worker = RunInThread(function, *args, **kwargs)

# Execute
worker.run()

*args, **kwargs will be passed to the function when run


connect to finishedSignal, startSignal, resultSignal
to deal with start of execution, end of execution and
get any result from function
"""

from typing import Any, Callable

from PySide6.QtCore import QObject, Signal

from vsutillib.process import ThreadWorker, isThreadRunning


class QRunInThread(QObject):
    """
    RunInThread - Runs a function in a Thread

    worker = RunInThread(function, *args, **kwargs)

    # Execute
    worker.run()

    *args, **kwargs will be passed to the function when run


    connect to finishedSignal, startSignal, resultSignal
    to deal with start of execution, end of execution and
    get any result from function
    Inherits from threading.Tread to handle worker thread setup, signals and wrap-up.

    Args:
        function (function): Function to submit to Thread.
        funcFinished (function): Call back function when thread finishes.
        funcResult (function): Call back function with the result of the execution.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    finishedSignal = Signal()
    startSignal = Signal()
    resultSignal = Signal(object)
    errorSignal = Signal(object)

    # Class logging state
    __log = False

    def __init__(
        self, 
        function: Callable[..., None], 
        *args: Any, 
        **kwargs: Any) -> None:
        super().__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """
        run summit jobs to worker
        """

        if not isThreadRunning(self.function.__name__):
            #
            # add:
            #    funcStart
            #    funcResult
            #    funcFinished
            #
            # parameters for ThreadWorker
            #
            jobsWorker = ThreadWorker(
                self.function,
                *self.args,
                funcStart=self.start,
                funcResult=self.result,
                funcFinished=self.finished,
                funcError=self.error,
                **self.kwargs,
            )

            jobsWorker.name = self.function.__name__
            jobsWorker.start()

    def start(self) -> None:
        """
        start generate signal for start of run
        """
        self.startSignal.emit()

    def finished(self) -> None:
        """
        finished generate signal for finished run
        """
        self.finishedSignal.emit()

    def result(self, funcResult: object) -> None:
        """
        result from jobs queue process

        Args:
            funcResult (object): messages from runJobs
        """

        self.resultSignal.emit(funcResult)

    def error(self, errorInfo: object) -> None:
        """
        error in the execution
        """

        self.errorSignal.emit(errorInfo)
