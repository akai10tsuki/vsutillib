"""
 Parse mkvmerge into a class

Track options assumed appear after --language

r"|--sync "
r"|--cues "
r"|--default-track "
r"|--forced-track "
r"|--blockadd "
r"|--track-name "
r"|--tags "
r"|--aac-is-sbr "
r"|--reduce-to-core "
r"|--remove-dialog-normalization-gain  "
r"|--timestamps "
r"|--default-duration "
r"|--fix-bitstream-timing-information "
r"|--nalu-size-length "
r"|--compression "

"""
# MCP0003

import ast
import logging
import re
import shlex

from pathlib import Path

from vsutillib.files import fileQuote
from vsutillib.media import MediaFileInfo
from vsutillib.misc import XLate

from ..mkvutils import (
    convertToBashStyle,
    numberOfTracksInCommand,
    resolveOverwrite,
    stripEncaseQuotes,
    unQuote,
)
from .mkvattachments import MKVAttachments
from .mkvclassutil import SourceFile, SourceFiles

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class MKVCommandParser:
    """
    Class for parsing CLI **mkvmerge** command part of MKVToolnix_

    Args:
        strCommand (`str`, optional): command line as generated by mkvtoolnix-gui
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

    def __init__(self, strCommand=None, log=None):

        self.log = log
        self.command = strCommand

    def _initVars(self):

        self.__bashCommand = None
        self.__errorFound = False
        self.__log = None
        self.__lstAnalysis = None
        self.__totalSourceFiles = None
        self.__readFiles = False
        self.__strCommand = None
        self.__shellCommands = []
        self.__strCommands = []

        self.chaptersFile = None
        self.chaptersFileMatchString = None
        self.chaptersLanguage = None
        self.commandTemplate = None
        self.language = None
        self.mkvmerge = None
        self.outputFile = None
        self.outputFileMatchString = None
        self.title = None
        self.titleMatchString = None
        self.trackOrder = None

        self.chaptersFiles = []
        self.filesInDirByKey = {}
        self.titles = []

        self.oAttachments = MKVAttachments()
        self.oSourceFiles = SourceFiles()

    def __bool__(self):
        return not self.__errorFound

    def __contains__(self, item):
        return item in self.__strCommands

    def __getitem__(self, index):
        return (
            self.__shellCommands[index],
            self.baseFiles,
            self.oSourceFiles[index],
            self.filesInDirByKey[_Key.outputFile][index],
            None if not self.oAttachments else self.oAttachments.attachmentsStr[index],
            None if not self.titles else self.titles[index],
            None if not self.chaptersFile else self.chaptersFiles[index],
        )

    def __len__(self):
        return self.__totalSourceFiles

    def __str__(self):

        strCommand = shlex.quote(str(self.mkvmerge))
        strCommand += " --ui-language " + self.language
        strCommand += " --output " + shlex.quote(str(self.outputFile))
        for oFile in self.oSourceFiles.sourceFiles:
            strCommand += " " + oFile.options
            strCommand += " '(' " + shlex.quote(str(oFile.fileName)) + " ')'"
        for oAttach in self.oAttachments.cmdLineAttachments:
            strCommand += " " + str(oAttach)
        if self.title:
            strCommand += " --title " + self.title
        if self.chaptersFile:
            strCommand += " --chapter-language " + self.chaptersLanguage
            strCommand += " --chapters " + shlex.quote(str(self.chaptersFile))
        strCommand += " --track-order " + self.trackOrder

        return strCommand

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

        return MKVCommandParser.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value

    @property
    def analysis(self):
        """
        results of analysis of the command

        Returns:
            list:

            list with comments of anything found
        """

        return self.__lstAnalysis

    @property
    def baseFiles(self):
        lstTmp = []
        lstTmp = [x.fileName for x in self.oSourceFiles.sourceFiles]

        return lstTmp

    @property
    def bashCommand(self):
        return self.__bashCommand

    @property
    def command(self):
        return self.__strCommand

    @command.setter
    def command(self, value):
        if isinstance(value, str):
            self._initVars()
            self.__strCommand = value
            strCommand = convertToBashStyle(self.__strCommand)
            self.__bashCommand = strCommand
            self._parse()
            self.__readFiles = True

    @property
    def commandsGenerated(self):
        return not self.__readFiles

    @property
    def destinationFiles(self):
        """
        destination files

        Returns:
            list:

            list with destination files
        """
        return self.filesInDirByKey[_Key.outputFile]

    @property
    def strCommands(self):
        return self.__strCommands

    @property
    def shellCommands(self):
        return self.__shellCommands

    def _parse(self):
        """
        _parse parse command line
        """

        strCommand = self.__bashCommand
        self.__lstAnalysis = []

        rg = r"^(.*?)\s--.*?--output.(.*?)\s--.*?\s'\('\s(.*?)\s'\)'.*?--track-order\s(.*)"

        reCommandEx = re.compile(rg)
        reExecutableEx = re.compile(r"^(.*?)\s--")
        reLanguageEx = re.compile(r"--ui-language (.*?) --")
        reOutputFileEx = re.compile(r".*?--output\s(.*?)\s--")
        reFilesEx = re.compile(
            (
                r"(?=--audio-tracks "
                r"|--video-tracks "
                r"|--subtitle-tracks "
                r"|--button-tracks "
                r"|--track-tags  "
                r"|--attachments "
                r"|--no-audio "
                r"|--no-video "
                r"|--no-subtitles "
                r"|--no-buttons "
                r"|--no-track-tags "
                r"|--no-chapters "
                r"|--no-global-tags "
                r"|--chapter-charset "
                r"|--chapter-language "
                r"|--language "
                r")"
                r"(.*?) '\(' (.*?) '\)'"
            )
        )
        reChaptersFileEx = re.compile(
            r"--chapter-language (.*?) --chapters (.*?) (?=--)"
        )
        self.__errorFound = False

        # To look Ok must match the 4 expected groups in the
        # command line
        # 1: mkvmerge name with fullpath
        # 2: output file
        # 3: at list one source
        # 4: track order
        if (matchCommand := reCommandEx.match(strCommand)) and (
            len(matchCommand.groups()) == 4  # pylint: disable=used-before-assignment
        ):
            self.trackOrder = matchCommand.group(4)
            self.__lstAnalysis.append("chk: Command seems ok.")
            try:
                d = ast.literal_eval("{" + self.trackOrder + "}")
                trackTotal = numberOfTracksInCommand(strCommand)
                s = self.trackOrder.split(",")
                if trackTotal == len(s):
                    for e in s:
                        if not e.find(":") > 0:
                            self.__errorFound = True
                else:
                    self.__errorFound = True
                if self.__errorFound:
                    self.__lstAnalysis.append(
                        "err: Number of tracks {} and track order of {} don't match.".format(
                            trackTotal, len(d)
                        )
                    )
            except SyntaxError:
                self.__lstAnalysis.append("err: Command track order bad format.")
                self.__errorFound = True
        else:
            self.__lstAnalysis.append("err: Command bad format.")
            self.__errorFound = True

        if matchUILanguage := reLanguageEx.search(strCommand):
            self.language = matchUILanguage.group(1)

        if matchExecutable := reExecutableEx.match(strCommand):
            f = stripEncaseQuotes(matchExecutable.group(1))
            p = Path(f)
            if p.is_file():
                self.mkvmerge = p
                self.__lstAnalysis.append("chk: mkvmerge ok - {}.".format(str(p)))
            else:
                self.__lstAnalysis.append(
                    "err: mkvmerge not found - {}.".format(str(p))
                )
                self.__errorFound = True
        else:
            self.__lstAnalysis.append("err: mkvmerge not found.")
            self.__errorFound = True

        if matchOutputFile := reOutputFileEx.match(strCommand):
            f = stripEncaseQuotes(matchOutputFile.group(1))
            f = f.replace(r"'\''", "'")
            p = Path(f)
            if Path(p.parent).is_dir():
                self.outputFile = p
                self.outputFileMatchString = matchOutputFile.group(1)
                self.__lstAnalysis.append(
                    "chk: Destination directory ok = {}.".format(str(p.parent))
                )
            else:
                self.outputFile = None
                self.__errorFound = True
                self.__lstAnalysis.append(
                    "err: Destination directory not found - {}.".format(str(p.parent))
                )
        else:
            self.__errorFound = True
            self.__lstAnalysis.append("err: No output file found in command.")

        if matchFiles := reFilesEx.finditer(strCommand):
            for index, match in enumerate(matchFiles):
                oFile = SourceFile(match.group(0))
                if oFile:
                    self.oSourceFiles.append(oFile)
                    if self.__totalSourceFiles is None:
                        self.__totalSourceFiles = len(oFile.filesInDir)
                    self.__lstAnalysis.append(
                        "chk: Source directory ok - {}.".format(
                            str(oFile.fileName.parent)
                        )
                    )
                    if index == 0:
                        self.filesInDirByKey[_Key.outputFile] = []
                        for f in oFile.filesInDir:
                            of = self.outputFile.parent.joinpath(f.stem + ".mkv")
                            of = resolveOverwrite(of)
                            self.filesInDirByKey[_Key.outputFile].append(of)
                    key = "<SOURCE{}>".format(str(index))
                    self.filesInDirByKey[key] = oFile.filesInDir
                    if len(oFile.filesInDir) != self.__totalSourceFiles:
                        self.__errorFound = True
                        self.__lstAnalysis.append(
                            "err: Error source files total mismatched." + match.group(0)
                        )
                else:
                    self.__errorFound = True
                    self.__lstAnalysis.append(
                        "err: Error reading source files." + match.group(2)
                    )
        else:
            self.__errorFound = True
            self.__lstAnalysis.append("err: No source file found in command.")

        #
        # Optional
        #
        if matchChaptersFile := reChaptersFileEx.search(strCommand):
            self.chaptersLanguage = matchChaptersFile.group(1)
            f = unQuote(matchChaptersFile.group(2))
            p = Path(f)
            if p.is_file():
                self.chaptersFile = p
                self.chaptersFileMatchString = matchChaptersFile.group(2)
                self.__lstAnalysis.append(
                    "chk: Chapters files directory ok = {}.".format(str(p.parent))
                )

    def _readDirs(self):
        """
        _readDirs read files in directories
        """

        reAttachmentsEx = re.compile(
            (
                r"--attachment-name (.*?) --attachment-mime-type "
                r"(.*?) --attach-file (.*?)(?= --)"
            )
        )

        if reAttachmentsEx.finditer(self.__bashCommand):
            self.oAttachments.strCommand = self.__bashCommand
            if self.oAttachments.isAttachmentsDirByEpisode:
                for oDir in self.oAttachments.attachmentsDirs:
                    self.__lstAnalysis.append(
                        "chk: Attachments directory ok - {}.".format(str(oDir))
                    )
            else:
                for oDir in self.oAttachments.cmdLineAttachmentsDirs:
                    self.__lstAnalysis.append(
                        "chk: Attachments directory ok - {}.".format(str(oDir))
                    )

        for f in self.oSourceFiles.sourceFiles[0].filesInDir:
            mediaInfo = MediaFileInfo(str(f))
            if mediaInfo:
                self.titles.append(mediaInfo.title)
            else:
                self.titles.append("")

        if self.chaptersFile:
            d = self.chaptersFile.parent
            fid = [x for x in d.glob("*" + self.chaptersFile.suffix) if x.is_file()]
            self.chaptersFiles.extend(fid)

        if self.log:
            for line in self.__lstAnalysis:
                if line.find("chk:") >= 0:
                    MODULELOG.debug("MCM0001: %s", line)
                elif line.find("err:") >= 0:
                    MODULELOG.error("MCM0002: %s", line)

    def _filesInDirByKey(self):

        if self.oAttachments.cmdLineAttachments:
            self.filesInDirByKey[
                _Key.attachmentFiles
            ] = self.oAttachments.attachmentsStr
        self.filesInDirByKey[_Key.title] = self.titles
        if self.chaptersFiles:
            self.filesInDirByKey[_Key.chaptersFile] = self.chaptersFiles

    def _template(self):

        cmdTemplate = self.__bashCommand
        cmdTemplate = cmdTemplate.replace(
            self.outputFileMatchString, _Key.outputFile, 1
        )
        for index, sf in enumerate(self.oSourceFiles.sourceFiles):
            key = "<SOURCE{}>".format(str(index))
            cmdTemplate = cmdTemplate.replace(sf.matchString, key, 1)
        if self.oAttachments.cmdLineAttachments:
            cmdTemplate = cmdTemplate.replace(
                self.oAttachments.attachmentsMatchString, _Key.attachmentFiles, 1
            )
        if self.title:
            cmdTemplate = cmdTemplate.replace(
                self.titleMatchString, "--title " + _Key.title, 1
            )
        if self.chaptersFile:
            cmdTemplate = cmdTemplate.replace(
                self.chaptersFileMatchString, _Key.chaptersFile, 1
            )
        self.commandTemplate = cmdTemplate

    def generateCommands(self):
        """
        generateCommands genrate and store all command lines needed
        """

        if not self.__errorFound:
            if self.__readFiles:
                self._readDirs()
                self._template()
                self._filesInDirByKey()
                self.__readFiles = False
            cmdTemplate = self.commandTemplate
            totalCommands = len(self.filesInDirByKey[_Key.outputFile])
            for i in range(totalCommands):
                keyDictionary = {}
                for key, sourceFiles in self.filesInDirByKey.items():
                    if key != _Key.attachmentFiles:
                        keyDictionary[key] = shlex.quote(str(sourceFiles[i]))
                    else:
                        keyDictionary[key] = sourceFiles[i]
                xLate = XLate(keyDictionary)  # instantiate regex dictionary translator
                strCommand = xLate.xLate(cmdTemplate)
                shellCommand = shlex.split(
                    strCommand
                )  # save command as shlex.split to submit to Pipe
                self.__strCommands.append(strCommand)
                self.__shellCommands.append(shellCommand)

    def renameOutputFiles(self, newNames):

        if len(newNames) == self.__totalSourceFiles:
            self.filesInDirByKey[_Key.outputFile] = list(newNames)
            if not self.__readFiles:
                self.generateCommands()

class _Key:

    attachmentFiles = "<ATTACHMENTS>"
    chaptersFile = "<CHAPTERS>"
    outputFile = "<OUTPUTFILE>"
    title = "<TITLE>"
