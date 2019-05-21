"""
File utilities
"""


import os
import platform
from pathlib import Path, PurePath


def findFile(element, dirPath=None):
    """find file in the path"""

    if dirPath is None:
        dirPath = os.getenv('PATH')

    if isinstance(dirPath, str):
        dirs = dirPath.split(os.pathsep)
    else:
        dirs = dirPath

    for dirname in dirs:
        candidate = Path(PurePath(dirname).joinpath(element))
        if candidate.is_file():
            return candidate

    return None

def getFileList(strPath, wildcard=None, fullpath=False, recursive=False, strName=False):
    """
    Get files in a directory
    strPath has to be an existing directory or file
    in case of a file the parent directory is used
    strExtFilter in the form -> .ext
    """
    p = Path(strPath)

    if not p.is_file() and not p.is_dir():
        return []

    lstFilesFilter = []

    if p.is_file():
        p = p.parent

    if wildcard is None:
        wc = "*.*"
    else:
        wc = wildcard

    if recursive:
        wc = "**/" + wc

    lstObjFileNames = [x for x in p.glob(wc) if x.is_file()]

    if not fullpath:
        lstFilesFilter = [x.name for x in lstObjFileNames]
        return lstFilesFilter

    if strName:
        lstFilesFilter = [str(x) for x in lstObjFileNames]
        return lstFilesFilter

    return lstObjFileNames

def getExecutable(search):
    """get executable"""

    fileToSearch = search

    currentOS = platform.system()

    if currentOS == "Darwin":

        lstTest = Path("/Applications").glob('**/' + fileToSearch)

        for l in lstTest:
            p = Path(l)
            if p.stem == fileToSearch:
                return p

    elif currentOS == "Windows":

        if fileToSearch.find('.') < 0:
            # assume is binary executable
            fileToSearch += '.exe'

        defPrograms64 = os.environ.get('ProgramFiles')
        defPrograms32 = os.environ.get('ProgramFiles(x86)')

        dirs = []
        if defPrograms64 is not None:
            dirs.append(defPrograms64)

        if defPrograms32 is not None:
            dirs.append(defPrograms32)

        # search 64 bits
        for d in dirs:
            search = sorted(Path(d).rglob(fileToSearch))
            if search:
                executable = Path(search[0])
                if executable.is_file():
                    return executable

    search = findFile(fileToSearch)

    if search is not None:
        executable = Path(search)
        if executable.is_file():
            return executable

    return None
