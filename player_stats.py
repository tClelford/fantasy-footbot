import imp
from typing import Tuple
import aiohttp
from fpl import FPL
import asyncio
import sys
from tom import get_creds

async def pl():
    username, password = get_creds()
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email=username, password=password)
        user = await fpl.get_user()
        my_team = await user.get_team()
    print(my_team[0])


async def main():
    await pl()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())