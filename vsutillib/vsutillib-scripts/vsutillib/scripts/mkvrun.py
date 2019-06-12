#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run command line generated by mkvmerge-gui

use the linux bash one encased in double quotes
"""

import argparse

from vsutillib.media import MediaFileInfo
from vsutillib.mkv import MKVCommand, VerifyStructure
from vsutillib.process import RunCommand

VERSION = "1.0"


def displayMKVRun(line):
    """
    Convenience function used by mkvrun
    used to display lines of the mkvmerge
    execution

    Args:
        line (str): line to display
    """

    if line.find("Progress:") >= 0:
        print("\r" + line[:-1], end='')
    elif line.find('The cue') == 0:
        print("\n" + line, end='')
    else:
        print(line, end='')


def mkvVerifyStructure(lstBaseFiles, lstFiles, msgs):
    """
    Convenience function used by mkvrun
    verify the file structure against
    the base files

    Args:
        lstBaseFiles (list): list files parsed from command

        lstFiles (list): list of files read from directories
    """

    msg = "Error: In structure \n\nSource:\n{}\nBase Source:\n{}\n"

    for strSource, strFile in zip(lstBaseFiles, lstFiles):

        try:
            objSource = MediaFileInfo(strSource)
            objFile = MediaFileInfo(strFile)

        except OSError:

            msg = msg.format(str(objFile), str(objSource))
            msgs.append(msg)
            return False

        if objSource != objFile:

            msg = msg.format(str(objFile), str(objSource))
            msgs.append(msg)
            return False

    return True


def mkvrun():
    """
    Run mkvmerge-gui generated cli command and
    applied to all files in directory. The command
    select has to be for bash shell and encase in
    double quotes

    ::

        usage: mkvrun.py [-h] [--version] command

        mkvmerge-gui generated command line batch run utility

        positional arguments:
        command     mkvmerge-gui "command" line - used Linux/Unix shell enclose it
                    in double quotes

        optional arguments:
        -h, --help  show this help message and exit
        --version   show program's version number and exit

    Args:
        command (str): bash command line as generated
            by mkvmerge-gui
    """

    parser = argparse.ArgumentParser(
        description='mkvmerge-gui generated command line batch run utility')

    parser.add_argument(
        'command',
        help=
        'mkvmerge-gui "command" line - used Linux/Unix shell enclose it in double quotes'
    )
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + VERSION)

    args = parser.parse_args()

    if args.command:
        print('command read: [{}]'.format(args.command))

    f = open("log.txt", mode='w', encoding='utf-8')

    mkv = MKVCommand()
    mkv.command = args.command

    verify = VerifyStructure()

    cli = RunCommand(processLine=displayMKVRun,
                     commandShlex=True,
                     universalNewLines=True)

    if mkv:

        for cmd, baseFiles, sourceFiles, destinationFiles in mkv:

            verify.verifyStructure(baseFiles, sourceFiles)

            if verify:

                msg = '\nCommand: {}\nBase Files: {}\nSource Files: {}\nDestination Files: {}\n\n'.format(  # pylint: disable=line-too-long
                    cmd, baseFiles, sourceFiles, destinationFiles)
                print(msg)
                f.write(msg)

                cli.command = cmd
                cli.run()

                for l in cli.output:
                    f.write(str(l))

            else:
                msg = '\nDestination Files: {}\n'.format(destinationFiles)
                f.write(msg)
                for m in verify.analysis:
                    print(m)
                    f.write(m)

    else:

        print("Bummer...{}".format(mkv.error))


if __name__ == "__main__":
    mkvrun()
