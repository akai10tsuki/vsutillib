"""
vsutillib version and configuration constants

config can be use by other applications

import vsutillib.config as config

config.init(configFile='appName-config.xml',
            filesRoot='.appName',
            logFile='file.log',
            name='appName',
            version='1.0')

and

config.close()

config.data is files.ConfigurationSettings class instance

before application exit
"""

import logging
import sys
from pathlib import Path

from vsutillib.files import ConfigurationSettings
from vsutillib.log import LogRotateFileHandler


__VERSION = (3, 0, "0b1", "dev0")


FILES_VERSION = "1.7.0"
LOG_VERSION = "1.7.0"
SYSTEM_VERSION = "1.7.0"
MEDIA_VERSION = "1.7.0"
MISC_VERSION = "1.7.0"
MKV_VERSION = "1.7.0"
NETWORK_VERSION = "1.7.0"
PROCESS_VERSION = "1.7.0"
PYQT_VERSION = "1.7.0"
PYQT6_VERSION = "1.7.0"
SCRIPTS_VERSION = "1.7.0"
SQL_VERSION = "1.7.0"
VSXML_VERSION = "1.7.0"

LXML_VERSION = ">=4.5"
NATSORT_VERSION = ">=7.0.1"
PYMEDIAINFO_VERSION = ">=4.2.1"
PYSIDE2_VERSION = ">=5.14.1"
PYSIDE6_VERSION = ">=6.2.0"
PYTHON_VERSION = ">=3.10.1, <3.13"
PYTHONVERSIONS = ">=3.10.1, <3.13"

APPNAME = "vsutillib"
VERSION = ".".join(map(str, __VERSION))
AUTHOR = "Efrain Vergara"
EMAIL = "akai10tsuki@gmail.com"
PACKAGES = [APPNAME]

COPYRIGHT = "2018-2024, Efrain Vergara"
LICENSE = "MIT"
DESCRIPTION = "Library module with miscellaneous convenience functions and classes"
NAME = "vsutillib"
KEYWORDS = "mkv multimedia video audio configuration"
REQUIRED = [
    "lxml" + LXML_VERSION,
    "pymediainfo" + PYMEDIAINFO_VERSION,
    "PySide6" + PYSIDE6_VERSION,
    "natsort" + NATSORT_VERSION,
]
URL = "https://github.com/akai10tsuki/vsutillib"
PYPI = "https://pypi.org/project/vsutillib/"
PROJECTURLS = {
    "Source": "https://pypi.org/project/vsutillib/#files",
}

CONFIGFILE = "config.xml"
FILESROOT = "." + APPNAME
LOGFILE = APPNAME + ".log"
IMAGEFILESPATH = ""

__version__ = VERSION

data = ConfigurationSettings()  # pylint: disable=invalid-name


def init(filesRoot=None, configFile=None, logFile=None, name=None, version=None):
    """
    configures the system to save application configuration to xml file

    Args:
        filesRoot (str, optional): root folder on ~ for files. Defaults to [.vsutillib].
        configFile (str, optional): name of configuration file. Defaults to [config.xml].
        logFile (str, optional): name of logging file. Defaults to [vsutillib.log].
        name (str, optional): name of application. Defaults to [vsutillib].
        version (str, optional): appplication version . Defaults to [vsutillib version].
    """

    if filesRoot is None:
        filesPath = Path(Path.home(), FILESROOT)
    else:
        filesPath = Path(Path.home(), filesRoot)

    filesPath.mkdir(parents=True, exist_ok=True)

    if configFile is None:
        cfgFile = Path(filesPath, CONFIGFILE)
    else:
        cfgFile = Path(filesPath, configFile)

    data.setConfigFile(cfgFile)
    data.readFromFile()

    if logFile is None:
        loggingFile = Path(filesPath, LOGFILE)
    else:
        loggingFile = Path(filesPath, logFile)

    loghandler = LogRotateFileHandler(loggingFile, backupCount=10)
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s %(message)s")
    loghandler.setFormatter(formatter)

    logging.getLogger("").setLevel(logging.DEBUG)
    logging.getLogger("").addHandler(loghandler)
    logging.info("App Start.")
    logging.info("Python: %s", sys.version)

    if name is None:
        appName = NAME
    else:
        appName = name

    if version is None:
        appVersion = VERSION
    else:
        appVersion = version

    logging.info("%s-%s", appName, appVersion)


def close():
    """
    save configuration to file and write end message to log file
    """
    data.saveToFile()

    logging.info("App End.")
