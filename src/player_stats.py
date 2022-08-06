from operator import ge
from typing import Dict, List
import pandas as pd
import aiohttp
from fpl import FPL
import asyncio
from tom import get_creds

def break_the_bloody_async_chain(async_func):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_func)
    return result


async def get_current_team(username, password)-> List[Dict]:
     async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email=username, password=password)
        user = await fpl.get_user()
        my_team = await user.get_team()
        return my_team


async def all_players_to_csv(username, password)-> None:
     async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
       # await fpl.login(email=username, password=password)
        players = await fpl.get_players()
        dics = [vars(p) for p in players]
        df = pd.DataFrame(dics)
        df.to_csv("./data/all_players_w1.csv")

username, password = get_creds()
break_the_bloody_async_chain(get_current_team(username, password))