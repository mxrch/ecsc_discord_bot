from copy import deepcopy

import httpx
from bs4 import BeautifulSoup as bs


class Country():
    def __init__(self, index, name, points):
        self.index = index
        self.name = name
        self.points = points
        self.delta = 0 # 0 = not moving, 1 = up, 2 = down

    def __eq__(self, other):
        if not isinstance(other, Country):
            return NotImplemented
        return vars(self) == vars(other)

class ECSC_Stats():
    def __init__(self):
        self.as_client = httpx.AsyncClient()

        self.old_scoreboard = []
        self.scoreboard = []

    async def fetch_scoreboard(self):
        req = await self.as_client.get("https://ecsc.eu/leaderboard")
        body = bs(req.text, 'html.parser')
        countries = body.find("tbody").find_all("tr")

        scoreboard = []
        for nb,country in enumerate(countries):
            index = nb + 1
            name = country.find("span", {"class": "liveboard-country"}).text
            points = int(country.find("span", {"class": "progress-number"}).text)

            country = Country(index, name, points)
            scoreboard.append(country)

        return scoreboard

    async def refresh(self):
        self.old_scoreboard = deepcopy(self.scoreboard)
        self.scoreboard = await self.fetch_scoreboard()

    def get_deltas(self):
        deltas = deepcopy(self.scoreboard)

        if not self.old_scoreboard:
            return deltas

        countries_indexes_cache = {}
        for country in self.old_scoreboard:
            countries_indexes_cache[country.name] = country.index
        
        for nb,country in enumerate(self.scoreboard):
            cached_index = countries_indexes_cache[country.name]
            if cached_index == country.index:
                deltas[nb].delta = 0
            elif cached_index > country.index:
                deltas[nb].delta = 1
            elif cached_index < country.index:
                deltas[nb].delta = 2

        return deltas