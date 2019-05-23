"""
RunCommand

Run a command in a subprocess and capture any output

if processLine function is provided it will be called
with every line read

if regexsearch regular expresion is provided the first
match will be set on regexmatch property
"""


import re
import shlex
import subprocess

import traceback


class RunCommand:
    """
    Run system command in subprocess
    and save generated output

    :param command: command to execute
    :type command: str
    :param processLine: function called with every line read
    :type processLine: func
    :param regexsearch: regular expresion to search for match
    :type regexsearch: str
    """

    def __init__(
            self,
            command=None,
            processLine=None,
            processArgs=None,
            processKWArgs=None,
            regexsearch=None,
            commandShlex=False,
            universalNewLines=False
        ):

        self.__command = None
        self.command = command

        self.__commandShlex = commandShlex
        self.__process = processLine
        self.__universalNewLines = universalNewLines
        self.__processArgs = []

        if processArgs is not None:
            if isinstance(processArgs, list):
                self.__processArgs = processArgs
            else:
                raise ValueError('processLineParam has to be a dictionary')

        self.__processKWArgs = {}

        if processKWArgs is not None:
            if isinstance(processKWArgs, dict):
                self.__processKWArgs = processKWArgs
            else:
                raise ValueError('processLineParam has to be a dictionary')

        self.__regEx = None
        if regexsearch is not None:
            if isinstance(regexsearch, list):
                self.__regEx = []
                for regex in regexsearch:
                    self.__regEx.append(re.compile(regex))
            else:
                self.__regEx = re.compile(regexsearch)

        self.__error = ""
        self.__output = []
        self.__returnCode = None
        self.__regexmatch = None

    def __bool__(self):
        if self.__command:
            return True
        return False

    @property
    def command(self):
        """command to execute"""
        return self.__command

    @command.setter
    def command(self, value):
        """return current command set in class"""
        self.__command = None
        self._reset(value)

    @property
    def shlexCommand(self):
        """command to submit to subproccess PIPE"""
        return shlex.split(self.__command)

    @property
    def error(self):
        """error if command can not be executed"""
        return self.__error

    @property
    def output(self):
        """captured output"""
        return self.__output

    @property
    def parsedcommand(self):
        """
        command parsed by shlex
        can be used for debugging
        """
        return shlex.split(self.__command)

    @property
    def rc(self):
        """return code"""
        return self.__returnCode

    @property
    def regexmatch(self):
        """results of regular expresion search"""
        return self.__regexmatch

    def run(self):
        """method to call to execute command"""
        self._reset()

        self._getCommandOutput()

        if self.__output:
            return True

        return False

    def _reset(self, command=None):

        self.__output = []
        self.__error = ""
        self.__regexmatch = None
        if command is not None:
            self.__command = command

    def _regexMatch(self, line):
        """Have to set the size of in case of list"""

        m = None

        if isinstance(self.__regEx, list):

            for index, regex in enumerate(self.__regEx):
                m = regex.search(line)

                if m is not None:
                    if self.__regexmatch is None:
                        self.__regexmatch = [None] * len(self.__regEx)

                    tmpList = []
                    for i in m.groups():
                        tmpList.append(i)

                    self.__regexmatch[index] = tmpList

        else:

            if self.__regEx:
                m = self.__regEx.search(line)

            if m is not None:
                if self.__regexmatch is None:
                    self.__regexmatch = []

                for i in m.groups():
                    self.__regexmatch.append(i)

    def _getCommandOutput(self):
        """Execute command in a subprocess"""

        self.__returnCode = 10000
        rc = 1000
        if self.__commandShlex:
            cmd = self.__command
        else:
            cmd = shlex.split(self.__command)

        try:

            with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE,
                    bufsize=1,
                    universal_newlines=self.__universalNewLines,
                    stderr=subprocess.STDOUT
                ) as p:

                try:

                    for l in p.stdout:

                        if self.__universalNewLines:
                            line = l
                        else:
                            line = l.decode('utf-8')

                        self.__output.append(line)
                        self.__regexmatch(line)

                        if self.__process is not None:
                            self.__process(
                                line,
                                *self.__processArgs,
                                **self.__processKWArgs
                            )

                except UnicodeDecodeError as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.reason)
                    self.__output.append(str(cmd) + '\n')
                    self.__output.append(msg)
                    self.__output.append(trb)

                    if self.__process is not None:
                        self.__process(
                            line,
                            *self.__processArgs,
                            **self.__processKWArgs
                        )

                except KeyboardInterrupt as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.args)
                    self.__output.append(str(cmd) + '\n')
                    self.__output.append(msg)
                    self.__output.append(trb)

                    if self.__process is not None:
                        self.__process(
                            line,
                            *self.__processArgs,
                            **self.__processKWArgs
                        )

                    raise SystemExit(0)

                rcResult = p.poll()
                if rcResult is not None:
                    self.__returnCode = rcResult
                    rc = rcResult

        except FileNotFoundError as e:
            self.__error = e

        return rc

    def _getCommandOutputBackup(self):
        """Execute command in a subprocess"""

        self.__returnCode = 10000
        rc = 1000
        if self.__commandShlex:
            cmd = self.__command
        else:
            cmd = shlex.split(self.__command)

        try:

            with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE,
                    bufsize=1,
                    stderr=subprocess.STDOUT
                ) as p:

                try:
                    for l in iter(p.stdout):

                        line = l.decode('utf-8')

                        self.__output.append(line)
                        self.__regexmatch(line)

                        if self.__process is not None:
                            self.__process(
                                line,
                                *self.__processArgs,
                                **self.__processKWArgs
                            )

                except UnicodeDecodeError as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.reason)
                    self.__output.append(str(cmd) + '\n')
                    self.__output.append(msg)
                    self.__output.append(trb)

                    if self.__process is not None:
                        self.__process(line)

                except KeyboardInterrupt as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.args)
                    self.__output.append(str(cmd) + '\n')
                    self.__output.append(msg)
                    self.__output.append(trb)

                    if self.__process is not None:
                        self.__process(line)

                    raise SystemExit(0)

                rcResult = p.poll()
                if rcResult is not None:
                    self.__returnCode = rcResult
                    rc = rcResult

        except FileNotFoundError as e:
            self.__error = e

        return rc
