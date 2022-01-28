"""
Movie - class to get information from The Movie Database

 http://www.omdbapi.com/?i=tt3896198&apikey=8903ce2e

 http://www.omdbapi.com/?t=Happy+Lesson&y=2002

moviedbKey = 955ae1de8a8e94a5907b7bb7b286fdea
omdbKey = 8903ce2e

https://api.themoviedb.org/3/configuration?api_key=955ae1de8a8e94a5907b7bb7b286fdea

"""

import json
import logging
import pprint
import urllib.parse
import urllib.request
import xml.dom.minidom as DOM
import xml.etree.ElementTree as ET

from vsutillib import network as net

from .Keys import MTKeys as k

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())


class Movie:
    """
    class to search movie information
    from Internet databases
    supports: The Movie Database https://www.themoviedb.org
              Open Movie Database https://www.omdbapi.com/
    """

    __SERVICESITES = {"moviedbKey": k.moviedb, "omdbKey": k.omdb}
    __SERVICEKEYS = ["moviedbKey", "omdbKey"]

    __DATAKEYSITES = {"title": k.moviedb, "Title": k.omdb}
    __DATAKEYSEARCH = ["title", "Title"]

    def __init__(self, movieTitle=None, movieYear=None, **kwargs):

        self.searchTitle = movieTitle
        self.searchYear = movieYear

        self.apiKey = None
        self.serviceSite = None

        self._setupService(**kwargs)

        self.status = None
        self.data = None
        self.searchData = None
        self.movieID = None
        self.imdbID = None
        self.numberOfResults = 0

        self.date = None
        self.director = None
        self.overview = None
        self.title = None

        if self.searchTitle is not None:

            self.search()

    def __bool__(self):

        return self.movieID is not None

    def __str__(self):

        if self.overview is not None:
            opp = pprint.pformat(self.overview)
            opp = opp[1:-1]
            oss = opp.split("\n")

        else:
            oss = [""]

        tmpStr = "Movie:    {}\nDirector: {}\nReleased: {}\nOverview: {}\n".format(  # pylint: disable=line-too-long
            self.title, self.director, self.date, oss[0][1:-1]
        )

        if len(oss) > 1:
            for index, line in enumerate(oss):
                if index == 0:
                    continue

                tmpStr += "          " + line[2:-1] + "\n"

        return tmpStr

    @property
    def xmlMKVTags(self):
        """MKV Tags for movie"""

        return self._xmlMovieMKVTags()

    def search(self, title=None, year=None, **kwargs):
        """Search for the movie ID"""

        if kwargs:
            self._setupService(**kwargs)

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

        url = self._serviceUrl(title=searchTitle, year=searchYear, serviceType=k.search)

        request = net.UrlRequest(url=url)

        if request.status == 200:

            bJson = request.message
            data = json.loads(bJson.decode("utf-8"))

            if self.serviceSite == k.moviedb:

                self.numberOfResults = data[k.total_results]
                self.searchData = data

                if data[k.total_results] == 1:
                    self.movieID = data[k.results][0][k.idOfMedia]
                    self.getInfo()
                else:
                    # search is not unique clear id inspect data to decide correct movie
                    self.movieID = None

            elif self.serviceSite == k.omdb:
                # self.imdbID = data[k.imdbID]
                # self.movieID = self.imdbID
                # self.searchData = data
                self.data = data
                self._setData(data)
            else:
                self.movieID = None
                self.data = None

        else:
            self.movieID = None
            self.data = None

    def getInfo(self, movieID=None, **kwargs):
        """Get Movie information"""

        if kwargs:
            self._setupService(**kwargs)

        if movieID is None:
            if self.movieID is None:
                return
            else:
                searchID = self.movieID
        else:
            searchID = movieID

        url = self._serviceUrl(movieID=searchID, serviceType=k.getinfo)

        request = net.UrlRequest(url=url)

        if request.status == 200:

            bJson = request.message
            data = json.loads(bJson.decode("utf-8"))

            self.status = request.status
            self.searchData = None
            self._setData(data)

        else:

            self.movieID = None
            self.searchData = None
            self.status = None
            self.data = None

        return

    def restoreData(self, movieData):
        """setup movie info from saved data"""

        self.serviceSite = None
        self.apiKey = None

        for key in self.__DATAKEYSEARCH:
            if key in movieData:
                self.serviceSite = self.__DATAKEYSITES[key]
                break

        print("Service: ", self.serviceSite)

        if self.serviceSite is not None:
            self._setData(movieData)

    def _setupService(self, **kwargs):

        iLen = len(kwargs)

        if iLen <= 0:
            raise KeyError("No API key suplied.")
        elif iLen > 1:
            raise KeyError("More than one API key suplied {}".format(str(kwargs)))

        key, value = tuple(kwargs.items())[0]

        if key not in self.__SERVICEKEYS:
            print("Bummer!!!")
            raise KeyError("Error key {} not registered.".format(key))

        if key not in self.__SERVICESITES:
            print("Bummer!!!")
            raise RuntimeError("Cannot set service site the site keys may be missing.")

        self.apiKey = value
        self.serviceSite = self.__SERVICESITES[key]

    def _setData(self, movieData):

        if movieData is not None:

            self.data = movieData

            if self.serviceSite == k.moviedb:

                self.movieID = self.data[k.idOfMedia]
                self.date = self.data[k.release_date]
                self.title = self.data[k.title]
                self.overview = self.data[k.overview]

                movieCredits = self.data[k.creditsOfVideo]
                movieCrew = movieCredits[k.crew]
                for d in movieCrew:
                    if d[k.department] == k.Directing:
                        if d[k.job] == k.Director:
                            self.director = d[k.name]

                self._xmlMovieMKVTags()

            elif self.serviceSite == k.omdb:

                self.movieID = self.data[k.imdbID]
                self.date = self.data[k.Released]
                self.title = self.data[k.Title]
                self.overview = self.data[k.Plot]
                self.director = self.data[k.Director]

        else:
            self.movieID = None
            self.data = None

    def _xmlMovieMKVTags(self):

        movieInfo = {
            k.TITLE: self.title,
            k.DIRECTOR: self.director,
            k.DATE_RELEASED: self.date,
            k.COMMENT: self.overview,
        }
        tags = ET.Element(k.Tags)
        tags.append(ET.Comment(" MOVIE "))

        tag = ET.SubElement(tags, k.Tag)

        targets = ET.SubElement(tag, k.Targets)

        targetTypeValue = ET.SubElement(targets, k.TargetTypeValue)
        targetTypeValue.text = "50"

        for key in movieInfo:
            simple = ET.SubElement(tag, k.Simple)

            elemName = ET.SubElement(simple, k.Name)
            elemName.text = str(key)

            elemString = ET.SubElement(simple, k.String)
            elemString.text = str(movieInfo[key])

        xmlDoc = DOM.parseString(ET.tostring(tags, encoding="utf-8"))

        return xmlDoc.toprettyxml(indent="    ")

    def _serviceUrl(self, title=None, year=None, movieID=None, serviceType=None):

        if title is None:
            if self.searchTitle is not None:
                searchTitle = self.searchTitle
            else:
                return None
        else:
            searchTitle = title

        if year is None:
            if self.searchYear is not None:
                searchYear = self.searchYear
            else:
                searchYear = None
        else:
            searchYear = year

        if movieID is None:
            if serviceType == k.getinfo:
                return None
            if self.movieID is not None:
                searchID = self.movieID
            else:
                searchID = None
        else:
            searchID = movieID

        if serviceType == k.search:
            if self.serviceSite == k.moviedb:

                url = "https://api.themoviedb.org/3/search/movie?api_key={}".format(
                    self.apiKey
                )  # pylint: disable=line-too-long
                qYear = "" if searchYear is None else "&year={}".format(searchYear)
                url += "&query=" + urllib.parse.quote_plus(searchTitle) + qYear
                return url

            elif self.serviceSite == k.omdb:

                url = "http://www.omdbapi.com/?t={}&apikey={}".format(
                    urllib.parse.quote_plus(searchTitle), self.apiKey
                )
                qYear = "" if searchYear is None else "&y={}".format(searchYear)
                url += qYear
                return url

        if serviceType == k.getinfo:

            if self.serviceSite == k.moviedb:
                url = (
                    "https://api.themoviedb.org/3/movie/"
                    + str(searchID)
                    + "?api_key={}&append_to_response=credits".format(self.apiKey)
                )
                return url
            elif self.serviceSite == k.omdb:
                url = "http://www.omdbapi.com/?i={}&apikey={}".format(
                    searchID, self.apiKey
                )
                return url

        return None
