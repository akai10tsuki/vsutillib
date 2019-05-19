"""
File utilities
"""


import os
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
