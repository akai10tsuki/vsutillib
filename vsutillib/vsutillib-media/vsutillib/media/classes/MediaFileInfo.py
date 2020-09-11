"""
Get file structure information from media file
"""

# MFI0001

import base64
import logging

from pymediainfo import MediaInfo

from vsutillib.misc import iso639

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class MediaFileInfo:
    """
    Media file properties
    This class main function is to verify that the structure of the files
    is the same:

        Same order of tracks
        Same language if it applies

    Args:

        strMediaFile (str): name with fullpath of source file

    Attributes:

        lstMediaTracks (MediaTrackInfo): list of media tracks
            found
    """

    # log state
    __log = False

    def __init__(self, mediaFile, log=None):

        self.fileName = mediaFile
        self.mediaInfo = None
        self.codec = ""
        self.format = ""
        self.title = ""
        self.menu = ""
        self.lstMediaTracks = []
        self.__log = None
        self.log = log
        self.totalTracksByType = {"Video": 0, "Audio": 0, "Text": 0}
        self.totalTracksByTypeLanguage = {
            "Video": {"all": 0},
            "Audio": {"all": 0},
            "Text": {"all": 0},
        }
        self.attachments = ""
        self._initHelper()

    def _initHelper(self):

        try:
            fileMediaInfo = MediaInfo.parse(self.fileName)
            self.mediaInfo = fileMediaInfo
        except OSError as e:
            raise OSError("MediaInfo not found.") from e

        for track in fileMediaInfo.tracks:
            if track.track_type == "General":
                self.codec = track.codec
                self.format = track.format
                if track.title is not None:
                    self.title = track.title
                    try:
                        self.title = base64.b64decode(track.title).decode("UTF-8")
                    except:  # pylint: disable=bare-except
                        pass
                    self.title = self.title.strip()
                self.totalTracksByType["Video"] = (
                    0
                    if track.count_of_video_streams is None
                    else int(track.count_of_video_streams)
                )
                self.totalTracksByType["Audio"] = (
                    0
                    if track.count_of_audio_streams is None
                    else int(track.count_of_audio_streams)
                )
                self.totalTracksByType["Text"] = (
                    0
                    if track.count_of_text_streams is None
                    else int(track.count_of_text_streams)
                )
                self.attachments = (
                    "" if track.attachments is None else track.attachments.split(" / ")
                )
                self.totalTracksByTypeLanguage["Video"]["all"] = (
                    0
                    if track.count_of_video_streams is None
                    else int(track.count_of_video_streams)
                )
                self.totalTracksByTypeLanguage["Audio"]["all"] = (
                    0
                    if track.count_of_audio_streams is None
                    else int(track.count_of_audio_streams)
                )
                self.totalTracksByTypeLanguage["Text"]["all"] = (
                    0
                    if track.count_of_text_streams is None
                    else int(track.count_of_text_streams)
                )
            if track.track_type == "Menu":
                self.menu = track
            if track.track_type in ("Video", "Audio", "Text"):
                lang = iso639(track.language, codeOnly=True)
                if lang in self.totalTracksByTypeLanguage[track.track_type].keys():
                    langIndex = (
                        self.totalTracksByTypeLanguage[track.track_type][lang] + 1
                    )
                else:
                    langIndex = 0
                self.totalTracksByTypeLanguage[track.track_type][lang] = langIndex
                self.lstMediaTracks.append(
                    MediaTrackInfo(
                        track.streamorder,
                        track.track_type,
                        lang,
                        track.default,
                        track.forced,
                        track.title,
                        track.codec,
                        track.format,
                        track.count_of_stream_of_this_kind,
                        track.stream_identifier,
                        typeLanguageOrder=langIndex,
                    )
                )

        if self.lstMediaTracks:
            for trk in self.lstMediaTracks:
                if trk.track_type in ("Video", "Audio", "Text"):
                    trk.tracksLanguageOfThisKind = (
                        self.totalTracksByTypeLanguage[trk.trackType][trk.language] + 1
                    )

    def __contains__(self, item):
        return item in self.lstMediaTracks

    def __eq__(self, objOther):

        bReturn = True

        if self.log:
            MODULELOG.debug(
                "MFI0001: Structure equality test between [%s] and [%s]",
                self.fileName,
                objOther.fileName,
            )
            MODULELOG.debug("MFI0002: FORMAT: %s", self.format)

        if self.codec != objOther.codec:
            if self.log:
                MODULELOG.debug(
                    "MFI0003: Codec mismatched %s - %s", self.codec, objOther.codec
                )
            bReturn = False
        elif len(self) != len(objOther):
            if self.log:
                MODULELOG.debug(
                    "MFI0004: Number of tracks mismatched %s - %s",
                    len(self),
                    len(objOther),
                )
            bReturn = False
        elif len(self) == len(objOther):
            for a, b in zip(self.lstMediaTracks, objOther.lstMediaTracks):
                if a.streamorder != b.streamorder:
                    if self.log:
                        MODULELOG.debug(
                            "MFI0005:  Stream order mismatched %s - %s",
                            a.streamorder,
                            b.streamorder,
                        )
                    bReturn = False
                elif a.track_type != b.track_type:
                    if self.log:
                        MODULELOG.debug(
                            "MFI006: Stream type mismatched %s - %s",
                            a.track_type,
                            b.track_type,
                        )
                    bReturn = False
                elif (a.language != b.language) and (a.track_type != "Video"):
                    if self.log:
                        MODULELOG.debug(
                            "MFI0007: Stream language mismatched %s - %s",
                            a.language,
                            b.language,
                        )
                    if self.format == "AVI":
                        # Ignore language for AVI container
                        if self.log:
                            MODULELOG.debug(
                                "MFI0008: AVI container ignore language mismatched %s - %s",
                                a.track_type,
                                b.track_type,
                            )
                    else:
                        bReturn = False
                elif (a.codec != b.codec) and (
                    a.track_type != "Audio"
                ):  # Audio has no codec
                    if self.log:
                        MODULELOG.debug(
                            "MFI0009: Codec mismatched %s - %s", a.codec, b.codec
                        )
                    if self.format == "AVI":
                        # Ignore for AVI container
                        if self.log:
                            MODULELOG.debug(
                                "MFI0010: AVI container ignore codec mismatched %s - %s",
                                a.codec,
                                b.codec,
                            )
                    else:
                        bReturn = False
                elif a.format != b.format:
                    if self.log:
                        MODULELOG.debug(
                            "MFI0011: Stream format mismatched %s - %s",
                            a.format,
                            b.format,
                        )
                    bReturn = False

        if self.log:
            if bReturn:
                MODULELOG.debug("MFI0012: Structure found ok.",)
            else:
                MODULELOG.debug("MFI0013: Structure not ok.",)

        return bReturn

    def __getitem__(self, value):
        return self.lstMediaTracks[value]

    def __len__(self):
        return len(self.lstMediaTracks) if self.lstMediaTracks else 0

    def __str__(self):

        tmpStr = "File Name: {}\nFile Format: -{}-\n\n".format(
            self.fileName, self.format
        )
        tmpNum = 0

        for track in self.lstMediaTracks:
            tmpStr += (
                f"Track: {tmpNum:>2} "
                f"Order: {track.streamorder:>2} - {track.track_type:>5} "
                f"- Codec: {track.codec} "
                f"- Language: {str(track.language):>4} "
                f"- Format: {track.format}\n"
            )
            tmpNum += 1

        return tmpStr

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

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return MediaFileInfo.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value


