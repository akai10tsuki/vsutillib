"""
mkvUtils:

related to mkv application functionality
"""

import ast
import glob
import logging
import os
import platform
import re
import shlex

from pathlib import Path


from ..files import findFileInPath
from ..process import RunCommand


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


def getMKVMerge():
    """get the name of the mkvmerge executable in the system"""

    currentOS = platform.system()

    if currentOS == "Darwin":

        lstTest = glob.glob("/Applications/MKVToolNix*")
        if lstTest:
            f = lstTest[0] + "/Contents/MacOS/mkvmerge"
            mkvmerge = Path(f)
            if mkvmerge.is_file():
                return mkvmerge

    elif currentOS == "Windows":

        defPrograms64 = os.environ.get('ProgramFiles')
        defPrograms32 = os.environ.get('ProgramFiles(x86)')

        dirs = []
        if defPrograms64 is not None:
            dirs.append(defPrograms64)

        if defPrograms32 is not None:
            dirs.append(defPrograms32)

        # search 64 bits
        for d in dirs:
            search = sorted(Path(d).rglob("mkvmerge.exe"))
            if search:
                mkvmerge = Path(search[0])
                if mkvmerge.is_file():
                    return mkvmerge

    elif currentOS == "Linux":

        search = findFileInPath("mkvmerge")

        if search:
            for s in search:
                mkvmerge = Path(s)
                if mkvmerge.is_file():
                    return mkvmerge

    return None


def getMKVMergeVersion(mkvmerge):
    """get mkvmerge version"""

    s = mkvmerge

    if s[0:1] != "'" and s[-1:] != "'":
        s = shlex.quote(s)
        print(s)

    runCmd = RunCommand(s + " --version", regexsearch=r" v(.*?) ")

    if runCmd.run():
        return runCmd.regexmatch

    return None


