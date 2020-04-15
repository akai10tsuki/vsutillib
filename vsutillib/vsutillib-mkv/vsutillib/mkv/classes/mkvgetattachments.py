"""
 Get file attachments

"""

import shlex


class MKVGetAttachments:
    """
     Get attachment files

     Case 1: More than directories with attachments
        Return MKVCommandParser.attachmentsString for every Source

     Case 2: One directory with attachments
        - files in directory differ from total attachments on CL
          return MKVCommandParser.attachmentsString for every Source
        - files in directory equals total attachments on CL
          read directories on parent directory
          * total direcoties equals total source read directories
            and return files read to corresponding source. Directories
            can be empty meaning corresponding source has no attachments.
            This way each source can have different attachment files
          * total directories differ from total source files
            return MKVCommandParser.attachmentsString for every Source
    """

    def __init__(self, parsedCommand=None):

        self.__parsedCommand = None
        self.__totalSource = None
        self.__attachments = []

        # for iterator
        self.__index = 0
        self.parsedCommand = parsedCommand

    def __contains__(self, item):
        return item in self.__attachments

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__attachments)

    def __getitem__(self, index):
        return self.__attachments[index]

    def __next__(self):
        if self.__index >= len(self.__attachments):
            self.__index = 0
            raise StopIteration
        else:
            self.__index += 1
            return self.__getitem__(self.__index - 1)

    @property
    def attachments(self):
        return self.__attachments

    @property
    def parsedCommand(self):
        return self.__parsedCommand

    @parsedCommand.setter
    def parsedCommand(self, value):
        if value:
            self._reset()
            self.__parsedCommand = value
            self._totalSourceFiles()
            self._readDirs()

    def _reset(self):

        self.__parsedCommand = None
        self.__totalSource = None
        self.__attachments = []

    def _totalSourceFiles(self):

        self.__totalSource = len(self.parsedCommand)

    def _readDirs(self):
        if self.parsedCommand.attachments:
            if len(self.parsedCommand.attachmentsDirs) == 1:
                # Check parent for directories
                d = self.parsedCommand.attachmentsDirs[0]
                pd = self.parsedCommand.attachmentsDirs[0].parent
                did = [x for x in pd.glob("*") if x.is_dir()]
                fid = [x for x in d.glob("*") if x.is_file()]

                if len(self.parsedCommand.attachments) != len(fid):
                    self.__attachments.extend(
                        [self.parsedCommand.attachmentsString] * self.__totalSource
                    )

                elif self.__totalSource == len(did):
                    for d in did:
                        fid = [x for x in d.glob("*") if x.is_file()]
                        self.__attachments.append(attachmentsToStr(fid))
                else:
                    self.__attachments.extend(
                        [self.parsedCommand.attachmentsString] * self.__totalSource
                    )


def mimeType(fileName):
    """
    mimeType return mime type of known files by suffix

    Args:
        fileName (filepath.Path): file Path object

    Returns:
        str: known mime type for file defaults to application/octet-stream
    """

    if fileName.suffix.upper() in [".TTF", ".TTC"]:
        return "application/x-truetype-font"
    elif fileName.suffix.upper() in [".OTF"]:
        return "application/vnd.ms-opentype"

    return "application/octet-stream"


def _attachmentToStr(attachFile):

    strTmp = "--attachment-name " + shlex.quote(attachFile.name)
    strTmp += " --attachment-mime-type " + mimeType(attachFile)
    strTmp += " --attach-file " + shlex.quote(str(attachFile))

    return strTmp


def attachmentsToStr(attachFiles):
    """
    attachmentsToStr convert list of attachment files to mkvmerge option

    Args:
        attachFiles (list): list of attachment files

    Returns:
        str: mkvmerge options string
    """

    strTmp = ""
    bFirst = True
    for f in attachFiles:
        if bFirst:
            strTmp = _attachmentToStr(f)
            bFirst = False
        else:
            strTmp += " " + _attachmentToStr(f)

    return strTmp
