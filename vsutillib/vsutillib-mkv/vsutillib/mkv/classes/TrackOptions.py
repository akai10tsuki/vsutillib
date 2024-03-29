"""
Track Options - get the tracks options as set in cli
"""

import re
import shlex

from ..mkvutils import quoteString
from .MergeOptions import MergeOptions


class TrackOptions:
    """
    TrackOptions get the options for a source file found in the match string


    """

    def __init__(self, options=None):

        if options is not None:
            self.options = options

    def _initVars(self):

        self.__options = None
        self.__aParsedOptions = []
        self.__strOptions = []
        self.__dOptionsByTrack = {}
        self.__dTrackNames = {}
        self.__aTracks = []
        self.__translation = {}
        self.__fileOrder = None
        self.__mediaInfo = None
        self.__trackTitleEdited = {}
        self.__hasNamesToPreserve = False
        self.needTracksByTypeLanguage = {
            "Video": {"all": 0},
            "Audio": {"all": 0},
            "Text": {"all": 0},
        }

    @property
    def strIOptions(self):
        return self.__strOptions

    @property
    def parsedIOptions(self):
        return self.__aParsedOptions

    @property
    def fileOrder(self):
        return self.__fileOrder

    @fileOrder.setter
    def fileOrder(self, value):
        if isinstance(value, int):
            self.__fileOrder = value

    @property
    def mediaInfo(self):
        return self.__mediaInfo

    @mediaInfo.setter
    def mediaInfo(self, value):
        self.__mediaInfo = value
        self._tracksNeeded()
        self._trackTitlesEdited()

    @property
    def hasNamesToPreserve(self):
        return self.__hasNamesToPreserve

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, value):
        if isinstance(value, str):
            self._initVars()
            self.__options = value
            self._shlexSeparation()
            # self._parse()

    @property
    def trackNames(self):
        return self.__dTrackNames

    def trackNameMatch(self, track):
        """
        trackNameMatch track names

        Args:
            track (int, str): track number

        Returns:
            str: track name option
        """
        if isinstance(track, int):
            strTrack = str(track)
        if isinstance(track, str):
            strTrack = track

        strTmp = None
        if strTrack in self.trackNames:
            strTmp = "--track-name " + quoteString(self.trackNames[strTrack][0])

        return strTmp

    @property
    def tracks(self):
        return self.__aTracks

    @property
    def trackTitleEdited(self):
        return self.__trackTitleEdited

    @property
    def translation(self):
        return self.__translation

    @translation.setter
    def translation(self, value):
        if isinstance(value, dict):
            self.__translation = value

    @property
    def orderTranslation(self):
        """
        orderTranslation translation for --track-order option in template

        Returns:
            dict: dictionary with substitution key, value pairs
        """

        orderDict = {}
        for key in self.translation.keys():
            orderDict[str(self.fileOrder) + ":" + key] = (
                str(self.fileOrder) + ":" + self.translation[key]
            )
        return orderDict

    def optionsByTrack(self, track=None, general=False):
        """
        optionsByTrack return list with all parsed options by track

        Args:
            track (str, optional): track to get values if None return full dictionary.
                Defaults to None.

        Returns:
            list!dict: list with track options or full dictionary
        """

        if general:
            return self._strNonTrackIDOptions()
        if track is None:
            return self.__dOptionsByTrack
        strTmp = self.__dOptionsByTrack.get(track, None)

        return strTmp

    def strTrackName(self, track):
        """
        strOptionsByTrack recreate options with lookup in track substitution dictionary

        Args:
            track (str): track id

        Returns:
            str: option for track id
        """

        strTmp = ""
        aTmp = self.trackNames.get(track, None)
        if aTmp is not None:
            tmpTrack = self.translation.get(track, track)
            option =  tmpTrack + ":" + aTmp[1]
            option = quoteString(option)
            strTmp = "--track-name " + option

        return strTmp


    def strOptionsByTrack(self, track):
        """
        strOptionsByTrack recreate options with lookup in track substitution dictionary

        Args:
            track (str): track id

        Returns:
            str: option for track id
        """

        strTmp = ""
        aTmp = self.__dOptionsByTrack.get(track, None)
        for index, tTmp in enumerate(aTmp):
            track = self.translation.get(tTmp[1], tTmp[1])
            option = track + ":" + tTmp[2]
            if tTmp[0] == "--track-name":
                option = quoteString(option)
            if index == len(aTmp) - 1:
                strTmp += tTmp[0] + " " + option
            else:
                strTmp += tTmp[0] + " " + option + " "

        return strTmp

    def strOptions(self, translation=None):
        """
        strOptions reconstruct the options for a file with translation if any

        Args:
            translation (dict, optional): dictionary with substitution for
               the tracks. Defaults to None.

        Returns:
            str: full options with any translation
        """

        if isinstance(translation, dict):
            self.translation = translation

        strTmp = self._strNonTrackIDOptions()
        for index, track in enumerate(self.tracks):
            if index == len(self.tracks) - 1:
                strTmp += self.strOptionsByTrack(track)
            else:
                strTmp += self.strOptionsByTrack(track) + " "
        return strTmp

    def _strNonTrackIDOptions(self):
        """
        _strOptions takes care of any general options for a track

        Returns:
            str: string for general options for a track
        """

        mOptions = MergeOptions()

        strTmp = ""

        for tOption in self.__aParsedOptions:
            opt = tOption[0]
            if mOptions.hasTrackID(opt):
                # Since the general options are found first just skip
                # processing at first option with track ID
                break
            if opt in (
                "--video-tracks",
                "--audio-tracks",
                "--subtitle-tracks",
                "--button-tracks",
                "--track-tags",
                "--attachments",
            ):
                # These are options with tracks as paremeters
                tracks = tOption[1].split(",")
                newTracks = []
                for trk in tracks:
                    trans = self.__translation.get(trk, trk)
                    newTracks.append(trans)
                newStr = ""
                for trk in newTracks:
                    if not newStr:
                        newStr += trk
                    else:
                        newStr += "," + trk
                if not strTmp:
                    strTmp += opt + " " + newStr
                else:
                    strTmp += " " + opt + " " + newStr
            elif mOptions.hasParameter(opt):
                if not strTmp:
                    strTmp += tOption[0] + " " + tOption[1]
                else:
                    strTmp += " " + tOption[0] + " " + tOption[1]
            else:
                if not strTmp:
                    strTmp += opt
                else:
                    strTmp += " " + opt

        if strTmp:
            strTmp += " "

        return strTmp

    def _shlexSeparation(self):

        shellOptions = shlex.split(self.__options)
        mOptions = MergeOptions()

        trackOptions = []

        for index, option in enumerate(shellOptions):
            if mOptions.isTrackOption(option):
                parameter = (
                    None
                    if not mOptions.hasParameter(option)
                    else shellOptions[index + 1]
                )
                trackOptions.append([option, index, parameter])

        currentTrack = ""

        reTrackID = re.compile(r"(\d+):(.*?)$")

        index = -1

        for opt in trackOptions:

            if mOptions.hasTrackID(opt[0]):
                if match := reTrackID.match(opt[2]):
                    if currentTrack != match.group(1):
                        currentTrack = match.group(1)
                        index += 1
                        self.__strOptions.append("")
                        self.__strOptions[index] += opt[0] + " " + opt[2]
                    else:
                        self.__strOptions[index] += " " + opt[0] + " " + opt[2]
                    option = (opt[0], match.group(1), match.group(2))
                    self.__aParsedOptions.append(option)
                    if currentTrack not in self.__dOptionsByTrack.keys():
                        self.__dOptionsByTrack[currentTrack] = []
                        self.__aTracks.append(currentTrack)
                    self.__dOptionsByTrack[currentTrack].append(option)
                    if opt[0] == "--track-name":
                        self.__dTrackNames[currentTrack] = [opt[2], match.group(2)]
            else:
                index += 1
                self.__strOptions.append("")
                if mOptions.hasParameter(opt[0]):
                    self.__strOptions[index] += opt[0] + " " + opt[2]
                    self.__aParsedOptions.append((opt[0], opt[2], ""))
                else:
                    self.__strOptions[index] += opt[0]
                    self.__aParsedOptions.append((opt[0], "", ""))

    def _tracksNeeded(self):
        if self.mediaInfo:
            for nTrk in self.tracks:
                trk = self.mediaInfo[int(nTrk)]
                lang = trk.language
                if lang in self.needTracksByTypeLanguage[trk.trackType].keys():
                    self.needTracksByTypeLanguage[trk.trackType][lang] = (
                        self.needTracksByTypeLanguage[trk.trackType][lang] + 1
                    )
                else:
                    self.needTracksByTypeLanguage[trk.trackType][lang] = 1
                self.needTracksByTypeLanguage[trk.trackType]["all"] = (
                    self.needTracksByTypeLanguage[trk.trackType]["all"] + 1
                )

    def _trackTitlesEdited(self):

        self.__trackTitleEdited = {}

        #
        # BUG #9
        # Don't check titles for files that don't have any
        #
        if self.mediaInfo.hasMediaTracks:
            for key in self.trackNames:
                if self.mediaInfo[int(key)].title != self.trackNames[key][1]:
                    self.__trackTitleEdited[key] = True
                else:
                    self.__trackTitleEdited[key] = False
                    if not self.__hasNamesToPreserve:
                        self.__hasNamesToPreserve = True
