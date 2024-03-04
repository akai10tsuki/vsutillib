"""
RunCommand

Run a command in a subprocess and capture any output

if processLine function is provided it will be called
with every line read

if regexsearch regular expression is provided the first
match will be set on regexmatch property
"""
# RNC0004

import io
import logging
import platform
import re
import shlex
import subprocess
import traceback

from vsutillib.misc import staticVars

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class RunCommand:
    """
    Run a command in a subprocess and capture any output

    processLine function if provided it will be called
    with every line read.

    regexsearch regular expression if provided the first
    match will be set on regexmatch property

    Args:
        **command** (str): command to execute

        **commandShlex** (:obj:`bool`): True if command is shlex.split
        False otherwise. Defaults to False.

        **processLine** (:obj:`function`, optional): Function called with
        every line read if working in text mode. If working in binary it
        receives character by character. Defaults to None.

        **processArgs** (:obj:`list`, optional): Variable length list to
        pass to processLine. Defaults to None.

        **processKWArgs** (:obj:`list`, optional): Arbitrary keyword
        arguments to pass to processLine. Defaults to None.

        **regexsearch** (:obj:`str`, optional): Regex applied to every
        line read. Defaults to None

        **universalNewLine** (:obj:`bool`): True to read in text mode
        False to read binary mode. Defaults to False.

    Raises:

        ValueError: If processArgs is not a list or if processKWArgs
            is not a dictionary.
    """

    __log = False

    @classmethod
    def classLog(cls, setLogging=None):
        """
        get/set logging at class level
        every class instance will log
        unless overwritten

        Args:
            setLogging (`bool`):

                - True class will log
                - False turn off logging
                - None returns current Value

        Returns:
            bool:

            returns the current value set
        """

        if setLogging is not None:
            if isinstance(setLogging, bool):
                cls.__log = setLogging

    def __init__(
        self,
        command=None,
        processLine=None,
        processArgs=None,
        processKWArgs=None,
        regexsearch=None,
        commandShlex=False,
        universalNewLines=False,
        controlQueue=None,
        log=None,
    ):  # pylint: disable=too-many-arguments

        self.__command = None
        self.command = command  # Call class setter property

        self.__commandShlex = commandShlex
        self.__processLine = processLine

        self.__universalNewLines = universalNewLines
        if not self.__universalNewLines:
            if self.__processLine is None:
                self.__processLine = processCommandOutput

        self.__processArgs = []
        if processArgs is not None:
            if isinstance(processArgs, list):
                self.__processArgs = processArgs
            else:
                raise ValueError("processLineParam has to be a list")

        self.__processKWArgs = {}
        if processKWArgs is not None:
            if isinstance(processKWArgs, dict):
                self.__processKWArgs = processKWArgs
            else:
                raise ValueError("processLineParam has to be a dictionary")

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
        self.__controlQueue = controlQueue
        self.__returnCode = None
        self.__regexmatch = None
        self.__log = log

    def __bool__(self):
        if self.__command:
            return True
        return False

    # region log setup
    @property
    def log(self):
        """
        class property can be used to override the class global
        logging setting if set to None class log will be followed

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return RunCommand.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value
    # endregion log setup

    # region properties
    @property
    def command(self):
        """return current command set in class"""

        return self.__command

    @command.setter
    def command(self, value):
        """
        command to execute

        Args:
            command (str): command to execute

        Returns:
            str:

            current command set
        """
        self.__command = None
        self._reset(value)

    @property
    def shlexCommand(self):
        """
        command to submit to subprocess PIPE

        Returns:
            list:

            command split by shlex.split
        """
        return shlex.split(self.__command)

    @property
    def error(self):
        """
        error if command can not be executed

        Returns:
            str:

            message if command fails to execute
        """
        return self.__error

    @property
    def output(self):
        """
        captured output

        Returns:
            list:

            output of executed command
        """
        return self.__output

    @property
    def parsedCommand(self):
        """
        command parsed by shlex
        can be used for debugging

        Returns:
            list|dict:

            depending of the regex returns a list or
            re.Match object
        """
        return shlex.split(self.__command)

    @property
    def rc(self):
        """
        Return code. On Windows is not reliable information.

        Returns:
            int:

            return code of executed command
        """
        return self.__returnCode

    @property
    def regexmatch(self):
        """
        results of regular expression search

        Returns:
            list|dict:

            list if matches if single regex passed.  dict of list
            with the regex as key if a list of regex is passed.
        """
        return self.__regexmatch
    # endregion properties

    def run(self):
        """
        method to submit command to subprocess PIPE
        """

        self._reset()
        if self.__universalNewLines:
            self._getCommandOutputText()
        else:
            self._getCommandOutputBinary()
        if self.__output:
            return True
        return False

    def _reset(self, command=None):
        """reset internal variables"""

        self.__output = []
        self.__error = ""
        self.__regexmatch = None
        if command is not None:
            self.__command = command

    def _regexMatch(self, line):
        """Have to set the size of in case of list"""

        if isinstance(self.__regEx, list):
            for index, regex in enumerate(self.__regEx):
                if m := regex.search(line):
                    if self.__regexmatch is None:
                        self.__regexmatch = [None] * len(self.__regEx)
                    tmpList = []
                    for i in m.groups():
                        tmpList.append(i)
                    self.__regexmatch[index] = tmpList
        else:
            if self.__regEx:
                if m := self.__regEx.search(line):
                    if self.__regexmatch is None:
                        self.__regexmatch = []
                    for i in m.groups():
                        self.__regexmatch.append(i)

    def _getCommandOutputText(self):
        """Execute command in a subprocess"""

        self.__returnCode = 10000
        rc = 1000
        if self.__commandShlex:
            cmd = self.__command
        else:
            cmd = shlex.split(self.__command)
        try:
            if platform.system() == "Windows":
                p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    universal_newlines=True,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            else:
                p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    universal_newlines=True,
                    stderr=subprocess.STDOUT,
                )
            try:
                for line in p.stdout:
                    self.__output.append(line)
                    self._regexMatch(line)
                    if self.__processLine is not None:
                        self.__processLine(
                            line, *self.__processArgs, **self.__processKWArgs
                        )
                    if self.__controlQueue:
                        queueStatus = self.__controlQueue.popleft()
                        self.__controlQueue.appendleft(queueStatus)
                        if queueStatus in [
                            RunStatus.Abort,
                            RunStatus.AbortJob,
                            RunStatus.AbortForced,
                        ]:
                            p.kill()
                            outs, errs = p.communicate()
                            rc = p.returncode
                            self.__returnCode = p.returncode
                            if self.log:
                                msg = (
                                    f"RNC0003: Aborting outs {outs} errs {errs} rc={rc}"
                                )
                                MODULELOG.debug(msg)
                            break
                p.kill()
            except UnicodeDecodeError as error:
                trb = traceback.format_exc()
                msg = "Error: {}".format(error.reason)
                self.__output.append(str(cmd) + "\n")
                self.__output.append(msg)
                self.__output.append(trb)
                if self.__processLine is not None:
                    self.__processLine(
                        line, *self.__processArgs, **self.__processKWArgs
                    )
                if self.log:
                    MODULELOG.debug("RNC0001: Unicode decode error %s", msg)
            except KeyboardInterrupt as error:
                trb = traceback.format_exc()
                msg = "Error: {}".format(error.args)
                self.__output.append(str(cmd) + "\n")
                self.__output.append(msg)
                self.__output.append(trb)
                if self.__processLine is not None:
                    self.__processLine(
                        line, *self.__processArgs, **self.__processKWArgs
                    )
                if self.log:
                    MODULELOG.debug("RNC0002: Keyboard interrupt %s", msg)
                raise SystemExit(0) from error
            if rcResult := p.poll():
                self.__returnCode = rcResult
                rc = rcResult
            p.kill()
        except FileNotFoundError as e:
            self.__error = e

        return rc

    def _getCommandOutputBinary(self):
        """Execute command in a subprocess"""

        self.__returnCode = 10000
        rc = 1000
        if self.__commandShlex:
            cmd = self.__command
        else:
            cmd = shlex.split(self.__command)
        try:
            cFlag = 0
            if platform.system() == "Windows":
                cFlag = subprocess.CREATE_NO_WINDOW
            with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=False,
                creationflags=cFlag,
            ) as p:
                reader = io.TextIOWrapper(p.stdout, encoding="utf8")
                try:
                    while ch := reader.read(1):
                        self.__output.append(ch)
                        if self.__processLine is not None:
                            if line := self.__processLine(
                                ch, *self.__processArgs, **self.__processKWArgs
                            ):
                                # self.__output.append(line)
                                self._regexMatch(line)

                        if self.__controlQueue:
                            queueStatus = self.__controlQueue.popleft()
                            self.__controlQueue.appendleft(queueStatus)
                            if queueStatus in [
                                RunStatus.Abort,
                                RunStatus.AbortJob,
                                RunStatus.AbortForced,
                            ]:
                                p.kill()
                                outs, errs = p.communicate()
                                rc = p.returncode
                                self.__returnCode = p.returncode
                                if self.log:
                                    msg = f"RNC0003: Aborting outs {outs} errs {errs} rc={rc}"
                                    MODULELOG.debug(msg)
                                break
                    p.kill()

                except UnicodeDecodeError as error:
                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.reason)
                    self.__output.append(str(cmd) + "\n")
                    self.__output.append(msg)
                    self.__output.append(trb)
                    # if self.__processLine is not None:
                    #    self.__processLine(line)
                except KeyboardInterrupt as error:
                    trb = traceback.format_exc()
                    msg = "Error: {}".format(error.args)
                    self.__output.append(str(cmd) + "\n")
                    self.__output.append(msg)
                    self.__output.append(trb)
                    # if self.__processLine is not None:
                    #    self.__processLine(line)
                    raise SystemExit(0) from error
                rcResult = p.poll()
                if rcResult is not None:
                    self.__returnCode = rcResult
                    rc = rcResult
        except FileNotFoundError as e:
            self.__error = e

        return rc


@staticVars(line="")
def processCommandOutput(ch):  # pylint: disable=invalid-name
    """
    Convenience function that interprets lines in a stream of characters.

    Args:
        ch (str): characters to display

    Returns:
        str: Complete line including "\n" character when "\n" is received.
        None if character received is not a newline.
    """

    processCommandOutput.line += ch
    if ch != "\n":
        return None

    line = processCommandOutput.line

    processCommandOutput.line = ""

    return line


class RunStatus:
    """Key values for job related work"""

    Abort = "Abort"
    Aborted = "Aborted"
    AbortForced = "AbortForced"
    AbortJob = "AbortJob"
    AbortJobError = "AbortJobError"
    AddToQueue = "AddToQueue"
    Blocked = "Blocked"
    Done = "Done"
    DoneWithError = "DoneWithError"
    Error = "Error"
    Queue = "Queue"
    Running = "Running"
    Skip = "Skip"
    Skipped = "Skipped"
    Stop = "Stop"
    Stopped = "Stopped"
    Waiting = "Waiting"
