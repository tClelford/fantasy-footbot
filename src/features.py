import os
import pandas as pd
import re


class Position:
    GK = "GK"
    DEF= "DEF"
    MID="MID"
    FWD="FWD"


THIS_YEAR = "2022-23"


def minutes_to_points(mins: int) -> int:
    if mins <= 0:
        return 0
    if mins < 60:
        return 1
    if mins >= 60:
        return 2


goal_multiplier = {Position.GK: 6, Position.DEF: 6, Position.MID: 5, Position.FWD: 4}


def defence_points(position:str, conceeded:float, saves:float)-> float:
    return {
        Position.FWD:0,
        Position.MID: max(0, 1-conceeded),
        Position.DEF: defender_points(conceeded),
        Position.GK: gk_points(conceeded, saves)
    }[position]


def defender_points(conceeded: float)-> float:
    clean_sheet_bonus = 4 * max((1-conceeded), 0)
    concession_loss = conceeded // 2
    return clean_sheet_bonus - concession_loss


def gk_points(conceeded: float, saves: float)-> float:
    save_points = saves //3
    return save_points + defender_points(conceeded)



def calc_points(
    position: str,
    minutes: float,
    goals: float,
    assists: float,
    conceeded: float,
    yellows: float,
    reds: float,
    ogs: float,
    saves: float,
    pen_saves: float,
    pen_misses: float
) -> float:
    points = 0
    points += goals * goal_multiplier[position]
    points += assists * 3
    points += minutes_to_points(90/minutes)
    points += yellows * -1
    points += reds * -3
    points += ogs * -2
    points += defence_points(position, conceeded, saves)
    points += -2 * pen_misses
    points += 5 * pen_saves
    return points
    


def ewma_understats(player_name: str, weeks: int) -> float:
    path = f"./data/{THIS_YEAR}/understat"
    for f in os.listdir(path):
        # print(f)
        match = re.match(f"{player_name}_.*.csv", f)
        if not match:
            continue
        # print("!!!")
        df = pd.read_csv(f"{path}/{f}")
        # print(df.head())ß
        ewma = df.fillna("ffil").rolling(3).mean()
        print(ewma.head())


ewma_understats("Gabriel_Jesus", 10)
