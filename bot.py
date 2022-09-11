import os
import nextcord
import random
import requests
import math
import _thread
from nextcord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import time
import karma
import quotes
import DL
import covid19
import isSomething
from questionsTool import questions_api

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='.')

global users
users = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    userList = bot.get_all_members()
    while True:
         try:
             tmp = next(userList)
             users[str(tmp.id)] = {'name': tmp.name, 'discriminator': tmp.discriminator, 'nick': tmp.nick}
         except StopIteration:
             break
    print(users)

@bot.command(name="new_question", help="")
async def add_questions(ctx, question, channel=""):
    if ctx.author == os.getenv("OWNER"):
        dbIP = os.getenv('DB_IP')
        dbUser = os.getenv('DB_USERNAME')
        dbPass = os.getenv('DB_PASSWORD')
        questionsDB = questions_api(ip=dbIP, username=dbUser, password=dbPass, db="questions")
        mod = 'insert into existential values(default, "{0}", "{1}", false'.format(question.replace("'", "\\'"), channel.replace("'", "\\'"))
        questionsDB.modify(modification=mod)
        await ctx.send("question Added!")

async def daily_question():
    channels = {
        '#dnd': 654446991912206346,
        '#general-gaming': 654753999907586058,
        '#ac': 707272408645632020,
        '#borderlands': 707272479101550684,
        '#among-us': 760698098686885888,
        '#themueller': 654497924121755661,
        '#nack': 654447029925183498,
        '#rdu': 655119793472405505,
        '#hannibal': 655119856303210522,
        '#talkingtech': 659770298803159051,
        '#music': 681942244076421128,
        '#capslock': 667775102951227413,
        '#corona': 688492183275438134,
        '#polyglots': 672449279851364369,
        '#werk': 655059635199541260,
        '#code': 697907185618780271,
        '#pet_friends': 713519629250592891,
        '#trees': 654824088124129288,
        '#homeimprovement': 718124248803180604,
        '#cars': 728014796620038184,
        '#filmevision': 740442658367078461,
        '#whatsthesubject': 667014858004496417,
        '#storytellers': 737397728631324792,
        '#starwars': 738097758480760853,
        '#damnit': 778744161317683283,
        '#general': 654446795077976090,
        '#emoji': 707607654746554459,
        '#bots': 655092075389517894,
        '#council-chambers': 656269116092710918,
    }
    await asyncio.sleep(10)
    while True:
        now = datetime.strftime(datetime.now(), '%H')
        print(f"the time loop starts now: {now}")
        if now == os.getenv("SEND_TIME"):
            dbIP = os.getenv('DB_IP')
            dbUser = os.getenv('DB_USERNAME')
            dbPass = os.getenv('DB_PASSWORD')
            questionsDB = questions_api(ip=dbIP, username=dbUser, password=dbPass, db="questions")
            ask = "select * from existential where asked = 0;"
            data = questionsDB.query(ask=ask)
            if data == ():
                # tell me its empty and do nothing else
                pass
            else:
                num = random.randint(0, len(data)-1)
                question = "Hey <@&788466685199908897>, "
                question += data[num].get("question")
                channel = channels.get(data[num].get("channel"))
                if channel is not None:
                    channel = bot.get_channel("#" +str(channels.get(channel)))
                else:
                    channel = bot.get_channel(channels.get("#nack"))
                print(f"printing channel {channel} to know where this should go")
                try:
                    await channel.send(question)
                except AttributeError:
                    channel = bot.get_channel(channels.get("#nack"))
                    await channel.send(question)
                # now to update the DB to say we asked that question
                mod = "UPDATE existential set asked = 1 where id = {0}".format(data[num].get("id"))
                questionsDB.modify(modification=mod)
                # I also want to, periodically, send a secondary ping to remind people to give me their questions
                ran = random.randint(0,250)
                # This should mean AROUND a third of the time, it'll do things
                if ran%3 == 0:
                    channel.send("Hey, please send jonesin your questions to help keep this going!")
            # If it IS the time, lets reset for a day
            time = 86400
        else:
            # Otherwise, lets check again in an hour!
            time = 3600
        # now lets wait this thread for the given time
        await asyncio.sleep(time)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #if 'test' in message.content.lower():
     #   await message.channel.send('Bingpot!')
    if '--' in message.content or '++' in message.content or '~~' in message.content or '``' in message.content:
        await karma.karmaChange(message, users)
    if ' is ' in message.content:
        # time to make sure it was directed at pandabot
        words = message.content.split()
        print(words)
        try:
            user = words[0].split('@')[1]
        except:
            user = ''
        person = users.get(user[1:][:-1])
        person2 = users.get(user[:-1])
        if person is not None:
            if person.get('name','') == 'pandabot':
                things = message.content.split(words[0])[1].split(' is ')
                print(f"I found that |{things[0][1:]}| is |{things[1]}|")
                # NOTE that things[0] needs to trim the FIRST character
                # things[0][1:]
                await isSomething.addIs(message, things[0][1:], things[1])
            else:
                pass
        elif person2 is not None:
            if person2.get('name','') == 'pandabot':
                things = message.content.split(words[0])[1].split(' is ')
                print(f"I found that |{things[0][1:]}| is |{things[1]}|")
                # NOTE that things[0] needs to trim the FIRST character
                # things[0][1:]
                await isSomething.addIs(message, things[0][1:], things[1])
            else:
                pass
        else:
            pass
    if message.content[-1:] == '?':
        # time to make sure it was directed at pandabot
        words = message.content.split()
        try:
            user = words[0].split('@')[1]
        except:
            user = ''
        person = users.get(user[1:][:-1])
        person2 = users.get(user[:-1])
        if person is not None:
            if person.get('name') == 'pandabot':
                print(message.content)
                #selected = message.content.split()[-1:][0][:-1]
                selected = " ".join(message.content.split()[1:])[:-1]
                print(selected)
                await isSomething.getIs(message, selected)
        elif person2 is not None:
            if person2.get('name') == 'pandabot':
                selected = message.content.split()[-1:][0][:-1]
                await isSomething.getIs(message, selected)


    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, Welcome to Mad Hatters! Most of the roles you see on the server are things you can either add yourself or ask in the channel to get added to! We primarily use them for highlights! Feel free to explore and use #nack to ask questions!!!"
    )
    users[member.id] = {'name': member.name, 'discriminator': member.discriminator, 'nick': member.nick}
    print(f"Added {member.name} to the user list")

