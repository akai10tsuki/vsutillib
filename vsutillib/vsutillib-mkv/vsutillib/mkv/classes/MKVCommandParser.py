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


Properties update

<MKVPROPEDIT.EXE> <SOURCE> --edit info --set title=<TITLE>

"""
# MCP0003

import ast
import logging
import platform
import re
import shlex

from pathlib import Path

from natsort import natsorted, ns

from vsutillib.media import MediaFileInfo
from vsutillib.misc import XLate


from ..mkvutils import (
    convertToBashStyle,
    generateCommand,
    numberOfTracksInCommand,
    resolveOverwrite,
    stripEncaseQuotes,
    unQuote,
)

from .SourceFiles import SourceFile, SourceFiles
from .mkvattachments import MKVAttachments

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class MKVCommandParser:
    """
    Class for parsing CLI **mkvmerge** command part of MKVToolnix_

    Args:
        strCommand (`str`, optional): command line as generated by mkvtoolnix-gui
    """

    __log = False

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
        self.__strOCommands = []
        self.__setTitles = False

        self.cliChaptersFile = None
        self.cliChaptersFileMatchString = None
        self.chaptersLanguage = None
        self.commandTemplate = None
        self.language = None
        self.mkvmerge = None
        self.mkvpropedit = None
        self.cliOutputFile = None
        self.cliOutputFileMatchString = None
        self.cliTitleMatchString = None
        self.cliTracksOrder = None

        self.commandTemplates = []
        self.tracksOrder = []
        self.translations = None
        self.chaptersFiles = []
        self.filesInDirByKey = {}
        self.dirsByKey = {}
        self.titles = []

        self.oAttachments = MKVAttachments()
        self.oBaseFiles = []
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
            self.filesInDirByKey[MKVParseKey.outputFile][index],
            None if not self.oAttachments else self.oAttachments.attachmentsStr[index],
            None if not self.titles else self.titles[index],
            None if not self.cliChaptersFile else self.chaptersFiles[index],
        )

    def __len__(self):
        return self.__totalSourceFiles

    def __str__(self):
        return self.__strCommand

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

            if self.__strCommand:
                self._removeTitle()

                strCommand = convertToBashStyle(self.__strCommand)

                self.__bashCommand = strCommand
                self._parse()
                if not self.__errorFound:
                    self.translations = [None] * self.__totalSourceFiles
                self.__readFiles = True
                self.readFiles()
                self.generateCommands()

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

        if MKVParseKey.outputFile in self.filesInDirByKey:
            return self.filesInDirByKey[MKVParseKey.outputFile]

        return []

    @property
    def outputFileExtension(self):
        if isinstance(self.cliOutputFile, Path):
            return self.cliOutputFile.suffix
        return None

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
        rgOneTrack = r"^(.*?)\s--.*?--output.(.*?)\s--.*?\s'\('\s(.*?)\s'\)'.*?"

        reCommandEx = re.compile(rg)
        reCommandOneTrackEx = re.compile(rgOneTrack)
        reExecutableEx = re.compile(r"^(.*?)\s--")
        reLanguageEx = re.compile(r"--ui-language (.*?) --")
        reOutputFileEx = re.compile(r".*?--output\s(.*?)\s--")

        reFilesEx = re.compile(
            (
                r"(?=--audio-tracks "
                r"|--video-tracks "
                r"|--subtitle-tracks "
                r"|--button-tracks "
                r"|--track-tags "
                r"|--attachments "
                r"|--no-audio "
                r"|--no-video "
                r"|--no-subtitles "
                r"|--no-buttons "
                r"|--no-track-tags "
                r"|--no-chapters "
                r"|--no-attachments "
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
            self.cliTracksOrder = matchCommand.group(4)
            self.__lstAnalysis.append("chk: Command seems ok.")
            try:
                d = ast.literal_eval("{" + self.cliTracksOrder + "}")
                trackTotal = numberOfTracksInCommand(strCommand)
                s = self.cliTracksOrder.split(",")
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
        elif (matchCommand := reCommandOneTrackEx.match(strCommand)) and (
            len(matchCommand.groups()) == 3  # pylint: disable=used-before-assignment
        ):
            self.cliTracksOrder = None
            self.__lstAnalysis.append("chk: Command seems ok.")
        else:
            self.__lstAnalysis.append("err: Command bad format.")
            self.__errorFound = True

        if matchUILanguage := reLanguageEx.search(strCommand):
            self.language = matchUILanguage.group(1)

        if matchExecutable := reExecutableEx.match(strCommand):
            f = stripEncaseQuotes(matchExecutable.group(1))
            p = Path(f)
            try:
                test = p.is_file()
            except OSError:
                self.__lstAnalysis.append(
                    "err: mkvmerge incorrect syntax - {}.".format(str(p))
                )
                self.__errorFound = True
            else:
                if test:
                    self.mkvmerge = p
                    self.mkvpropedit = str(p.parent) + "mkvpropedit"
                    self.__lstAnalysis.append("chk: mkvmerge ok - {}.".format(str(p)))
                else:
                    self.__lstAnalysis.append(
                        "err: mkvmerge not found - {}.".format(str(p))
                    )
                    self.__errorFound = True
        else:
            self.__lstAnalysis.append("err: mkvmerge not found in command.")
            self.__errorFound = True

        if matchOutputFile := reOutputFileEx.match(strCommand):
            self.cliOutputFile = None
            self.cliOutputFileMatchString = None
            f = stripEncaseQuotes(matchOutputFile.group(1))
            f = f.replace(r"'\''", "'")
            p = Path(f)
            try:
                test = Path(p.parent).is_dir()
            except OSError:
                self.__errorFound = True
                self.__lstAnalysis.append(
                    "err: Destination directory incorrect syntax - {}.".format(
                        str(p.parent)
                    )
                )
            else:
                if test:
                    self.cliOutputFile = p
                    self.cliOutputFileMatchString = matchOutputFile.group(1)
                    self.__lstAnalysis.append(
                        "chk: Destination directory ok = {}.".format(str(p.parent))
                    )
                else:
                    self.__errorFound = True
                    self.__lstAnalysis.append(
                        "err: Destination directory not found - {}.".format(
                            str(p.parent)
                        )
                    )
        else:
            self.__errorFound = True
            self.__lstAnalysis.append("err: No output file found in command.")

        if matchFiles := reFilesEx.finditer(strCommand):
            for index, match in enumerate(matchFiles):
                oFile = SourceFile(match.group(0), index)
                if oFile:
                    self.oBaseFiles.append(oFile)
                    self.oSourceFiles.append(oFile)
                    if self.__totalSourceFiles is None:
                        self.__totalSourceFiles = len(oFile.filesInDir)
                        self.tracksOrder = [
                            self.cliTracksOrder
                        ] * self.__totalSourceFiles
                    self.__lstAnalysis.append(
                        "chk: Source directory ok - {}.".format(
                            str(oFile.fileName.parent)
                        )
                    )
                    if index == 0:
                        self.filesInDirByKey[MKVParseKey.outputFile] = []
                        self.dirsByKey[MKVParseKey.outputFile] = ""
                        for f in oFile.filesInDir:
                            if self.dirsByKey[MKVParseKey.outputFile] == "":
                                self.dirsByKey[
                                    MKVParseKey.outputFile
                                ] = oFile.fileName.parent

                            of = self.cliOutputFile.parent.joinpath(
                                f.stem + self.outputFileExtension
                            )
                            of = resolveOverwrite(of)
                            self.filesInDirByKey[MKVParseKey.outputFile].append(of)
                    key = "<SOURCE{}>".format(str(index))
                    self.filesInDirByKey[key] = oFile.filesInDir
                    self.dirsByKey[key] = oFile.fileName.parent
                    if len(oFile.filesInDir) != self.__totalSourceFiles:
                        self.__errorFound = True
                        self.__lstAnalysis.append(
                            "err: Error source files TOTAL mismatched." + match.group(0)
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
            self.cliChaptersFile = None
            self.cliChaptersFileMatchString = None
            f = unQuote(matchChaptersFile.group(2))
            p = Path(f)
            try:
                test = p.is_file()
            except OSError:
                self.__lstAnalysis.append(
                    "err: Chapters file incorrect syntax - {}.".format(str(p))
                )
                self.__errorFound = True
            else:
                if test:
                    self.cliChaptersFile = p
                    self.cliChaptersFileMatchString = matchChaptersFile.group(2)
                    self.__lstAnalysis.append(
                        "chk: Chapters file ok - {}.".format(str(p.parent))
                    )
                else:
                    self.__lstAnalysis.append(
                        "chk: Chapters file not found - {}.".format(str(p.parent))
                    )
                    self.__errorFound = True

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

        # Attachments can be in command for all files or one directory per file
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

        # get title from first source file and use that if defined
        if self.__setTitles:
            for f in self.oSourceFiles.sourceFiles[0].filesInDir:
                mediaInfo = MediaFileInfo(str(f))
                if mediaInfo:
                    self.titles.append(mediaInfo.title)
                else:
                    self.titles.append("")

        if self.cliChaptersFile:
            d = self.cliChaptersFile.parent
            fid = [x for x in d.glob("*" + self.cliChaptersFile.suffix) if x.is_file()]
            fid = natsorted(fid, alg=ns.PATH)
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
                MKVParseKey.attachmentFiles
            ] = self.oAttachments.attachmentsStr
        if self.__setTitles:
            self.filesInDirByKey[MKVParseKey.title] = self.titles
        if self.chaptersFiles:
            self.filesInDirByKey[MKVParseKey.chaptersFile] = self.chaptersFiles

    def _template(self):

        cmdTemplate = self.__bashCommand

        reExecutableEx = re.compile(r"^(.*?)\s--")
        if matchExecutable := reExecutableEx.match(cmdTemplate):
            m = matchExecutable.group(1)
            f = stripEncaseQuotes(m)
            e = shlex.quote(f)

            ##
            # BUG 1
            # Reported by zFerry98
            #
            # When running in Windows there is no space in the mkvmerge executable path
            # \ is use as escape
            # Command: ['C:binmkvtoolnixmkvmerge.exe', ...
            #
            # Solution:
            #   Force quotes for mkvmerge executable
            #
            #   Command: ['C:\\bin\\mkvtoolnix\\mkvmerge.exe'
            ##
            if platform.system() == "Windows":
                if e[0:1] != "'":
                    e = "'" + f + "'"
            ##

            cmdTemplate = self.__bashCommand
            cmdTemplate = cmdTemplate.replace(m, e, 1)
            cmdTemplate = cmdTemplate.replace(
                self.cliOutputFileMatchString, MKVParseKey.outputFile, 1
            )
            for index, sf in enumerate(self.oSourceFiles.sourceFiles):
                key = "<SOURCE{}>".format(str(index))
                cmdTemplate = cmdTemplate.replace(sf.matchString, key, 1)
            if self.oAttachments.cmdLineAttachments:
                cmdTemplate = cmdTemplate.replace(
                    self.oAttachments.attachmentsMatchString,
                    MKVParseKey.attachmentFiles,
                    1,
                )
            ##
            # Bug #3
            #
            # It was not preserving the episode title
            #
            # Remove title before parsing and added the <TITLE> key to the template
            # If there is no title read --title '' will be used.
            # working with \ ' " backslash, single and double quotes in same title
            ##

            # Add title to template
            if self.__setTitles:
                if self.cliTracksOrder:
                    cmdTemplate = cmdTemplate.replace(
                        "--track-order",
                        "--title " + MKVParseKey.title + " --track-order",
                        1,
                    )
                else:
                    cmdTemplate += "--title " + MKVParseKey.title

            if self.cliChaptersFile:
                cmdTemplate = cmdTemplate.replace(
                    self.cliChaptersFileMatchString, MKVParseKey.chaptersFile, 1
                )

            if self.cliTracksOrder:
                cmdTemplate = cmdTemplate.replace(
                    self.cliTracksOrder, MKVParseKey.trackOrder, 1
                )

            self.commandTemplate = cmdTemplate
            self.commandTemplates = [cmdTemplate] * len(self)

    def _removeTitle(self):
        """
        _removeTitle remove --title option from command
        """

        ##
        # Bug #3
        #
        # It was not preserving the episode title
        #
        # Remove title before parsing and added the <TITLE> key to the template
        # If there is no title read --title '' will be used.
        # working with \ ' " backslash, single and double quotes in same title
        ##

        reTitleEx = re.compile(r".*?--title\s(.*?)\s--")

        if matchTitle := reTitleEx.match(self.__strCommand):
            self.cliTitleMatchString = matchTitle.group(1)

            self.__strCommand = self.__strCommand.replace(
                "--title " + self.cliTitleMatchString + " ", "", 1
            )

    def createKeysDictionary(self, index):
        """
        createKeysDictionary create a keys dictionary for template substitution

        Args:
            index (int): command index

        Returns:
            dict: dictionary of keys
        """

        keyDictionary = {}
        for key, sourceFiles in self.filesInDirByKey.items():
            if key != MKVParseKey.attachmentFiles:
                keyDictionary[key] = shlex.quote(str(sourceFiles[index]))
            else:
                keyDictionary[key] = sourceFiles[index]
        keyDictionary[MKVParseKey.trackOrder] = self.tracksOrder[index]

        return keyDictionary

    def readFiles(self):
        if not self.__errorFound:
            self._readDirs()
            self._template()
            self._filesInDirByKey()

    def generateCommands(self):
        """
        generateCommands genrate and store all command lines needed
        """

        if not self.__errorFound:
            totalCommands = len(self.filesInDirByKey[MKVParseKey.outputFile])
            self.__strCommands = []
            self.__shellCommands = []

            for i in range(totalCommands):

                self.__strCommands.append(None)
                self.__shellCommands.append(None)

                _, _ = self.generateCommandByIndex(i, update=True)


    def generateCommandByIndex(self, index, update=False):
        """
        generateCommandByIndex generate a command for a determined index

        Args:
            index (int): index of command been worked on
            shell (bool, optional): If True return a shell command for subprocess
                otherwise return cli command. Defaults to False.

        Returns:
            str: final command
        """

        cmdTemplate = self.commandTemplates[index]
        keyDictionary = self.createKeysDictionary(index)
        strCommand = generateCommand(cmdTemplate, keyDictionary)
        shellCommand = shlex.split(
            strCommand
        )  # save command as shlex.split to submit to Pipe

        if update:
            self.__strCommands[index] = strCommand
            self.__shellCommands[index] = shellCommand

        return strCommand, shellCommand

    def renameOutputFiles(self, newNames):

        if len(newNames) == self.__totalSourceFiles:
            self.filesInDirByKey[MKVParseKey.outputFile] = list(newNames)
            self.generateCommands()


class MKVParseKey:

    attachmentFiles = "<ATTACHMENTS>"
    chaptersFile = "<CHAPTERS>"
    outputFile = "<OUTPUTFILE>"
    title = "<TITLE>"
    trackOrder = "<ORDER>"
