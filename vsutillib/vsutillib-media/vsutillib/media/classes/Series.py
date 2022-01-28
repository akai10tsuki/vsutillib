"""

Series - class to get series information from TVMaze
https://www.tvmaze.com/api

5312
http://api.tvmaze.com/shows/5312?embed[]=episodes?embed[]=specials&embed[]=cast&embed[]=akas

"""

from __future__ import annotations

import json
import logging
import re
import pprint
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

from typing import Any, Dict, List, Optional, Union

import vsutillib.network as net

from .Keys import MTKeys as k


# type aliases
TVMazeDict = Dict[str, Union[str, int, None]]
TVMazeList = List[TVMazeDict]


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class Series:
    """Get Series information from TVMaze"""

    def __init__(
        self, seriesTitle: Optional[str] = None, seriesYear: Optional[int] = None
    ) -> None:

        self.searchTitle: str = seriesTitle
        self.searchYear: int = seriesYear

        self.candidatesData: TVMazeList = None
        self.seriesData: TVMazeList = None
        self.seasonsData: TVMazeList = None
        self.episodesData: TVMazeList = None

        self.seriesID: int = -1
        self.premieredDate: str = ""
        self.image: str = ""
        self.overview: str = ""
        self.title: str = ""
        self.genre: List[str] = []
        self.url: str = ""
        self.status: str = ""

        self.totalEpisodes: int = 0
        self.totalSpecials: int = 0
        self.totalSeasons: int = 0
        self.seasons: List[Season] = []

        self.episodes: List[Episode] = []

        # self.xmlMKVTags: str = None

        if seriesTitle is not None:
            self.search()

    def __bool__(self) -> int:
        return self.seriesID is not None

    def __str__(self) -> str:
        if self.overview is not None:
            opp = pprint.pformat(self.overview)
            opp = opp[1:-1]
            oss = opp.split("\n")
        else:
            oss = [""]

        tmpStr = (
            f"Series:         {self.title}\n"
            f"Premiered:      {self.premieredDate}\n"
            f"Status:         {self.status}\n"
            f"Total Seasons:  {self.totalSeasons}\n"
            f"Total Episodes: {self.totalEpisodes}\n"
            f"Total Specials: {self.totalSpecials}\n"
            f"Genre:          {self.genre}\n"
            f"TVmaze:         {self.url}\n"
            f"Overview:       {oss[0][1:-1]}\n"
        )

        if len(oss) > 1:
            for index, line in enumerate(oss):
                if index == 0:
                    continue
                tmpStr += "                " + line[2:-1] + "\n"

        return tmpStr

    def search(
        self,
        title: Optional[str] = None,
        year: Optional[int] = None,
        seriesID: Optional[int] = None,
    ) -> None:
        """Search for the series ID"""

        searchID = seriesID

        if searchID is None:
            # look for id

            if title is None:
                if self.searchTitle is not None:
                    searchTitle = self.searchTitle
                else:
                    return
            else:
                searchTitle = title

            if year is None:
                if self.searchYear is not None:
                    searchYear = self.searchYear
                else:
                    searchYear = None
            else:
                searchYear = year

            # get ID
            url = "http://api.tvmaze.com/search/shows?q=" + urllib.parse.quote_plus(
                searchTitle
            )
            request = net.UrlRequest(url=url)

            if request.status == 200:

                bJson = request.message
                data = json.loads(bJson.decode("utf-8"))

                candidates = data

                self.candidatesData = candidates

                candidateIndex = []

                for index, series in enumerate(candidates):
                    if str(searchYear) == series["show"]["premiered"][:4]:
                        candidateIndex.append(index)

                totalCandidates = len(candidateIndex)

                if totalCandidates == 1:
                    # This should be it
                    index = candidateIndex[0]

                    searchID = candidates[index]["show"][k.idOfMedia]

                    data = candidates[index]

                    self._setSeriesData(data)

                else:

                    self.seriesID = None
                    self.date = None
                    self.title = None

        # Get information from series ID found or sent
        if searchID is not None:

            self.getInfo(searchID)

        else:

            self.seriesID = None
            self.date = None
            self.title = None
            self.seriesData = None

    def getInfo(self, seriesID: Optional[int] = None) -> None:
        """Get series information"""

        searchID = None

        if seriesID is None:
            if self.seriesID is None:
                self.search(seriesID)
                if self.seriesID is None:
                    return
            else:
                searchID = self.seriesID
        else:
            searchID = seriesID

        # Get seasons

        url = "https://api.tvmaze.com/shows/" + str(searchID) + "/seasons"

        request = net.UrlRequest(url=url)

        if request.status == 200:

            bJson = request.message
            data = json.loads(bJson.decode("utf-8"))

            self.seasonsData = data
            # Answer saved in case more than one match
            self._setSeasonsData(data)

        else:

            self.seasonsData = None
            self.seasons = []

        if self.seasons:

            self.totalSeasons = len(self.seasons)

            for index, season in enumerate(self.seasons):

                url = (
                    "http://api.tvmaze.com/seasons/"
                    + str(season.seasonID)
                    + "/episodes?specials=1"
                )
                # Get episodes by season

                request = net.UrlRequest(url=url)

                if request.status == 200:

                    bJson = request.message
                    data = json.loads(bJson.decode("utf-8"))

                    # Answer saved in case more than one match
                    self._setEpisodesData(index, data)

                else:

                    self.seasons[index].episodesData = None
                    self.seasons[index].episodes = None

    def _setSeriesData(self, data: TVMazeList) -> None:

        if data is not None:

            self.seriesData = data

            strTmp = data[k.summary]
            strTmp = re.sub(r"\r", "", strTmp)
            strTmp = re.sub(r"\n", "", strTmp)
            strTmp = re.sub(r"\t", "", strTmp)
            strTmp = strTmp.replace("<p>", "").replace("</p>", "")

            self.seriesID = data[k.idOfMedia]
            self.premieredDate = data[k.premiered]
            self.title = data[k.name]
            self.overview = data[k.summary]
            self.genre = data[k.genres]
            self.image = data[k.image][k.medium]
            self.url = data[k.url]
            self.status = data[k.status]

    def _setSeasonsData(self, data: TVMazeList) -> None:

        self.seasons = []
        if data is not None:
            self.seasonsData = data
            for season in data:
                s = Season(season)
                self.seasons.append(s)

    def _setEpisodesData(self, index, episodesData: TVMazeList) -> None:

        if episodesData is not None:

            self.seasons[index].episodesData = episodesData
            self.seasons[index].episodes = Episodes(episodesData)

            self.totalEpisodes += self.seasons[index].episodes.totalEpisodes
            self.totalSpecials += self.seasons[index].episodes.totalSpecials

    def _xmlMKVTags(self) -> None:

        seriesInfo = {
            "TITLE": self.title,
            "DIRECTOR": "",  # TVMaze don't provide this
            "DATE_RELEASED": self.date,
            "COMMENT": self.overview,
        }
        tags = ET.Element("Tags")
        tags.set("version", "1.0")
        tags.append(ET.Comment(" series "))

        tag = ET.SubElement(tags, "Tag")

        targets = ET.SubElement(tag, "Targets")

        targetTypeValue = ET.SubElement(targets, "TargetTypeValue")
        targetTypeValue.text = "50"

        for key in seriesInfo:
            simple = ET.SubElement(tag, "Simple")

            elemName = ET.SubElement(simple, "Name")
            elemName.text = str(key)

            elemString = ET.SubElement(simple, "String")
            elemString.text = str(seriesInfo[key])

        xmlDoc = DOM.parseString(ET.tostring(tags, encoding="utf-8"))

        self.xmlMKVTags = xmlDoc.toprettyxml(indent="    ")


