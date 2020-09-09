"""
adjustSources try and adjust tracks to account for structure difference
"""

import copy

from vsutillib.media import findSimilarTrack, MediaFileInfo, MediaTrackInfo

from .classes import TracksOrder


def adjustSources(oCommand, index):
    """
    adjustSources scan tracks and adjust for structure difference

    Args:
        oCommand (MKVCommandParser): current commands for job
        index (int): command index

    Returns:
        bool: True if conflict resolved.  False otherwise.
    """

    rc = False

    tracksOrder = TracksOrder(oCommand.cliTracksOrder)
    tracksOrderTranslation = {}
    sourceFiles = oCommand.oSourceFiles[index]
    dummyTrack = MediaTrackInfo()

    for baseIndex, oBaseFile in enumerate(oCommand.oBaseFiles):
        baseFileInfo = oBaseFile.mediaFileInfo
        sourceFileInfo = MediaFileInfo(sourceFiles[baseIndex])
        trackOptions = oBaseFile.trackOptions
        translate = {}

        for track in oBaseFile.trackOptions.tracks:
            i = int(track)
            if len(baseFileInfo) <= 0:
                # source file with no tracks
                return False
            trackBase = baseFileInfo[i]
            if i < len(sourceFileInfo):
                # source less tracks than base
                trackSource = sourceFileInfo[i]
            else:
                trackSource = dummyTrack
            if trackBase != trackSource:
                trackSimilar, _ = findSimilarTrack(sourceFileInfo, trackBase)
                if trackSimilar >= 0:
                    translate[track] = str(trackSimilar)
                    trackSource = sourceFileInfo[trackSimilar]
        if translate:
            if not rc:
                rc = True
            template = oCommand.commandTemplates[index]
            trackOpts = copy.deepcopy(trackOptions)
            trackOpts.translation = translate
            newTemplate = template.replace(trackOpts.options, trackOpts.strOptions(), 1)
            oCommand.commandTemplates[index] = newTemplate
            tracksOrderTranslation.update(trackOpts.orderTranslation)

    if tracksOrderTranslation:
        tracksOrder.translation = tracksOrderTranslation
        oCommand.tracksOrder[index] = tracksOrder.strOrder()

    return rc
