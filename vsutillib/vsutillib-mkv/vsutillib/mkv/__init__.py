"""VS module names"""

# MKV0001

from .classes import (
    IVerifyStructure,
    MergeOptions,
    MKVAttachment,
    MKVAttachments,
    MKVCommand,
    MKVCommandParser,
    MKVParseKey,
    SourceFile,
    SourceFiles,
    TrackOptions,
    TracksOrder,
    VerifyMKVCommand,
    VerifyStructure,
)
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