@bot.command(name='score', help='For checking in on the score for our Team! Add `daily` afterwards to get the days scores')
async def duolingoScore(ctx, target=None):
    print(ctx.message.channel)
    if str(ctx.message.channel) == 'polyglots':
        print('made it here')
        if target is None:
            await DL.score(ctx)
            #_thread.start_new_thread(await DL.score, (ctx,))
        elif target.lower() == 'daily':
            await DL.daily(ctx)
            #_thread.start_new_thread(DL.daily, (ctx,))


@bot.command(name='covid19', help='For checking in on covid19.')
async def covidCheck(ctx, location=None):
    await covid19.covid(ctx, location)


@bot.command(name='alias', help='For making someone known as something else!      `.alias ALIAS OG_NICK`')
async def alias(ctx, alias, nick):
    await karma.addAlias(ctx, alias, nick, users)


@bot.command(name='clear', help='For removing an alias!      `.clear ALIAS`')
async def clear(ctx, alias):
   await karma.delAlias(ctx, alias, users)


@bot.command(name='getalias', help='What is the full list of aliases for the given name? `.getalias nick`')
async def getalias(ctx, name):
    await karma.getAlias(ctx, name)


@bot.command(name='anger', help='Be angry at people!      `.anger <Target>`')
async def anger(ctx, target=None):
    if target is None:
        response = "(ಠ益ಠ)ᕗ {0}".format(ctx.author)
    else:
        response = "(ಠ益ಠ)ᕗ {0}".format(target)
    await ctx.send(response)

@bot.command(name="beans", help="Share beans with someone.     .beans !target!")
async def beans(ctx, target=None):
    urls = {
        0: "https://farm1.static.flickr.com/224/509478598_606e6a436d_o.jpg",
        1: "https://i.redd.it/bcykiuff3lz41.jpg",
        2: "https://i.redd.it/ne6jt50jwra61.jpg",
    }
    if target is None:
        response = f"Hey {ctx.author}, {urls.get(random.randint(0,1000000)%3)}"
    else:
        response = f"Hey {target}, {urls.get(random.randint(0,1000000)%3)}"
    await ctx.send(response)

@bot.command(name='quorum', help='This is to decide if quorum has been made.      `.quorum <yes> <members>`')
async def quorum(ctx, yes=0, members=0):
    quorumCalc = math.floor(members/2) + 1
    if yes >= quorumCalc:
        await ctx.send('Quorum is met!')
    else:
        await ctx.send(f"No quorum! {quorumCalc} of {members} must agree!")


@bot.command(name='test', help='This is a testing command.      `.test`')
async def test(ctx):
    print("context:{0}".format(ctx))
    await ctx.send('Bingpot!')


@bot.command(name='quote', help='For quote things!')
async def quote(ctx, target=None):
    await ctx.send('This has been deprecated, please use /quotes instead!')
    # await quotes.getQuote(ctx, target)


@bot.command(name='findquote', help='Find quotes with the searchword')
async def findQuote(ctx, search):
    await quotes.findQuote(ctx, search, users)

@bot.command(name='roll', help='For rolling Dice.      `.roll number_of_dice number_of_sides`')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    if len(dice) > 1:
        response = ' + '.join(dice)
        total = 0
        for die in dice:
            total += int(die)
        response += ' = {}'.format(total)
    else:
        response = ', '.join(dice)
    await ctx.send(response)


def get_xkcd(number=None):
    if number:
        url = 'https://xkcd.com/{}/info.0.json'.format(number)
    else:
        url = 'https://xkcd.com/info.0.json'
    data = requests.get(url).json()
    data['url'] = 'https://xkcd.com/' + str(data['num'])
    return data

@bot.command(name='xkcd', help='Get a link for xkcd!      `.xkcd`')
async def xkcd(ctx):
    latest = get_xkcd()
    maxInt = latest['num']
    random.seed()
    response = get_xkcd(random.randint(1, maxInt + 1))
    await ctx.send(response.get('url','Sorry, I had a problem :frown:'))

bot.loop.create_task(daily_question())

bot.run(token)
