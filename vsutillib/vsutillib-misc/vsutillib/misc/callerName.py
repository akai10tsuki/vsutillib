"""
Get a name of a caller in the format [module.]class.method

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

    An empty string is returned if skipped levels exceed stack height
"""

import inspect


def callerName(skip=2, includeModule=False):

    stack = inspect.stack()
    start = 0 + skip

    if len(stack) < start + 1:
      return ''
    parentFrame = stack[start][0]

    name = []
    if includeModule:
        module = inspect.getmodule(parentFrame)
        if module:
            name.append(module.__name__)

    # detect class name
    if 'self' in parentFrame.f_locals:
        name.append(parentFrame.f_locals['self'].__class__.__name__)

    codename = parentFrame.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method

    return ".".join(name)
