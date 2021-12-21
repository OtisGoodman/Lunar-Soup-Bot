import re

import requests
from bs4 import BeautifulSoup
from mojang import MojangAPI

remove_spacing = lambda s: str(s).replace(" ", "").replace("\n", " ")


def scrape(name):
    url = f"https://www.lunar.gg/u/{name}/souppvp"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def scrape_stats(name):
    ret = []
    c = scrape(name).find(class_="list-item")
    if c is not None:
        for item in c.children:
            if item != "\n" and item != " ":
                ret.append(re.sub("[^0-9.]", "", remove_spacing(item.text)))
    else:
        ret.append("error")
    return ret


def scrape_rank(name):
    ret = "error"
    c = scrape(name).find(class_="btn-info")
    if c is not None:
        ret = remove_spacing(c.text)
    return ret


class Player:
    # Kills, Deaths, KD, Credits, Events, Highest Streak
    def __init__(self, name):
        self.name = name
        self.stats = scrape_stats(name)
        self.rank = scrape_rank(name)

    def isValid(self):
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

