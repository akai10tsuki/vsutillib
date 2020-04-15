"""
 convenience classes
"""

import re

from pathlib import Path

from ..mkvutils import unQuote


class SourceFile:
    """
     Tracks and file names
    """

    def __init__(self, fullMatchString=None):

        self.__fullMatchString = None
        self.__errorFound = False
        self.options = None
        self.tracks = []
        self.filesInDir = []
        self.fileName = None
        self.matchString = None

        self.fullMatchString = fullMatchString

    def _parse(self):

        reTrackEx = re.compile(r"(?=--language )(.*?) (?=--language|'\(')")
        reOptionsEx = re.compile(
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
                r")(.*?) (?='\(')"
            )
        )
        reSourcesEx = re.compile(r"'\('\s(.*?)\s'\)'")
        self.tracks = []
        self.fileName = []

        if self.__fullMatchString:
            if match := reTrackEx.finditer(self.__fullMatchString):
                for m in match:
                    self.tracks.append(m.group(1))
            if match := reOptionsEx.search(self.__fullMatchString):
                self.options = match.group(1)
            else:
                self.__errorFound = True
            if match := reSourcesEx.search(self.__fullMatchString):
                f = unQuote(match.group(1))
                p = Path(f)

                if p.is_file():
                    self.fileName = p
                    self.matchString = match.group(0)
                    d = p.parent
                    fid = [x for x in d.glob("*" + p.suffix) if x.is_file()]
                    self.filesInDir.extend(fid)
            else:
                self.__errorFound = True

    def __bool__(self):
        return not self.__errorFound

    @property
    def directory(self):
        return self.fileName.parent

    @property
    def fullMatchString(self):
        return self.__fullMatchString

    @fullMatchString.setter
    def fullMatchString(self, value):
        if isinstance(value, str):
            self.__fullMatchString = value
            self._parse()


class Attachment:  # pylint: disable=too-few-public-methods
    """
    Class to save attachment information

    """

    def __init__(self, attachment, span=None, matchString=None):

        self.name = None
        self.mimeType = None
        self.fileName = None

        if isinstance(attachment, tuple):
            self.name = attachment[0]
            self.mimeType = attachment[1]

            f = unQuote(attachment[2])
            p = Path(f)

            if p.is_file():
                self.fileName = p

        self.span = span
        self.matchString = matchString

    def __str__(self):

        return self.matchString
