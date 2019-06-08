"""
vsutillib version and configuration constants
"""

__VERSION = (1, 0, '1b1', 'dev1')

VERSION = ".".join(map(str, __VERSION))
AUTHOR = "Efrain Vergara"
EMAIL = "akai10tsuki@gmail.com"
COPYRIGHT = "2018-2019, Efrain Vergara"
LICENSE = "MIT"

IMAGEFILESPATH = ""
LOCALFILESPATH = ".vsutillib"
LOGFILE = LOCALFILESPATH + "/vsutillib.log"
CONFIGFILE = LOCALFILESPATH + "/vsutillib-config.xml"
DESCRIPTION = 'Library module'
KEYWORDS = 'mkv multimedia video audio configuration'
NAME = "vsutillib"
REQUIRED = [
    'pymediainfo>=4.0',
    'lxml>=4.0',
    'vsutillib-files>=1.0.0',
    'vsutillib-log>=1.0.0',
    'vsutillib-macos>=1.0.0',
    'vsutillib-media>=1.0.0',
    'vsutillib-network>=1.0.0',
    'vsutillib-process>=1.0.0',
    'vsutillib-vsxml>=1.0.0',
]
URL = 'https://github.com/akai10tsuki/vsutillib'

__version__ = VERSION