class MediaTrackInfo:
    r"""
    Convenience class used by MediaFileInfo_
    contains the media track properties

    Args:
        streamorder (:obj:`str`, optional): order of track
        track_type (:obj:`str`, optional): type of track
        language (:obj:`str`, optional): language of track
        default (:obj:`str`, optional): is this a default track
        forced (:obj:`str`, optional): is this a forced track
        title (:obj:`str`, optional): title of track
        codec (:obj:`str`, optional): codec used on track
        format\_ (:obj:`str`, optional): format of track

    Attributes:
        streamorder (str): Stream order
        track_type (str): Track Type
        language (str): Language of track
        default (str): Is a default track
            'Yes' it is 'No' otherwise
        forced (str): Is a forced track
            'Yes' it is 'No' otherwise
        title (str): Track tittle
        codec (str): Codec used
        format (str): Track format
    """

    def __init__(
        self,
        streamorder=None,
        track_type=None,
        language=None,
        default=None,
        forced=None,
        title=None,
        codec=None,
        format_=None,
        tracksOfThisKind=None,
        typeOrder=None,
        tracksLanguageOfThisKind=None,
        typeLanguageOrder=None,
        log=False,
    ):

        self.streamorder = streamorder
        self.track_type = track_type  # pylint: disable=C0103
        self.language = language
        self.default = default
        self.forced = forced
        self.title = title
        self.codec = codec
        self.format = format_
        self.log = log
        # Extending
        self.totalTracksOfThisKind = tracksOfThisKind
        self.typeOrder = (-1) if typeOrder is None else int(typeOrder)
        self.typeLanguageOrder = (
            (-1) if typeLanguageOrder is None else int(typeLanguageOrder)
        )
        self.tracksLanguageOfThisKind = (
            (-1) if tracksLanguageOfThisKind is None else int(tracksLanguageOfThisKind)
        )
        # Extending compatibility
        self.trackType = track_type
        self.streamOrder = (-1) if streamorder is None else int(streamorder)

    def __eq__(self, otherTrack):

        bReturn = True

        if self.streamorder != otherTrack.streamorder:
            if self.log:
                MODULELOG.debug(
                    "MFI0014:  Stream order mismatched %s - %s",
                    self.streamorder,
                    otherTrack.streamorder,
                )
            bReturn = False
        elif self.track_type != otherTrack.track_type:
            if self.log:
                MODULELOG.debug(
                    "MFI015: Stream type mismatched %s - %s",
                    self.track_type,
                    otherTrack.track_type,
                )
            bReturn = False
        elif (self.language != otherTrack.language) and (self.track_type != "Video"):
            if self.log:
                MODULELOG.debug(
                    "MFI0016: Stream language mismatched %s - %s",
                    self.language,
                    otherTrack.language,
                )
            if self.format == "AVI":
                # Ignore language for AVI container
                if self.log:
                    MODULELOG.debug(
                        "MFI0017: AVI container ignore language mismatched %s - %s",
                        self.track_type,
                        otherTrack.track_type,
                    )
            else:
                bReturn = False
        elif (self.codec != otherTrack.codec) and (
            self.track_type != "Audio"
        ):  # Audio has no codec
            if self.log:
                MODULELOG.debug(
                    "MFI0018: Codec mismatched %s - %s", self.codec, otherTrack.codec
                )
            if self.format == "AVI":
                # Ignore for AVI container
                if self.log:
                    MODULELOG.debug(
                        "MFI0019: AVI container ignore codec mismatched %s - %s",
                        self.codec,
                        otherTrack.codec,
                    )
            else:
                bReturn = False
        elif self.format != otherTrack.format:
            if self.log:
                MODULELOG.debug(
                    "MFI0020: Stream format mismatched %s - %s",
                    self.format,
                    otherTrack.format,
                )
            bReturn = False

        if self.typeOrder != otherTrack.typeOrder:
            if self.log:
                MODULELOG.debug(
                    "MFI0021:  Type order mismatched %s - %s",
                    self.streamorder,
                    otherTrack.streamorder,
                )
            bReturn = False

        return bReturn

    def __str__(self):
        return (
            f"Order: {self.streamorder:>2} "
            f"Type total: {str(self.totalTracksOfThisKind):>2} "
            f"Type order: {self.typeOrder:>2} "
            f"Type: {self.track_type:>5} "
            f"Language: {str(self.language):>4} "
            f"Total: {self.tracksLanguageOfThisKind:>2} "
            f"Order: {self.typeLanguageOrder:>2} "
            f"Default: {self.default:>3} "
            f"Forced: {self.forced:>3} "
            f"Format: {str(self.format):>7} "
            f"Title: {str(self.title)}"
        )

    def __repr__(self):
        return (
            f"Stream Order: {self.streamorder} "
            f"Track Type Order: {self.typeOrder} "
            f"Track Type: {self.track_type} "
            f"Language: {self.language} "
            f"Default Track: {self.default} "
            f"Forced Track: {self.forced} "
            f"Codec: {str(self.codec)} "
            f"Format: {str(self.format)} "
            f"Tracks of this kind: {str(self.totalTracksOfThisKind)} "
            f"Track Title: {str(self.title)}"
        )
