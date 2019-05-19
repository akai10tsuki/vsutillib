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

        self._command = command
        self._process = processLine
        self._commandShlex = commandShlex
        self._universalNewLines = universalNewLines
        self._processArgs = []

        if processArgs is not None:
            if isinstance(processArgs, list):
                self._processArgs = processArgs
            else:
                raise ValueError('processLineParam has to be a dictionary')

        self._processKWArgs = {}

        if processKWArgs is not None:
            if isinstance(processKWArgs, dict):
                self._processKWArgs = processKWArgs
            else:
                raise ValueError('processLineParam has to be a dictionary')

        self._regEx = None
        if regexsearch is not None:
            if isinstance(regexsearch, list):
                self._regEx = []
                for regex in regexsearch:
                    self._regEx.append(re.compile(regex))
            else:
                self._regEx = re.compile(regexsearch)

        self._error = ""
        self._output = []
        self._rc = None
        self._regexmatch = None

    def __bool__(self):
        if self._command:
            return True
        return False

    @property
    def command(self):
        """command to execute"""
        return self._command

    @command.setter
    def command(self, value):
        """return current command set in class"""
        self._reset(value)

    @property
    def shlexCommand(self):
        """command to submit to subproccess PIPE"""
        return shlex.split(self._command)

    @property
    def error(self):
        """error if command can not be executed"""
        return self._error

    @property
    def output(self):
        """captured output"""
        return self._output

    @property
    def parsedcommand(self):
        """
        command parsed by shlex
        can be used for debugging
        """
        return shlex.split(self._command)

    @property
    def rc(self):
        """return code"""
        return self._rc

    @property
    def regexmatch(self):
        """results of regular expresion search"""
        return self._regexmatch

    def run(self):
        """method to call to execute command"""
        self._reset()

        self._getCommandOutput()

        if self._output:
            return True

        return False

    def _reset(self, command=None):

        self._output = []
        self._error = ""
        self._regexmatch = None
        if command is not None:
            self._command = command

    def _regexMatch(self, line):
        """Have to set the size of in case of list"""

        m = None

        if isinstance(self._regEx, list):

            for index, regex in enumerate(self._regEx):
                m = regex.search(line)

                if m is not None:
                    if self._regexmatch is None:
                        self._regexmatch = [None] * len(self._regEx)

                    tmpList = []
                    for i in m.groups():
                        tmpList.append(i)

                    self._regexmatch[index] = tmpList

        else:

            if self._regEx:
                m = self._regEx.search(line)

            if m is not None:
                if self._regexmatch is None:
                    self._regexmatch = []

                for i in m.groups():
                    self._regexmatch.append(i)

    def _getCommandOutput(self):
        """Execute command in a subprocess"""

        self._rc = 10000
        rc = 1000
        if self._commandShlex:
            cmd = self._command
        else:
            cmd = shlex.split(self._command)

        try:

            with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE,
                    bufsize=1,
                    universal_newlines=self._universalNewLines,
                    stderr=subprocess.STDOUT
                ) as p:

                try:

                    for l in p.stdout:

                        if self._universalNewLines:
                            line = l
                        else:
                            line = l.decode('utf-8')

                        self._output.append(line)
                        self._regexMatch(line)

                        if self._process is not None:
                            self._process(
                                line,
                                *self._processArgs,
                                **self._processKWArgs
                            )

                except UnicodeDecodeError as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.reason)
                    self._output.append(str(cmd) + '\n')
                    self._output.append(msg)
                    self._output.append(trb)

                    if self._process is not None:
                        self._process(
                                line,
                                *self._processArgs,
                                **self._processKWArgs
                        )

                except KeyboardInterrupt as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.args)
                    self._output.append(str(cmd) + '\n')
                    self._output.append(msg)
                    self._output.append(trb)

                    if self._process is not None:
                        self._process(
                                line,
                                *self._processArgs,
                                **self._processKWArgs
                            )

                    raise SystemExit(0)

                rcResult = p.poll()
                if rcResult is not None:
                    self._rc = rcResult
                    rc = rcResult

        except FileNotFoundError as e:
            self._error = e

        return rc

    def _getCommandOutputBackup(self):
        """Execute command in a subprocess"""

        self._rc = 10000
        rc = 1000
        if self._commandShlex:
            cmd = self._command
        else:
            cmd = shlex.split(self._command)

        try:

            with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE,
                    bufsize=1,
                    stderr=subprocess.STDOUT
                ) as p:

                try:
                    for l in iter(p.stdout):

                        line = l.decode('utf-8')

                        self._output.append(line)
                        self._regexMatch(line)

                        if self._process is not None:
                            self._process(
                                line,
                                *self._processArgs,
                                **self._processKWArgs
                            )

                except UnicodeDecodeError as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.reason)
                    self._output.append(str(cmd) + '\n')
                    self._output.append(msg)
                    self._output.append(trb)

                    if self._process is not None:
                        self._process(line)

                except KeyboardInterrupt as error:

                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.args)
                    self._output.append(str(cmd) + '\n')
                    self._output.append(msg)
                    self._output.append(trb)

                    if self._process is not None:
                        self._process(line)

                    raise SystemExit(0)

                rcResult = p.poll()
                if rcResult is not None:
                    self._rc = rcResult
                    rc = rcResult

        except FileNotFoundError as e:
            self._error = e

        return rc
