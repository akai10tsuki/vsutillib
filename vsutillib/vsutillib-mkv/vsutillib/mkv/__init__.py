"""VS module names"""

# MKV0001

#     MKVCommand,
#     MKVCommandNew,

from .classes import (
    MKVAttachment,
    MKVAttachments,
    MKVCommandParser,
    MKVParseKey,
    SourceFile,
    SourceFiles,
    VerifyMKVCommand,
    VerifyStructure,
)
from .mkvutils import (
    getMKVMerge,
    getMKVMergeVersion,
    numberOfTracksInCommand,
    resolveOverwrite,
    stripEncaseQuotes,
    unQuote,
)
