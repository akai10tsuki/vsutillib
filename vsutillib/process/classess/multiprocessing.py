"""
Multithreading Class base on threading.Thread
"""

import logging
import multiprocessing
import traceback


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class ProcessWorker(multiprocessing.Process):
    """
    Generic Thread
    """

    log = False

    def __init__(self, function, *args, **kwargs):
        super(ProcessWorker, self).__init__()

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


class QueueProcessWorker(multiprocessing.Process):
    """
    Queue ThreadWorker
    """

    log = False

    def __init__(self, queue, function, *args, **kwargs):
        super(QueueProcessWorker, self).__init__()

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
