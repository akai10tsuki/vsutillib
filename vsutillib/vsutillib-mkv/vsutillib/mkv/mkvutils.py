"""
mkvUtils:

related to mkv application functionality
"""

import glob
import logging
import os
import platform
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
