"""
Convenience functions
"""

import threading

def isThreadRunning(threadName):

    if threadName in [x.name for x in threading.enumerate()]:
        return True

    return False
