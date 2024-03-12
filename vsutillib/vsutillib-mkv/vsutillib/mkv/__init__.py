"""VS module names"""

# MKV0001

# Classes
from .classes import (
    IVerifyStructure,
    MergeOptions,
    MKVAttachment,
    MKVAttachments,
    MKVParseKey,
    MKVCommandParser,
    SourceFile,
    SourceFiles,
    TrackOptions,
    TracksOrder,
    VerifyMKVCommand,
    VerifyStructure,
)

# Functions
from .adjustSources import adjustSources
from .generateCommandTemplate import generateCommandTemplate
from .mkvutils import (
    convertToBashStyle,
    generateCommand,
    getMKVMerge,
    getMKVMergeEmbedded,
    getMKVMergeVersion,
    numberOfTracksInCommand,
    quoteString,
    resolveOverwrite,
    restoreEscapeQuote,
    stripEncaseQuotes,
    setEncaseQuotes,
    unQuote,
)
