"""
mkvUtils:

related to mkv application functionality
"""

import glob
import logging
import os
import platform
import re
import shlex

from pathlib import Path

from vsutillib.files import findFileInPath
from vsutillib.process import RunCommand

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


def getMKVMerge():
    """
    get the name of the mkvmerge executable in the system
    search in the standard programs directories

    Returns:
        pathlib.Path:

        fully qualified mkvmerge executable
    """

    if (currentOS := platform.system()) == "Darwin":

        if lstTest := glob.glob("/Applications/MKVToolNix*"):

            f = lstTest[0] + "/Contents/MacOS/mkvmerge"

            if (mkvmerge := Path(f)).is_file():
                return mkvmerge

    elif currentOS == "Windows":

        dirs = []
        dirs.append(os.environ.get("ProgramFiles") or "")
        dirs.append(os.environ.get("ProgramFiles(x86)") or "")

        for d in dirs:
            if search := sorted(Path(d).rglob("mkvmerge.exe")):

                if (mkvmerge := Path(search[0])).is_file():
                    return mkvmerge

    elif currentOS == "Linux":

        if search := findFileInPath("mkvmerge"):

            for s in search:

                if (mkvmerge := Path(s)).is_file():
                    return mkvmerge

    return None


def getMKVMergeVersion(mkvmerge):
    """
    get mkvmerge version

    Args:
        mkvmerge (str): mkvmerge executable with full path

    Returns:
        str:

        version of mkvmerge
    """

    s = mkvmerge

    if s[0:1] != "'" and s[-1:] != "'":
        s = shlex.quote(s)

    runCmd = RunCommand(s + " --version", regexsearch=r" v(.*?) ")

    if runCmd.run():
        return runCmd.regexmatch[0]

    return None


def stripEncaseQuotes(strFile):
    """
    Strip single quote at start and end of file name
    if they are found

    Args:
        strFile (str): file name

    Returns:
        str:

        file name without start and end single quoute
    """

    # Path or str should work
    s = str(strFile)

    if (s[0:1] == "'") and (s[-1:] == "'"):
        s = s[1:-1]

    return s


def convertToBashStyle(strCommand):
    """
    Strip escape windows chars for the command line
    in the end they won't be used in a shell
    the resulting command is bash/zh like

    Args:
        strCommand (str): command generated by mkvtoolnix-gui

    Returns:
        str:

        cli command converted to bash style
    """

    strTmp = strCommand

    if strTmp.find(r'^"^(^"') >= 0:
        # This is for cmd in Windows
        strTmp = (
            strTmp.replace("'", r"'\''")
            .replace("^", "")
            .replace("/", "\\")
            .replace('"', "'")
        )

    return str(strTmp)


def numberOfTracksInCommand(strCmd):
    """
    Every track have a --language option count
    them to know the number of tracks

    Args:
        strCmd(str): command line

    Returns:
        int:

        total number of tracks
    """

    reLanguageEx = re.compile(r"\-\-language (.*?)\s")
    matchLanguage = reLanguageEx.findall(strCmd)

    return len(matchLanguage)


def resolveOverwrite(fileName, strPrefix="new-"):
    """
    resolveOverwrite resolve overwrite collisions

    Args:
        fileName (Path): desired file name to use
        strPrefix (str, optional): prefix to use for new name. Defaults to "new-".

    Returns:
        Path: Path object with the new file name.
    """

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

    return fileNameTmp


def unQuote(fileName):
    """
    Remove start end quotes and escape ones
    Args:
        fileName (str): file name

    Returns:
        str:

        file name without quotes if found
    """

    f = stripEncaseQuotes(fileName)
    f = f.replace(r"'\''", "'")

    return f

def quoteString(string):

    f = string.replace("'", r"'\''")
    f = "'" + f + "'"

    return f

def strPath(value):
    """
    Convenience function to help sort

    Arguments:
        value {various types} -- value to convert to string

    Returns:
        str -- argument received converted to string
    """
    return str(value)
