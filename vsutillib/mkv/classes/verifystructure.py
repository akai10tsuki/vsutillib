"""
Verify structure of media files for inconsistencies
against the source base files use for the templates
"""

import logging


from ...media import MediaFileInfo


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class VerifyStructure():
    """class to verify structure of media files against base files"""

    __log = False

    @classmethod
    def classLog(cls, setLogging=None):
        """
        get/set logging at class level
        every class instance will log
        unless overwritten
        """

        if setLogging is None:
            return cls.__log
        elif isinstance(setLogging, bool):
            cls.__log = setLogging

    def __init__(self, lstBaseFiles=None, lstFiles=None):

        MediaFileInfo.log = self.log

        self.__messages = None
        self.__status = None

        if (lstBaseFiles is not None) and (lstFiles is not None):
            self.verifyStructure(lstBaseFiles, lstFiles)

    def __bool__(self):
        return self.__status

    def __str__(self):
        msgs = ""
        for m in self.__messages:
            msgs += m
        return msgs

    @property
    def log(self):
        """
        return log enable/disable
        instance variable self.__log
        overrides global variable
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
        """current status of check"""
        return self.__status

    @property
    def messages(self):
        """status message"""
        return self.__messages

    def verifyStructure(self, lstBaseFiles, lstFiles):
        """verify the file structure against the base files"""

        msg = "Error: In structure \n\nSource:\n{}\nBase Source:\n{}\n"
        self.__messages = []
        self.__status = True

        for strSource, strFile in zip(lstBaseFiles, lstFiles):

            try:

                objSource = MediaFileInfo(strSource)
                objFile = MediaFileInfo(strFile)

            except OSError as error:

                msg = "Error: \n{}\n"
                msg = msg.format(error.strerror)
                self.__messages.append(msg)
                self.__status = False

            if objSource != objFile:
                msg = "Error: In structure \n\nSource:\n{}\nBase Source:\n{}\n"
                msg = msg.format(str(objFile), str(objSource))
                self.__messages.append(msg)
                self.__status = False
