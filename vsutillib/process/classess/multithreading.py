"""
Multithreading Class base on threading.Thread
"""

import logging
import sys
import threading
import traceback


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class GenericThreadWorker(threading.Thread):
    """
    Generic Thread
    """

    log = False

    def __init__(self, function, *args, **kwargs):
        super(GenericThreadWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Override run and start function from argument"""

        try:
            self.function(*self.args, **self.kwargs)
        except: # pylint: disable=bare-except
            traceback.print_exc()

        return


class QueueThreadWorker(threading.Thread):
    """
    Queue ThreadWorker
    """

    log = False

    def __init__(self, queue, function, *args, **kwargs):
        super(QueueThreadWorker, self).__init__()

        self.queue = queue
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):

        while True:
            # Get the work from the queue and expand the tuple
            nextJob = self.queue.get()
            try:
                self.function(nextJob, *self.args, **self.kwargs)
            finally:
                self.queue.task_done()


class ThreadWorker(threading.Thread):
    """
    Worker thread

    Inherits from threading.Tread to handle worker thread setup, signals and wrap-up.

    :param function: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type function: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    log = False

    def __init__(
            self,
            function,
            *args,
            funcFinished=None,
            funcError=None,
            funcResult=None,
            **kwargs
        ):
        super(ThreadWorker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = funcFinished
        self.error = funcError
        self.result = funcResult

    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
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
