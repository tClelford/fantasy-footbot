from ctypes.wintypes import HINSTANCE
from typing import Dict, Tuple, List
import pandas as pd
import os
import requests
import pprint


def roi(season=2022, use_prev_season=True, ewma=20) -> None:
    df = pd.read_csv("./data/cleaned_merged_seasons.csv")
    this_season = to_season_name(season)
    last_season = to_season_name(season-1)
    this_seasons_data = df.loc[df["season_x"] == this_season]

    gameweek = 1  # annoyingly the "round" is 1 indexed

    if not this_seasons_data.empty:
        gameweek = max(this_seasons_data["round"].max() + 1, 38)

    start_gameweek = gameweek - ewma
    if start_gameweek > 0:
       # current season only!
        raise Exception("todo")

    else:
        # gotta deal with last season and potential for championship players
        raise Exception("todo")


def simple_roi(season=2022) -> Dict[int, List[Dict]]:
    if season != 2022:
        raise Exception("Not an api call")
    current_data = requests.get(
        f"https://fantasy.premierleague.com/api/bootstrap-static/").json()
    players = list(current_data["elements"])
    print(players[0]["id"])
    season_name = to_season_name(season)
    folder = f"./data/{season_name}/players"

    positions = {
        1: [],
        2: [],
        3: [],
        4: []
    }

    for (root, dirs, files) in os.walk(folder, topdown=True):
        if root == folder:
            continue
        forename, surname, id = root.split("\\")[1].split("_")
        id = int(id)
        history = pd.read_csv(root + "/history.csv")
        last_year = history.loc[history["season_name"]
                                == to_season_name(season-1).replace("-", "/")]
        if last_year.empty:
            print(f"{surname}, {forename}: todo")
            continue

        points = last_year["total_points"].values[0]
        player = list(filter(lambda p: p["id"] == id, players))[0]
        cost = player["now_cost"]
        roi = points / cost
        dic = {
            "name": player["web_name"],
            "cost": cost,
            "roi": roi,
            "team": current_data["teams"][player["team"]-1]["short_name"]
        }
        positions[player["element_type"]].append(dic)

    pprint.pprint(sorted(positions[2], key=lambda p: p["roi"], reverse=True)[:10])



def get_price_api(id):
    res = requests.get(
        f"https://fantasy.premierleague.com/api/element-summary/{id}/").json()
    return res["history"][0]["value"]


def to_season_name(season: int) -> str:
    return f"{season}-{str( season+1)[2:]}"


rois = simple_roi(2022)