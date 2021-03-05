"""
    commandTemplate
"""

import logging
import platform
import re
import shlex

from .classes import MKVAttachments
from .classes.MKVParseKey import MKVParseKey
from .mkvutils import stripEncaseQuotes

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())

def generateCommandTemplate(bashCommand, attachments=None, setTitle=False):
    """
    commandTemplate creates templage of mkvtoolnix-gui command

    Args:
        bashCommand (str): command in linux/unix bash format
        setTitle (bool, optional): If True mark the title otherwise remove from
        template. Defaults to False.

    Returns:
        tuple: tuple with:

            - command template
            - match string for mkvmerge executable
            - list with match strings for source files
            - match string for templates
    """

    cmdTemplate = bashCommand

    dMatch = {}
    dMatch[MKVParseKey.mkvmergeMatch] = None
    dMatch[MKVParseKey.outputMatch] = None
    dMatch[MKVParseKey.baseFilesMatch] = []
    dMatch[MKVParseKey.chaptersMatch] = None

    reExecutableEx = re.compile(r"^(.*?)\s--")
    reOutputFileEx = re.compile(r".*?--output\s(.*?)\s--")
    reFilesEx = re.compile(r"'\(' (.*?) '\)'")
    reChaptersFileEx = re.compile(r"--chapter-language (.*?) --chapters (.*?) (?=--)")
    reTracksOrderEx = re.compile(r"--track-order\s(.*)")
    reTitleEx = re.compile(r"--title\s(.*?)(?=$|\s--)")

    if matchExecutable := reExecutableEx.match(cmdTemplate):
        dMatch[MKVParseKey.mkvmergeMatch] = matchExecutable.group(1)
        f = stripEncaseQuotes(dMatch[MKVParseKey.mkvmergeMatch])
        e = shlex.quote(f)

        ##
        # BUG 1
        # Reported by zFerry98
        #
        # When running in Windows there is no space in the mkvmerge executable path
        # \ is use as escape
        # Command: ['C:binmkvtoolnixmkvmerge.exe', ...
        #
        # Solution:
        #   Force quotes for mkvmerge executable
        #
        #   Command: ['C:\\bin\\mkvtoolnix\\mkvmerge.exe'
        ##
        if platform.system() == "Windows":
            if e[0:1] != "'":
                e = "'" + f + "'"
        ##

        cmdTemplate = bashCommand
        cmdTemplate = cmdTemplate.replace(dMatch[MKVParseKey.mkvmergeMatch], e, 1)

        if matchOutputFile := reOutputFileEx.match(bashCommand):
            dMatch[MKVParseKey.outputMatch] = matchOutputFile.group(1)
            cmdTemplate = cmdTemplate.replace(
                dMatch[MKVParseKey.outputMatch], MKVParseKey.outputFile, 1
            )

        if matchFiles := reFilesEx.finditer(bashCommand):
            for index, match in enumerate(matchFiles):
                key = "<SOURCE{}>".format(str(index))
                cmdTemplate = cmdTemplate.replace(match.group(0), key, 1)
                if index == 0:
                    regEx = r"<OUTPUTFILE>\s(.*?)\s<SOURCE0>"
                else:
                    regEx = f"<SOURCE{str(index - 1)}>" + r"\s(.*?)\s" + key
                    regEx.format(str(index - 1), str(index))
                options = re.search(regEx, cmdTemplate)
                dMatch[MKVParseKey.baseFilesMatch].append(
                    f"{options.group(1)} {match.group(0)}"
                )  # source file with options

        if attachments is None:
            oAttachments = MKVAttachments()
            MODULELOG.debug("GCT0001: Init attacment class.")
        else:
            oAttachments = attachments
            MODULELOG.debug("GCT0002: Attacment already initialized.")

        oAttachments.command = bashCommand

        if oAttachments.cmdLineAttachments:
            cmdTemplate = cmdTemplate.replace(
                oAttachments.attachmentsMatchString,
                MKVParseKey.attachmentFiles,
                1,
            )

        ##
        # Bug #3
        #
        # It was not preserving the episode title
        #
        # If there is no title read --title '' will be used.
        # If setTitle is False the --title option will be removed from the
        # template
        # working with \ ' " backslash, single and double quotes in same title
        ##
        if match := reTitleEx.search(bashCommand):
            if setTitle:
                cmdTemplate = cmdTemplate.replace(
                    match.group(1),
                    MKVParseKey.title,
                    1,
                )
            else:
                cmdTemplate = cmdTemplate.replace(" " + match.group(0), "", 1)

        if match := reChaptersFileEx.search(bashCommand):
            dMatch[MKVParseKey.chaptersMatch] = match.group(2)
            cmdTemplate = cmdTemplate.replace(
                dMatch[MKVParseKey.chaptersMatch], MKVParseKey.chaptersFile, 1
            )

        if match := reTracksOrderEx.search(bashCommand):
            cmdTemplate = cmdTemplate.replace(match.group(1), MKVParseKey.trackOrder, 1)

    return (cmdTemplate, dMatch)
