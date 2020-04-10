import sys, time, emoji, os, random, requests
from tabulate import tabulate
from isTool import is_api
from dotenv import load_dotenv

load_dotenv()
dbIP = os.getenv('DB_IP')
dbUser = os.getenv('DB_USERNAME')
dbPass = os.getenv('DB_PASSWORD')


async def addIs(ctx, something, somethingelse):
    isDB = is_api(ip=dbIP, username=dbUser, password=dbPass, db='isdata')
    modMsg = f"INSERT INTO issomething values(default, '{something}', '{somethingelse}')"
    modified = isDB.modify(
        modification=modMsg
    )
    await ctx.channel.send(
        f"Thanks! {something} is now also {somethingelse}"
    )

        
async def getIs(ctx, something):
    isDB = is_api(ip=dbIP, username=dbUser, password=dbPass, db='isdata')
    isSomething = isDB.query(ask=f"SELECT * FROM issomething WHERE something = '{something}'")
    if isSomething != ():
        # Its not empty, so there is somethingelse
        # if there is only the one, just say it
        if len(isSomething) == 1:
            await ctx.channel.send(
                f"{something} is {isSomething[0].get('issomethingelse')}"
            )
        # there are multiple options
        else:
            # randomly choose one
            num = random.randint(0, len(isSomething)-1)
            chosen = isSomething[num]
            await ctx.channel.send(
                f"{something} is {chosen.get('issomethingelse')}"
            )
