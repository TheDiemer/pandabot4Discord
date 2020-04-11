import os
import discord
import random
import requests
import math
import _thread
from discord.ext import commands
from dotenv import load_dotenv
import karma
import quotes
import DL
import covid19
import isSomething

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
                selected = message.content.split()[-1:][0][:-1]
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


#@bot.command(name='clear', help='For removing an alias!      `.clear ALIAS`')
#async def clear(ctx, alias):
#   await karma.delAlias(ctx, alias)


@bot.command(name='anger', help='Be angry at people!      `.anger <Target>`')
async def anger(ctx, target):
    if target is None:
        response = "(ಠ益ಠ)ᕗ {0}".format(ctx.author)
    else:
        response = "(ಠ益ಠ)ᕗ {0}".format(target)
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
    await quotes.getQuote(ctx, target)


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

bot.run(token)
