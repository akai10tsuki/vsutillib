"""
Class to organize episodes information
"""

import logging
import pprint
import re
import xml.dom.minidom as DOM

import lxml.etree as ET

from .Keys import MTKeys as k


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class Episode:
    """Information for one episode"""

    def __init__(self, parent=None):

        self.parent = parent

        self.absoluteNumber = None
        self.airedSeason = None
        self.airedEpisodeNumber = None
        self.airedSeasonID = None
        self.firstAired = None
        self.directors = None
        self.overview = None
        self.totalEpisodesSeason = None
        self.seriesId = None
        self.title = None
        self.seriesTitle = None
        self.seriesDate = None
        self.seriesOverview = None

    def __str__(self):

        if self.overview is not None:
            opp = pprint.pformat(self.overview)
            opp = opp[1:-1]
            oss = opp.split("\n")
        else:
            oss = [""]

        tmpStr = "Episode Title:  {}\nSeason:         {}\nEpisode number: {}\nOverview:       {}\n".format(  # pylint: disable=line-too-long
            str(self.title),
            str(self.airedSeason),
            str(self.airedEpisodeNumber),
            oss[0][1:-1],
        )

        if len(oss) > 1:
            for index, line in enumerate(oss):
                if index == 0:
                    continue
                tmpStr += "                " + line[2:-1] + "\n"

        return tmpStr

    @property
    def xmlMKVTags(self):
        """
        Return pretty print xml doc for MKV tags
        not all information is available at episode
        creation (Total episodes a season)
        """
        return self._xmlMKVTags()

    def _xmlMKVTags(self):
        """pretty print MKV xml tags"""

        tags = ET.Element(k.Tags)
        tags.append(ET.Comment(" SERIES "))

        tvInfo = [
            {
                k.Tag: " Series ",
                k.TargetTypeValue: "70",
                k.TITLE: self.seriesTitle,
                k.DATE_RELEASED: self.seriesDate,
                k.COMMENT: self.seriesOverview,
            },
            {
                k.Tag: " Season ",
                k.TargetTypeValue: "60",
                k.PART_NUMBER: self.airedSeason,
                k.TOTAL_PARTS: self.totalEpisodesSeason,
            },
            {
                k.Tag: " Episode ",
                k.TargetTypeValue: "50",
                k.PART_NUMBER: self.airedEpisodeNumber,
                k.DATE_RELEASED: self.firstAired,
                k.TITLE: self.title,
                k.COMMENT: self.overview,
            },
        ]

        for info in tvInfo:

            for key in info:

                if key == k.Tag:
                    tag = ET.SubElement(tags, k.Tag)
                    tag.append(ET.Comment(info[key]))

                elif key == k.TargetTypeValue:
                    targets = ET.SubElement(tag, k.Targets)
                    targettypevalue = ET.SubElement(targets, k.TargetTypeValue)
                    targettypevalue.text = info[key]

                else:
                    simple = ET.SubElement(tag, k.Simple)

                    elemName = ET.SubElement(simple, k.Name)
                    elemName.text = str(key)

                    elemString = ET.SubElement(simple, k.String)
                    elemString.text = str(info[key])

        xmlDoc = DOM.parseString(
            ET.tostring(
                tags,
                encoding="UTF-8",
                doctype='<!DOCTYPE Tags SYSTEM "matroskatags.dtd">',
            )
        )

        return xmlDoc.toprettyxml(indent="    ")


class Episodes:
    """
    Episodes class holds information for every episode

    The TV Database has Season 0 for specials
        Season list is 0 based
    For episodes episode 0 is set to None use
        1 base list for episodes
    """

    def __init__(self, parent=None, episodesData=None):

        self.parent = parent
        self._episodes = [[None]]  # season 0
        self.episodesData = None if episodesData is None else episodesData
        self.totalEpisodes = 0
        self.totalSpecials = 0
        self.seriesTitle = parent.title
        self.seriesDate = parent.date
        self.seriesOverview = parent.overview
        self.hasSpecials = False

        # for __next__
        self._totalEpisodesIndex = 0
        self._episodesIndex = 0
        self._startIteration = True

        self.totalEpisodesSeason = countEpisodes(self.episodesData)
        self.totalSpecials = self.totalEpisodesSeason[k.totalSpecials]
        self.totalEpisodes = self.totalEpisodesSeason[k.totalEpisodes]

        self._episodes = [None] * (self.totalEpisodes + 1)

        for e in self.episodesData:

            if e[k.number] is not None:
                episode = Episode(self)
                episode.airedSeason = e[k.season]
                episode.airedEpisodeNumber = e[k.number]
                episode.totalEpisodesSeason = self.totalEpisodesSeason[e[k.season]]
                episode.airedSeasonID = e[k.season]
                episode.firstAired = e[k.airdate]
                strTmp = "" if e[k.summary] is None else e[k.summary]
                if strTmp:
                    # some overviews have this literals that mess
                    # printing of plot summary's
                    strTmp = re.sub(r"\r", "", strTmp)
                    strTmp = re.sub(r"\n", "", strTmp)
                    strTmp = re.sub(r"\t", "", strTmp)
                    strTmp = strTmp.replace("<p>", "").replace("</p>", "")
                episode.overview = strTmp
                episode.seriesId = e[k.idOfMedia]
                episode.title = e[k.name]

                episode.seriesTitle = parent.title
                episode.seriesDate = parent.date
                episode.seriesOverview = parent.overview

                self._episodes[e[k.number]] = episode

        if self.totalSpecials > 0:
            self.hasSpecials = True

    def __getitem__(self, index):
        return self._episodes[index]

    def __iter__(self):
        return self

    def __next__(self):

        if self._totalEpisodesIndex >= (self.totalEpisodes + self.totalSpecials):
            self._totalEpisodesIndex = 0
            self._episodesIndex = 0
            self._startIteration = True
            raise StopIteration
        else:
            if self._startIteration:
                self._episodesIndex = 0
                self._startIteration = False

            if self._episodesIndex >= len(self._episodes) - 1:
                self._episodesIndex = 0

            self._episodesIndex += 1
            self._totalEpisodesIndex += 1

            return self._episodes[self._episodesIndex]


def countEpisodes(episodes):
    """Count pisodes per season return dictionary with info"""

    episodesPerSeason = {}
    totalSeasons = 0
    episodesPerSeason[k.totalSpecials] = 0
    episodesPerSeason[k.totalEpisodes] = 0
    seasons = []

    for e in episodes:

        season = e[k.season]

        if season not in seasons:
            seasons.append(season)
            episodesPerSeason[season] = 0
            totalSeasons += 1

        episodesPerSeason[season] = episodesPerSeason[season] + 1

        episodesPerSeason[k.totalEpisodes] = episodesPerSeason[k.totalEpisodes] + 1

    episodesPerSeason[k.totalSeasons] = totalSeasons
    # if 0 in episodesPerSeason:
    #    episodesPerSeason[k.totalSpecials] = episodesPerSeason[0]

    seasons.sort()
    episodesPerSeason[k.seasons] = seasons

    return episodesPerSeason