def commandLooksOk(strCmd, lstResults=None):
    """
    Sanity check on command any failure results in no action whatsoever
    and since the original are not modified the resulting command should be safe

    :param strCommand: command line as generated by mkvtoolnix-gui
    :type strCommand: str
    :param lstResults: list to put analysis messages
    :type lstResults: list
    :rtype: bool
    """

    if not strCmd:
        return False

    strCommand = strStripEscapeChars(strCmd)  # Comvert line to bash style

    lstAnalysis = []

    #rg = r"^'(.*?)'\s.*?\-\-output.'(.*?)'\s.*?\s'\('\s'(.*?)'\s'\)'.*?\-\-track-order\s(.*)"  # pylint: disable=C0301
    #rg = r"^'(.*?)'\s.*?\-\-output.'(.*?)'\s.*?\s'\('\s'(.*?)'\s'\)'.*?\-\-track-order\s(.*)"  # pylint: disable=C0301
    rg = r"^(.*?)\s\-\-.*?\-\-output.(.*?)\s\-\-.*?\s'\('\s(.*?)\s'\)'.*?\-\-track-order\s(.*)"

    regCommandEx = re.compile(rg)
    matchCommand = regCommandEx.match(strCommand)

    reExecutableEx = re.compile(r"^(.*?)\s\-\-")
    matchExecutable = reExecutableEx.match(strCommand)

    reOutputFileEx = re.compile(r".*?\-\-output\s(.*?)\s\-\-")
    matchOutputFile = reOutputFileEx.match(strCommand)

    reChaptersFileEx = re.compile(r".*?\-\-chapters\s(.*?)\s\-\-")
    matchChaptersFile = reChaptersFileEx.match(strCommand)

    reSourcesEx = re.compile(r"'\('\s(.*?)\s'\)'")
    matchSources = reSourcesEx.finditer(strCommand)

    reAttachmentsEx = re.compile(r"\-\-attach-file.(.*?)\s\-\-")
    matchAttachments = reAttachmentsEx.finditer(strCommand)

    bOk = True
    trackOrder = None
    # To look Ok must match the 5 group in the command line that
    # are expected
    # 1: mkvmerge name with fullpath
    # 2: output file
    # 3: at list one source
    # 4: track order
    if matchCommand and (len(matchCommand.groups()) == 4):
        lstAnalysis.append("Command seems ok.")
        trackOrder = matchCommand.group(4)
    else:
        if lstResults is None:
            return False
        lstAnalysis.append("Command bad format.")
        bOk = False

    if trackOrder is not None:
        try:
            d = ast.literal_eval("{" + trackOrder + "}")
            trackTotal = numberOfTracksInCommand(strCommand)

            s = trackOrder.split(',')
            if trackTotal == len(s):
                for e in s:
                    if not e.find(':') > 0:
                        bOk = False
            else:
                bOk = False

            if not bOk:
                if lstResults is None:
                    return False
                lstAnalysis.append("Number of tracks {} and track order of {} don't match.".format(trackTotal, len(d)))

        except SyntaxError:
            if lstResults is None:
                return False
            lstAnalysis.append("Command track order bad format.")
            bOk = False

    if matchExecutable:
        f = stripEncaseQuotes(matchExecutable.group(1))
        p = Path(f)
        if not p.is_file():
            if lstResults is None:
                return False
            lstAnalysis.append("mkvmerge not found - {}.".format(str(p)))
            bOk = False
        else:
            lstAnalysis.append("mkvmerge ok - {}".format(str(p)))
    else:
        if lstResults is None:
            return False
        lstAnalysis.append("mkvmerge not found.")
        bOk = False

    if matchOutputFile:
        f = stripEncaseQuotes(matchOutputFile.group(1))
        f = f.replace(r"'\''", "'")
        p = Path(f)

        if not Path(p.parent).is_dir():
            lstAnalysis.append("Destination directory not found - {}.".format(str(p.parent)))
            if lstResults is None:
                return False
            bOk = False
        else:
            lstAnalysis.append("Destination directory ok = {}".format(str(p.parent)))

    else:
        if lstResults is None:
            return False
        lstAnalysis.append("Destination directory not found.")
        bOk = False

    if matchSources:
        n = 1
        for match in matchSources:
            f = stripEncaseQuotes(match.group(1))
            f = f.replace(r"'\''", "'")
            p = Path(f)

            if not Path(p.parent).is_dir():
                if lstResults is None:
                    return False
                lstAnalysis.append("Source directory {} not found {}".format(n, str(p.parent)))
                bOk = False
            else:
                lstAnalysis.append("Source directory {} ok = {}".format(n, str(p.parent)))

            if not Path(p).is_file():
                if lstResults is None:
                    return False
                lstAnalysis.append("Source file {} not found {}".format(n, str(p)))
                bOk = False
            else:
                lstAnalysis.append("Source file {} ok = {}".format(n, str(p)))


            n += 1

        if n == 1:
            # if the command is so bad matchSources for loop won't run
            lstAnalysis.append("Source directory not found.")
            bOk = False
    else:
        if lstResults is None:
            return False
        lstAnalysis.append("Source directory not found.")
        bOk = False

    # Check for optional chapters file
    if matchChaptersFile:
        f = stripEncaseQuotes(matchChaptersFile.group(1))
        p = Path(f)
        print(p)
        if not p.is_file():
            if lstResults is None:
                return False
            lstAnalysis.append("Chapters file not found - {}.".format(str(p)))
            bOk = False
        else:
            lstAnalysis.append("Chapters file ok - {}".format(str(p)))

    # This check if for optional attachments files
    n = 1
    for match in matchAttachments:
        f = stripEncaseQuotes(match.group(1))
        f = f.replace(r"'\''", "'")
        p = Path(p)
        if not p.is_file():
            lstAnalysis.append("Attachment {} not found - {}".format(n, str(p)))
            if lstResults is None:
                return False
            bOk = False
        else:
            lstAnalysis.append("Attachment {} ok = {}".format(n, str(p)))
        n += 1

    if lstResults is not None:
        for e in lstAnalysis:
            lstResults.append(e)

    return bOk


def numberOfTracksInCommand(strCmd):
    """
    Every track have a --language option count
    them to know the number of tracks

    :param strCmd: command line
    :type strCmd: str
    :rtype: int
    """

    reLanguageEx = re.compile(r"\-\-language (.*?)\s")
    matchLanguage = reLanguageEx.findall(strCmd)

    return len(matchLanguage)


def stripEncaseQuotes(strFile):
    """
    Strip single quote at start and end of file name
    if the exists use for
    """

    s = str(strFile)

    if (s[0:1] == "'") and (s[-1:] == "'"):
        s = s[1:-1]

    return s


def strStripEscapeChars(strCommand):
    """
    Strip escape windows chars for the command line
    in the end they won't be used in a shell
    the resulting command is bash/zh like
    """

    strTmp = strCommand

    if strTmp.find(r'^"^(^"') >= 0:
        # This is for cmd in Windows
        strTmp = strTmp.replace("'", r"'\''").replace('^', '').replace('/', '\\').replace('"', "'")

    return strTmp
