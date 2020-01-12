"""
This class is used to construct the list used to execute the MKVMerge
command line

strCommand = Command obtained from mkvtoolnix-gui with the modifications
    needed for Multiplexing a series in a directory

path for executable and target options are parsed from the command line

"""

import re
import shlex
import logging

from pathlib import Path

from vsutillib.files import stripEncaseQuotes
from .verifycommand import VerifyMKVCommand

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class MKVCommand(object):
    """
    Class to work with **mkvmerge** command part of MKVToolnix_

    Args:
        strCommand (:obj:`str`, optional): command line as generated by mkvtoolnix-gui
    """

    __log = False

    @classmethod
    def classLog(cls, setLogging=None):
        """
        get/set logging at class level
        every class instance will log
        unless overwritten

        Args:
            setLogging (bool):
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

        return cls.__log

    def __init__(self, strCommand=None):

        # self.__destinationDirectory = None
        self.__lstCommands = []
        self.__strShellCommand = None
        self.__strError = ""
        self.__bErrorFound = False
        self.__workFiles = _WorkFiles()
        self.__commandTemplate = None
        self.__filesInDirsByKey = None

        self.__log = None

        # for iterator
        self.__index = 0

        if strCommand is not None:
            self._initHelper(strCommand)

    def _initHelper(self, strCommand, bRemoveTitle=True):

        if strCommand is None:
            self.__reset()
            verify = False
        else:
            verify = VerifyMKVCommand(strCommand)

        if verify:

            self.__strShellCommand = strCommand
            self.__bErrorFound = False
            lstSources = []
            bHasChaptersFile = False

            strCommand = verify.bashCommand

            reOutputFile = r"\-\-output\s(.*?)\s\-\-"
            reChaptersFile = r"\-\-chapters\s(.*?)\s\-\-"
            reSourceFile = r"('\('\s(.*?)\s'\)')"

            reOutputFileEx = re.compile(reOutputFile)
            reChaptersFileEx = re.compile(reChaptersFile)
            reSourcesEx = re.compile(reSourceFile)

            # search for the output file
            if match := reOutputFileEx.search(strCommand):
                strOutputFile = match.group(1)

            outputFile = verify.outputFile

            # search for chapters file
            # match = reChaptersFileEx.search(strCommand)
            if match := reChaptersFileEx.search(strCommand):
                strChaptersFile = match.group(1)
                chaptersFile = verify.chaptersFile
                bHasChaptersFile = True

            # search for the source files
            # this have to exist in the
            # file system
            if match := reSourcesEx.findall((strCommand)):
                for m in match:
                    lstSources.append(m)

            newCommandTemplate = strCommand

            filesInDirsByKey = {}
            lstBaseFiles = []

            lenOfListOfFiles = 0

            for index, source in enumerate(lstSources):

                # Set source files
                sub, fileName = source
                key = "<SOURCE{}>".format(str(index))
                fileName = fileName.replace(r"'\''", "'")
                f = Path(stripEncaseQuotes(fileName))
                d = f.parent
                fd = [x for x in d.glob("*" + f.suffix) if x.is_file()]
                fd.sort(key=_strPath)

                # Check all lists have same number of files
                if lenOfListOfFiles == 0:
                    lenOfListOfFiles = len(fd)

                elif lenOfListOfFiles != len(fd):
                    self.__reset()
                    self.__bErrorFound = True
                    self.__strError = "List of files are not equal."

                # Set output files
                if index == 0:
                    od = []
                    for o in fd:
                        of = outputFile.parent.joinpath(o.stem + ".mkv")
                        of = _resolveOverwrite(of)
                        od.append(of)
                    filesInDirsByKey[_Key.outputFile] = od
                    newCommandTemplate = newCommandTemplate.replace(
                        strOutputFile, _Key.outputFile, 1
                    )

                lstBaseFiles.append(f)  # backwards compatible
                filesInDirsByKey[key] = fd
                newCommandTemplate = newCommandTemplate.replace(sub, key, 1)

            # Set output files
            if bHasChaptersFile:
                d = chaptersFile.parent
                cd = [x for x in d.glob("*" + chaptersFile.suffix) if x.is_file()]
                cd.sort(key=_strPath)

                if lenOfListOfFiles != len(cd):
                    self.__reset()
                    self.__bErrorFound = True
                    self.__strError = "List of files are not equal."

                filesInDirsByKey[_Key.chaptersFile] = cd

                newCommandTemplate = newCommandTemplate.replace(
                    strChaptersFile, _Key.chaptersFile, 1
                )

            if not self.__bErrorFound:
                self.__commandTemplate = newCommandTemplate
                self.__filesInDirsByKey = filesInDirsByKey

                self.__workFiles.baseFiles = lstBaseFiles
                self.__workFiles.chaptersFiles = (
                    None
                    if _Key.chaptersFile not in filesInDirsByKey
                    else filesInDirsByKey[_Key.chaptersFile]
                )

                self._generateCommands()
            else:
                if self.log:
                    MODULELOG.error("MKV0005: %s", self.__strError)

        else:
            # error cannot process command
            self.__reset()
            self.__strError = "Error parsing command line."
            self.__bErrorFound = True

            if self.log:
                MODULELOG.error("MKV0005: %s", self.__strError)

    def __reset(self):
        """Reset variable properties"""

        # self.__destinationDirectory = None
        self.__lstCommands = []
        self.__strShellCommand = None
        self.__strError = ""
        self.__index = 0
        self.__workFiles.clear()
        self.__commandTemplate = None
        self.__filesInDirsByKey = None

    def __bool__(self):
        return not self.__bErrorFound

    def __contains__(self, item):
        return item in self.__lstCommands

    def __getitem__(self, index):
        return [
            self.__lstCommands[index],
            self.__workFiles.baseFiles,
            self.__workFiles.sourceFiles[index],
            self.__workFiles.destinationFiles[index],
            None
            if not self.__workFiles.chaptersFiles
            else self.__workFiles.chaptersFiles[index],
        ]

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__lstCommands)

    def __next__(self):
        if self.__index >= len(self.__lstCommands):
            self.__index = 0
            raise StopIteration
        else:
            self.__index += 1
            return self.__getitem__(self.__index - 1)

            # return [self.__lstCommands[self.__index - 1],
            #        self.__workFiles.baseFiles,
            #        self.__workFiles.sourceFiles[self.__index - 1],
            #        self.__workFiles.destinationFiles[self.__index - 1]]

    def _generateCommands(self, bRemoveTitle=True):

        lstTmp = []
        lstTmp1 = []

        #
        # lstTmp list of the form:
        # [[('<OUTFILE>', file1), ('<OUTFILE>', file2), ...],
        #  [('<SOURCE0>', file1), ('<SOURCE0>', file2), ...],
        #  [('<SOURCE1>', file1), ('<SOURCE1>', file2), ...],
        #  [('<CHAPTERS>', file1), ('<CHAPTERS>', file2), ...], # optional
        #  ...]
        # theese are the individual list by key
        #
        for key in self.__filesInDirsByKey:
            filesInDir = self.__filesInDirsByKey[key]
            z = zip([key] * len(filesInDir), filesInDir)
            if key != _Key.outputFile:
                lstTmp1.append(filesInDir)
            lstTmp.append(list(z))

        if self.log:
            MODULELOG.debug("MKV0006: Files by Key %s", str(lstTmp))

        #
        # list of the form:
        # [(('<OUTFILE>', file1), ('<SOURCE0>', file1), ('<SOURCE1>', file1), ('<CHAPTERS>', file1), ...), pylint: disable=line-too-long
        #  (('<OUTFILE>', file2), ('<SOURCE0>', file2), ('<SOURCE1>', file2), ('<CHAPTERS>', file1), ...),
        #  ...]
        # theese are the combined list of lstTmp unpacked and zip is applied
        # to have all the keys for substitution at the same point
        # chapters are optional
        #
        lstSourceFilesWithKey = list(zip(*lstTmp))
        lstSourceFiles = list(zip(*lstTmp1))  # backwards compatible

        #
        # generate all the commands and store them in shlex form
        #

        self.__lstCommands = []

        for s in lstSourceFilesWithKey:

            newCommand = self.__commandTemplate

            for e in s:
                key, fileName = e
                qf = shlex.quote(str(fileName))
                newCommand = newCommand.replace(key, qf, 1)

            shellCommand = shlex.split(newCommand)

            if bRemoveTitle and shellCommand:
                # Remove title if found since this is for batch processing
                # the title will propagate to all the files maybe erroneously.
                # This field is preserved from the source files.

                while "--title" in shellCommand:

                    i = shellCommand.index("--title")
                    del shellCommand[i : i + 2]

            self.__lstCommands.append(shellCommand)

        self.__workFiles.sourceFiles = lstSourceFiles  # redundant for rename
        self.__workFiles.destinationFiles = self.__filesInDirsByKey[_Key.outputFile]

        if self.log:
            MODULELOG.debug("MKV0001: Command template %s", str(self.__commandTemplate))
            MODULELOG.debug("MKV0002: Base files %s", str(self.__workFiles.baseFiles))
            MODULELOG.debug(
                "MKV0003: Source files %s", str(self.__workFiles.sourceFiles)
            )
            MODULELOG.debug(
                "MKV0004: Destination files %s", str(self.__workFiles.destinationFiles)
            )

    @property
    def log(self):
        """
        class property can be used to override the class global
        logging setting

            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return MKVCommand.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value

    @property
    def command(self):
        """
        get/set command produced by mkvtoolnix-gui

        Returns:
            str:

            original command set
        """
        return self.__strShellCommand

    @command.setter
    def command(self, value):
        """Update command through property"""
        if isinstance(value, str):
            self.__reset()
            self._initHelper(value, bRemoveTitle=True)

    @property
    def baseFiles(self):
        """
        files parsed from command

        Returns:
            list:

            list with the files as parsed from command
        """
        return self.__workFiles.baseFiles

    @property
    def sourceFiles(self):
        """
        source files read from respective directories

        Returns:
            list:

            list with all the source files
        """
        return self.__workFiles.sourceFiles

    @property
    def destinationFiles(self):
        """
        destination files

        Returns:
            list:

            list with destination files
        """
        return self.__workFiles.destinationFiles

    @property
    def template(self):
        """
        template to construct the commands

        Returns:
            list:

            command template
        """
        return self.__commandTemplate

    @property
    def error(self):
        """
        message of any error found during evaluation of command

        Returns:
            str:

            error description
        """
        return self.__strError

    def renameOutputFiles(self, fileNames):
        """
        Mothod for renaming the output files

        Arguments:
            fileNames {list} -- list of file names
        """

        totalNames = len(self.__filesInDirsByKey[_Key.outputFile])
        totalRenames = len(fileNames)

        if totalNames != totalRenames:
            self.__strError = "Files to rename and new names not equal length."

        else:
            self.__filesInDirsByKey[_Key.outputFile] = fileNames
            self._generateCommands()


class _WorkFiles:
    """Files read from directories"""

    def __init__(self):

        self.baseFiles = []
        self.sourceFiles = []
        self.destinationFiles = []
        self.chaptersFiles = []

    def clear(self):
        """Clear file lists"""

        self.baseFiles = []
        self.sourceFiles = []
        self.destinationFiles = []
        self.chaptersFiles = []


class _Key:

    outputFile = "<OUTPUTFILE>"
    chaptersFile = "<CHAPTERS>"


def _resolveOverwrite(fileName, strPrefix="new-"):

    fileNameTmp = fileName

    # Check if destination file exist and add prefix if it does
    if fileNameTmp.is_file():

        strSuffix = ""
        n = 1

        while True:
            fileNameTmp = fileNameTmp.parent.joinpath(
                strPrefix + fileName.stem + strSuffix + fileName.suffix
            )

            if fileNameTmp.is_file():
                strSuffix = " ({})".format(n)
                n += 1
            else:
                break

    # video-S01E01.mkv
    return fileNameTmp


def _strPath(value):
    """
    Convenience function to help sort

    Arguments:
        value {various types} -- value to convert to string

    Returns:
        str -- argument received converted to string
    """
    return str(value)
