"""

Series class to get series information from TVMaze
https://www.tvmaze.com/api

"""

import json
import logging
import re
import pprint
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

import vsutillib.network as net

from .Episodes import Episodes
from .Keys import MTKeys as k
from .Season import Season


MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class Series:
    """Get Series information from TVMaze"""

    def __init__(self, seriesTitle=None, seriesYear=None):

        self.seriesID = None

        self.searchTitle = seriesTitle
        self.searchYear = seriesYear

        self.seriesCandidates = None
        self.seriesData = None
        self.seasonsData = None
        self.episodesData = None

        self.seriesID = None
        self.date = None
        self.directors = None
        self.image = None
        self.overview = None
        self.title = None
        self.genre = None
        self.totalEpisodes = 0
        self.totalSpecials = 0
        self.seasons = []
        self.totalSeasons = 0

        self.episodes = None

        self.xmlMKVTags = None

        if seriesTitle is not None:
            self.search()

    def __bool__(self):
        return self.seriesID is not None

    def __str__(self):
        if self.overview is not None:
            opp = pprint.pformat(self.overview)
            opp = opp[1:-1]
            oss = opp.split("\n")
        else:
            oss = [""]

        tmpStr = (
            f"Series:         {self.title}\n"
            f"Released:       {self.date}\n"
            f"Total Episodes: {self.totalEpisodes}\n"
            f"Overview:       {oss[0][1:-1]}\n"
        )

        if len(oss) > 1:
            for index, line in enumerate(oss):
                if index == 0:
                    continue
                tmpStr += "                " + line[2:-1] + "\n"

        return tmpStr

    def search(self, title=None, year=None, seriesID=None):
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

                self.seriesCandidates = candidates

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
                    self.seriesCandidates = candidates

        # Get information from series ID found or sent
        if searchID is not None:

            self.getInfo(searchID)

        else:

            self.seriesID = None
            self.date = None
            self.title = None
            self.seriesData = None

    def getInfo(self, seriesID=None):
        """Get series information"""

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

            for index, season in enumerate(self.seasons):

                url = (
                    "http://api.tvmaze.com/seasons/"
                    + str(season.seasonID)
                    + "/episodes"
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

        # def restoreData(self, seriesData, episodesData):
        # """setup series information from variables"""

    #    self._setSeriesData(seriesData)
    #    self._setEpisodesData(episodesData)

    def _setSeriesData(self, seriesData):

        if seriesData is not None:

            self.seriesData = seriesData

            sData = seriesData[k.show]

            strTmp = sData[k.summary]
            strTmp = re.sub(r"\r", "", strTmp)
            strTmp = re.sub(r"\n", "", strTmp)
            strTmp = re.sub(r"\t", "", strTmp)
            strTmp = strTmp.replace("<p>", "").replace("</p>", "")

            self.seriesID = sData[k.idOfMedia]
            self.date = sData[k.premiered]
            self.title = sData[k.name]
            self.overview = strTmp  # self.seriesData['overview']
            self.genre = sData[k.genres]
            self.image = sData[k.image][k.medium]

    def _setSeasonsData(self, seasonsData):

        self.seasons = []
        if seasonsData is not None:
            self.seasonsData = seasonsData
            for season in seasonsData:
                s = Season(season)
                self.seasons.append(s)

    def _setEpisodesData(self, index, episodesData):

        if episodesData is not None:

            self.seasons[index].episodesData = episodesData
            self.seasons[index].episodes = Episodes(self, episodesData=episodesData)

            self.totalEpisodes = (
                self.totalEpisodes + self.seasons[index].episodes.totalEpisodes
            )
            self.totalSpecials = (
                self.totalSpecials + self.seasons[index].episodes.totalSpecials
            )

    def _xmlMKVTags(self):

        seriesInfo = {
            "TITLE": self.title,
            "DIRECTOR": self.directors,
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
