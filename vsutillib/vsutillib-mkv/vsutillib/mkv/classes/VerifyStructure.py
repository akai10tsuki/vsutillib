"""
Verify structure of media files for inconsistencies
against the source base files use for the templates
"""
# VFS0001

import logging

from vsutillib.media import MediaFileInfo

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class VerifyStructure:
    """
    Convenience class use by MKVCommand_ to verify structure
    of media files against base files.

    The class evaluates to True if structure if logically equal.
    That is tracks same order same type.

    .. code:: Python

        verify = VerifyStructure(lstBaseFile, lstSourceFiles)

        if verify:
            # Ok to proceed
            ...
        else:
            raise ValueError('')

    Args:
        lstBaseFile (:obj:`list`, optional): list with the base files
            as found in command
        lstSourceFiles (:obj:`list`, optional): list of files to generate new command
    """

    __log = False

    def __init__(
        self, lstBaseFiles=None, lstSourceFiles=None, destinationFile=None, log=None
    ):

        self.__analysis = None
        self.__log = None
        self.__status = None
        self.__matchedTracks = []
        self.__unmatchedTracks = []

        self.log = log

        if (lstBaseFiles is not None) and (lstSourceFiles is not None):
            self.verifyStructure(lstBaseFiles, lstSourceFiles, destinationFile)

    def __bool__(self):
        return self.__status

    def __str__(self):

        return "".join(self.__analysis)

    @classmethod
    def classLog(cls, setLogging=None):
        """
        get/set logging at class level
        every class instance will log
        unless overwritten

        Args:
            setLogging (`bool`):

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

    @property
    def log(self):
        """
        class property can be used to override the class global
        logging setting if set to None class log will be followed

        Returns:
            bool:

            True if logging is enable False otherwise
        """
        if self.__log is not None:
            return self.__log

        return VerifyStructure.classLog()

    @log.setter
    def log(self, value):
        """set instance log variable"""
        if isinstance(value, bool) or value is None:
            self.__log = value

    @property
    def isOk(self):
        """
        status check of analysis

        Returns:
            bool:

            Returns True if successful False otherwise.
        """
        return self.__status

    @property
    def analysis(self):
        """
        results of analysis of the comparison

        Returns:
            list:

            list with comments of anything found
        """
        return self.__analysis

    @property
    def matched(self):
        return self.__matchedTracks

    @property
    def unmatched(self):
        return self.__unmatchedTracks

    def verifyStructure(self, lstBaseFiles, lstSourceFiles, destinationFile=None):
        """
        Verify if structure of files if logically equal.


        Args:
            lstBaseFile (list): list with the base files
                as found in command
            lstSourceFiles (list): list of files to generate new command
        """

        # msg = "Error: In structure \n\nSource:\n{}\nBase Source:\n{}\n"
        self.__analysis = []
        self.__status = True
        self.__matchedTracks = []
        self.__unmatchedTracks = []

        for sourceIndex, (baseFile, sourceFile) in enumerate(
            zip(lstBaseFiles, lstSourceFiles)
        ):

            try:

                objSource = MediaFileInfo(baseFile, log=self.log)
                objFile = MediaFileInfo(sourceFile, log=self.log)

                if objSource != objFile:

                    if destinationFile is not None:
                        msg = "Error: In structure\nDestination File: {}\n\n"
                        msg = msg.format(destinationFile)
                    else:
                        msg = "Error: In structure\n\n"
                    msg = msg + "Source:\n{}\n\nBase Source:\n{}\n"
                    msg = msg.format(str(objFile), str(objSource))
                    self.__analysis.append(msg)
                    self.__status = False
                    self._detailAnalysis(objSource, objFile, sourceIndex)

                    if self.log:

                        msg = "Error: In structure Source: {} Base Source: {}"
                        msg = msg.format(objFile.fileName, objSource.fileName)
                        MODULELOG.error("VFS0002: Error: %s", msg)

                        for i, line in enumerate(self.__analysis):
                            if i > 0:
                                MODULELOG.error("VFS0003: Error: %s", line.strip())

                        msg = "Structure not ok. Source: {} Base Source: {}"
                        msg = msg.format(objFile.fileName, objSource.fileName)
                        MODULELOG.debug("VFS0004: %s", msg)

                else:
                    for track in range(len(objSource.lstMediaTracks)):
                        self.__matchedTracks.append(str(sourceIndex) + ":" + str(track))

                    if self.log:
                        msg = "Structure seems ok. Source: {} Base Source: {}"
                        msg = msg.format(objFile.fileName, objSource.fileName)
                        MODULELOG.debug("VFS0005: %s", msg)

            except OSError as error:

                msg = "Error: \n{}\n"
                msg = msg.format(error.strerror)
                self.__analysis.append(msg)
                self.__status = False

                if self.log:
                    msg = "Error: {}"
                    msg = msg.format(error.strerror)
                    MODULELOG.error("VFS0001: %s", msg)

    def _detailAnalysis(self, mediaFile1, mediaFile2, sourceIndex):

        name1 = mediaFile1.fileName.name
        name2 = mediaFile2.fileName.name

        if mediaFile1.codec != mediaFile2.codec:
            msg = "Codec mismatched {}: {} - {}: {}\n".format(
                name1, mediaFile1.codec, name2, mediaFile2.codec
            )
            self.__analysis.append(msg)
        elif len(mediaFile1) != len(mediaFile2):
            msg = "Number of tracks mismatched {}: {} - {}: {}\n".format(
                name1, len(mediaFile1), name2, len(mediaFile2)
            )
            self.__analysis.append(msg)
        elif len(mediaFile1) == len(mediaFile2):
            namePrinted = False
            for index, (a, b) in enumerate(
                zip(mediaFile2.lstMediaTracks, mediaFile1.lstMediaTracks)
            ):
                # if not namePrinted:
                #    msg = "Source order mismatched \n{}: {} - \n{}: {}\n".format(
                #        name1, a.streamorder, name2, b.streamorder
                #    )
                #    self.__analysis.append(msg)
                #    matched = False

                matched = True
                if a.streamorder != b.streamorder:
                    # msg = "Stream order mismatched Source: {} - Base: {}\n".format(
                    msg = (
                        "Track "
                        + str(index)
                        + ": Stream order mismatched \nSource: {}\n  Base: {}\n".format(
                            a.streamorder, b.streamorder
                        )
                    )
                    self.__analysis.append(msg)
                    matched = False
                elif a.track_type != b.track_type:
                    msg = (
                        "Track "
                        + str(index)
                        + ": Stream type mismatched \nSource: {}\n  Base: {}\n".format(
                            a.track_type, b.track_type
                        )
                    )
                    self.__analysis.append(msg)
                    matched = False
                elif a.language != b.language:
                    msg = (
                        "Track "
                        + str(index)
                        + ": Stream language mismatched \nSource: {}:{}\n  Base: {}:{}\n".format(
                            a.streamorder, a.language, b.streamorder, b.language,
                        )
                    )
                    self.__analysis.append(msg)
                    matched = False
                elif (a.codec != b.codec) and (a.track_type != "Audio"):
                    msg = (
                        "Track "
                        + str(index)
                        + ": Codec mismatched \nSource: {}\n  Base: {}\n".format(
                            a.codec, b.codec
                        )
                    )
                    self.__analysis.append(msg)
                    matched = False
                elif a.format != b.format:
                    # msg = "Stream format mismatched {}: {} - {}: {}\n".format(
                    msg = (
                        "Track "
                        + str(index)
                        + ": Stream format mismatched \nSource: {}\n  Base: {}\n".format(
                            a.format, b.format
                        )
                    )
                    self.__analysis.append(msg)
                    matched = False
                if matched:
                    self.__matchedTracks.append(str(sourceIndex) + ":" + str(index))
                else:
                    self.__unmatchedTracks.append(str(sourceIndex) + ":" + str(index))
