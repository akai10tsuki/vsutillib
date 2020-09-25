"""
class to parse media names

The name are expected to use media server naming
conventions:

1 Movie:  Title (year) - extra.mkv

2 Series:

    Series Title (year)/Season ##/Series Title - S##E##.mkv

    for series fullpath is needed to obtain the information needed.

"""

import logging
import re

from pathlib import Path


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class ParseMediaFileName():
    """
    Look for title, year, season and episode
    in the media file name
    """

    def __init__(self, strMediaFileName=None):

        self.title = None
        self.year = None

        self.season = None
        self.episode = None

        self.isFile = False
        self.isDir = False
        self.isString = False
        self.isTV = False
        self.isMovie = False

        if strMediaFileName is not None:
            self.parseFileName(strMediaFileName)

    def parseFileName(self, strMF, onlyName=False):
        """
        Parse file name for title, year
        and season, episode

        if strMF is:
            dir - should be for tv series
            file - it can be search for all tv information at once
            string - can be tv series or movie
        """

        p = Path(strMF)

        # repeat for pylint message declare out of init
        self.title = None
        self.year = None

        self.season = None
        self.episode = None

        self.isFile = p.is_file()
        self.isDir = p.is_dir()
        self.isString = not self.isDir and not self.isFile

        if onlyName:

            rc = self._parseAsString(strMF, p)

        else:

            rc = self._parseAsFile(strMF, p)

            if not rc:

                rc = self._parseAsString(strMF, p)

    def _parseAsString(self, strMF, p):

        regTitleYear = re.compile(r'(.*?) \((\d+)\)')
        regSeasonEpisode = re.compile(r'[sS](\d+)[eE](\d+)')
        #regNoTitle = re.compile(r'.*[sS](\d+)[eE](\d+)$')

        name = None

        if p.is_file():
            name = p.stem
        elif self.isString:
            name = strMF

        if name is not None:

            ty = regTitleYear.search(name)
            se = regSeasonEpisode.search(name)

            if ty:
                self.title = ty.group(1)
                self.year = ty.group(2)

            if se:
                self.season = se.group(1)
                self.episode = se.group(2)
                self.isTV = True

            if se or ty:
                return True

        return False

    def _parseAsFile(self, strMF, p):

        regAll = re.compile(r'.*[\\\/](.*?) \((\d+)\).*?[sS](\d+)[eE](\d+)') # File full path for tv series

        if self.isString:
            fn = strMF
        else:
            fn = str(p)

        fn += " S999E999"  # in case of movie regular expresion will work

        m = regAll.search(fn)

        if m:

            self.title = m.group(1)
            self.year = m.group(2)

            if m.group(3) != "999":
                self.season = m.group(3)
                self.episode = m.group(4)
                self.isTV = True

            if p.is_file() and (m.group(3) == "999"):
                self.isMovie = True
            elif not self.isTV:
                self.isTV = True

            return True

        return False
