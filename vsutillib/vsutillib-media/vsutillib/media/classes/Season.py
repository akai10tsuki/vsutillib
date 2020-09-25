"""
Seasons info
"""

from .Keys import MTKeys as k


class Season:
    """Season Info"""

    def __init__(self, season=None):

        self.seasonID = None
        self.number = None
        self.premiereDate = None
        self.endDate = None
        self.summary = None
        self.episodesData = None
        self.episodes = None

        if season is not None:
            self.setInfo(season)

    def __str__(self):

        strTmp = (
            f" Season: {self.number}\n"
            f"     ID: {self.seasonID}\n"
            f"Premier: {self.premiereDate}\n"
            f"    End: {self.endDate}"
        )

        return strTmp

    def setInfo(self, season):
        """Fill season info"""

        if isinstance(season, dict):
            self.seasonID = season[k.idOfMedia]
            self.number = season[k.number]
            self.premiereDate = season[k.premiereDate]
            self.endDate = season[k.endDate]
            self.summary = season[k.summary]