class Season:
    """Season Info"""

    def __init__(self, data: Optional(TVMazeDict) = None) -> None:

        self.seasonID = None
        self.number = None
        self.premiereDate = None
        self.endDate = None
        self.summary = None
        self.url = None
        self.episodes = None
        self.episodesData = None

        if data is not None:
            self.setInfo(data)

    def __str__(self) -> str:

        strTmp = (
            f"Season:         {self.number}\n"
            f"ID:             {self.seasonID}\n"
            f"Premier:        {self.premiereDate}\n"
            f"End:            {self.endDate}\n"
            f"Total Episodes: {self.episodes.totalEpisodes}\n"
            f"url:            {self.url}"
        )

        return strTmp

    def setInfo(self, data: Optional(TVMazeDict) = None) -> None:
        """Fill season info"""

        if data is not None:
            self.seasonID = data[k.idOfMedia]
            self.number = data[k.number]
            self.premiereDate = data[k.premiereDate]
            self.endDate = data[k.endDate]
            self.summary = data[k.summary]
            self.url = data[k.url]


class Episodes:
    """
    Episodes class holds information for every episode

    The TV Database has Season 0 for specials
        Season list is 0 based
    For episodes episode 0 is set to None use
        1 base list for episodes
    """

    def __init__(
        self,
        episodesData: Optional[TVMazeList] = None,
    ) -> None:

        self.episodesData = None
        self.totalEpisodes = 0
        self.totalSpecials = 0
        self.hasSpecials = False

        # for __next__
        self._episodesIndex = 0
        self._startIteration = True

        self._episodes = []

        if episodesData is not None:
            self.setData(episodesData)

    def __len__(self) -> int:
        return len(self._episodes)

    def __getitem__(self, index: int) -> Episode:
        return self._episodes[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._episodes[index] = value

    def __iter__(self) -> Episodes:
        return self

    def __next__(self) -> Episode:

        if self._episodesIndex >= len(self._episodes):
            self._episodesIndex = 0
            self._startIteration = True
            raise StopIteration
        else:
            if self._startIteration:
                self._episodesIndex = 0
                self._startIteration = False

            self._episodesIndex += 1

            return self._episodes[self._episodesIndex - 1]

    def setData(self, data: TVMazeList) -> None:

        self.episodesData = data

        for e in self.episodesData:

            episode = Episode(self, e)
            self._episodes.append(episode)
            if episode.airedEpisodeNumber is None:
                self.totalSpecials += 1
            else:
                self.totalEpisodes += 1

        if self.totalSpecials > 0:
            self.hasSpecials = True


class Episode:
    """Information for one episode"""

    def __init__(self, parent: Episodes, data: TVMazeDict) -> None:

        self.parent = parent

        self.airedSeason = -1
        self.airedEpisodeNumber = None
        self.airedSeasonID = None
        self.firstAired = None
        self.overview = ""
        self.episodeID = None
        self.title = None
        self.url = ""
        self.image = ""

        self._initHelper(data)

    def _initHelper(self, data: TVMazeDict) -> None:

        self.airedSeason = data[k.season]
        self.airedEpisodeNumber = data[k.number]
        self.airedSeasonID = data[k.season]
        self.firstAired = data[k.airdate]
        self.overview = data[k.summary]
        self.episodeID = data[k.idOfMedia]
        self.title = data[k.name]
        self.url = data[k.url]
        self.image = data[k.image]

    def __str__(self) -> str:

        if self.overview is not None:
            opp = pprint.pformat(self.overview)
            opp = opp[1:-1]
            oss = opp.split("\n")
        else:
            oss = [""]

        tmpStr = (
            f"Episode Title:  {self.title}\n"
            f"Season:         {self.airedSeason}\n"
            f"Episode number: {self.airedEpisodeNumber}\n"
            f"Overview:       {oss[0][1:-1]}\n"
        )

        if len(oss) > 1:
            for index, line in enumerate(oss):
                if index == 0:
                    continue
                tmpStr += "                " + line[2:-1] + "\n"

        return tmpStr

    @property
    def xmlMKVTags(self) -> str:
        """
        Return pretty print xml doc for MKV tags
        not all information is available at episode
        creation (Total episodes a season)
        """
        return self._xmlMKVTags()

    def _xmlMKVTags(self) -> str:
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

            tag = None
            targets = None

            for key in info:

                if key == k.Tag:
                    tag = ET.SubElement(tags, k.Tag)
                    tag.append(ET.Comment(info[key]))

                elif (key == k.TargetTypeValue) and tag is not None:
                    targets = ET.SubElement(tag, k.Targets)
                    targettypevalue = ET.SubElement(targets, k.TargetTypeValue)
                    targettypevalue.text = info[key]

                else:
                    if tag is not None:
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
                method="xml",
            )
        )

        return xmlDoc.toprettyxml(indent="    ")
