"""
Verify structure of media files for inconsistencies
against the source base files use for the templates
"""

import logging

from vsutillib.media import MediaFileInfo

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class VerifyStructure():
    """
    Convenience class use by MKVCommand_ to verify structure
    of media files against base files.

    The class evaluates to True if structure if logically equal.
    That is tracks same order same type.

    .. code:: Python

        verify = VerifyStructure(lstBaseFile, lstFiles)

        if verify:
            # Ok to proceed
            ...
        else:
            raise ValueError('')

    Args:
        lstBaseFile (:obj:`list`, optional): list with the base files
            as found in command
        lstFiles (:obj:`list`, optional): list of files to generate new command
    """

    __log = False

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

    def __init__(self, lstBaseFiles=None, lstFiles=None):

        MediaFileInfo.log = self.log

        self.__analysis = None
        self.__status = None

        if (lstBaseFiles is not None) and (lstFiles is not None):
            self.verifyStructure(lstBaseFiles, lstFiles)

    def __bool__(self):
        return self.__status

    def __str__(self):
        msgs = ""
        for m in self.__analysis:
            msgs += m
        return msgs

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

    def verifyStructure(self, lstBaseFiles, lstFiles):
        """
        Verify if structure of files if logically equal.


        Args:
            lstBaseFile (list): list with the base files
                as found in command
            lstFiles (list): list of files to generate new command
        """

        msg = "Error: In structure \n\nSource:\n{}\nBase Source:\n{}\n"
        self.__analysis = []
        self.__status = True

        for strSource, strFile in zip(lstBaseFiles, lstFiles):

            try:

                objSource = MediaFileInfo(strSource)
                objFile = MediaFileInfo(strFile)

            except OSError as error:

                msg = "Error: \n{}\n"
                msg = msg.format(error.strerror)
                self.__analysis.append(msg)
                self.__status = False

            if objSource != objFile:
                msg = "Error: In structure \n\nSource:\n{}\nBase Source:\n{}\n"
                msg = msg.format(str(objFile), str(objSource))
                self.__analysis.append(msg)
                self.__status = False
                _detailAnalysis(self, objFile, objSource)

def _detailAnalysis(self, mediaFile1, mediaFile2):

    if mediaFile1.codec != mediaFile2.codec:
        msg = "Codec mismatched {} - {}".format(mediaFile1.codec, mediaFile2.codec)
        self.__analysis.append(msg)
    elif len(mediaFile1) != len(mediaFile2):
        msg = "Number of tracks mismatched {} - {}".format(len(mediaFile1), len(mediaFile2))
        self.__analysis.append(msg)
    elif len(mediaFile1) == len(mediaFile2):
        for a, b in zip(mediaFile1.lstMediaTracks, mediaFile2.lstMediaTracks):
            if a.streamorder != b.streamorder:
                msg = "Stream order mismatched {} - {}".format(a.streamorder, b.streamorder)
                self.__analysis.append(msg)
            elif a.track_type != b.track_type:
                msg = "Stream type mismatched {} - {}".format(a.track_type, b.track_type)
                self.__analysis.append(msg)
            elif a.language != b.language:
                msg = "Stream language mismatched {} - {}".format(a.language, b.language)
                self.__analysis.append(msg)
            elif (a.codec != b.codec) and (a.track_type != "Audio"):
                msg = "Codec mismatched {} - {}".format(a.codec, b.codec)
                self.__analysis.append(msg)
            elif a.format != b.format:
                msg = "Stream format mismatched {} - {}".format(a.format, b.format)
                self.__analysis.append(msg)
