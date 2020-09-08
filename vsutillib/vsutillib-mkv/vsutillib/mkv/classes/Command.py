""" Command """

class Command:
    """
    Command class to group everything related with one command
    """

    def __init__(self):

        self._initVars()

    def _initVars(self):

        self.command = None
        self.template = None
        self.shellCommand = None
        self.translation = {}
        self.orderTranslation = {}
        self.adjusted = False
