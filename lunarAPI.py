import re

import requests
from bs4 import BeautifulSoup
import bs4
from disnake import OptionChoice
from mojang import MojangAPI

season = "5"

remove_spacing = lambda s: str(s).replace(" ", "").replace("\n", "").replace(
    "\t", "")


def is_vaid(query):
    if query is not None and type(query) == bs4.element.ResultSet and len(query) > 0:
        return True
    return False


def scrape_player(name):
    url = f"https://www.lunar.gg/u/{name}/souppvp"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def scrape_leaderboard(page: int, category: str):
    url = f"https://www.lunar.gg/soup/season-{season}/{category}?page={page}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def parse_stats(name):
    ret = []
    c = scrape_player(name).find(class_="list-item")
    if c is not None:
        for item in c.children:
            if item != "\n" and item != " ":
                ret.append(re.sub("[^0-9.]", "", remove_spacing(item.text)))
    else:
        ret.append("error")
    return ret


def parse_rank(name):
    ret = "error"
    c = scrape_player(name).find(class_="btn-info")
    if c is not None:
        ret = remove_spacing(c.text)
    return ret


class LeaderboardNameHelper:
    def __init__(self):
        self.fake = ["kills", "deaths", "eventwins", "killstreak", "credits"]
        self.real = ["Kills", "Deaths", "Events Won", "Highest Kill Streak", "Credits"]

    def get_real_name(self, category: str):
        return self.real[self.fake.index(category)]

    def create_options(self):
        ret = []
        for item in self.fake:
            ret.append(OptionChoice(self.get_real_name(item), item))
        return ret


class Leaderboard:
    def __init__(self, page, category):
        self.page = page
        self.category = category
        self.url = f"https://www.lunar.gg/soup/season-{season}/{category}?page={page}"
        self.leaderboard = scrape_leaderboard(page, category)

    def is_valid(self):
        ret = True
        if "error" in self.get_players() or "error" in self.get_ranks() or "error" in self.get_stats():
            ret = False
        return ret

    def get_ranks(self):
        ret = []
        c = self.leaderboard.find_all("td", class_="rank")
        if is_vaid(c):
            for item in c:
                ret.append(remove_spacing(str(item.text)))
        else:
            ret.append("error")
        return ret

    def get_players(self, force_lower=False):
        ret = []
        c = self.leaderboard.find_all("span")
        if is_vaid(c):
            for item in c:
                if list(item.parents)[0].name == "a":
                    if force_lower:
                        ret.append(remove_spacing(str(item.text).lower()))
                    else:
                        ret.append(remove_spacing(str(item.text)))
        else:
            ret.append("error")
        return ret

    def get_stats(self):
        ret = []
        c = self.leaderboard.find_all("td", class_="text-right")
        if is_vaid(c):
            for item in c:
                ret.append(remove_spacing(str(item.text)))
        else:
            ret.append("error")
        return ret

    def contains_player(self, player: str):
        if player.lower() in self.get_players(force_lower=True):
            return True
        return False


class Player:
    # Kills, Deaths, KD, Credits, Events, Highest Streak
    def __init__(self, name):
        self.name = name
        self.stats = parse_stats(name)
        self.rank = parse_rank(name)

    def is_valid(self):
        ret = True
        if self.stats[0] == "error" or self.rank == "error":
            ret = False
        return ret

    def get_kills(self):
        return self.stats[0]

    def get_deaths(self):
        return self.stats[1]

    def get_kdr(self):
        return self.stats[2]

    def get_credits(self):
        return self.stats[3]

    def get_event_wins(self):
        return self.stats[4]

    def get_highest_streak(self):
        return self.stats[5]

    def get_rank(self):
        return self.rank

    def get_uuid(self):
        return MojangAPI.get_uuid(self.name)
