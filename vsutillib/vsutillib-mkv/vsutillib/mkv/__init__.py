"""VS module names"""

# MKV0001

# Classes
from .classes import (
    IVerifyStructure,
    MergeOptions,
    MKVAttachment,
    MKVAttachments,
    MKVCommandParser,
    MKVParseKey,
    SourceFile,
    SourceFiles,
    TrackOptions,
    TracksOrder,
    VerifyMKVCommand,
    VerifyStructure,
)

# Functions
from .adjustSources import adjustSources
from .mkvutils import (
    convertToBashStyle,
    generateCommand,
    getMKVMerge,
    getMKVMergeVersion,
    numberOfTracksInCommand,
    quoteString,
    resolveOverwrite,
    stripEncaseQuotes,
    unQuote,
)
