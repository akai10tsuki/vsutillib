"""vsutillib version and configuration constants"""

__VERSION = (1, 0, '0', 'dev1')

VERSION = ".".join(map(str, __VERSION))
AUTHOR = "Efrain Vergara"
EMAIL = "akai10tsuki@gmail.com"
COPYRIGHT = "2018-2019, Efrain Vergara"
IMAGEFILESPATH = ""
LOCALFILESPATH = ".vsutillib"
LOGFILE = LOCALFILESPATH + "/vsutillib.log"
CONFIGFILE = LOCALFILESPATH + "/vsutillib-config.xml"
DESCRIPTION = 'Library module'
KEYWORDS = 'mkv multimedia video audio configuration'
NAME = "vsutillib"
REQUIRED = [
    'pymediainfo>=4.0',
    'lxml>=4.0'
]
URL = 'https://github.com/akai10tsuki/vsutillib'

__version__ = VERSION
