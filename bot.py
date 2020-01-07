import os
import discord
import random
import requests
from discord.ext import commands
from dotenv import load_dotenv
import karma

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
             users[tmp.id] = {'name': tmp.name, 'discriminator': tmp.discriminator, 'nick': tmp.nick}
         except StopIteration:
             print('Done! Check out the users dict')
             break
    print(users)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'test' in message.content.lower():
        await message.channel.send('Bingpot!')
    if '--' in message.content or '++' in message.content or '~~' in message.content or '``' in message.content:
        #if '<@!' in message.content:
        #    user = message.content.split('<@!')[1].split('>')[0]
        #    print(user)
        #    print(users.get(int(user)))
        #print(message.content.split('++')[0].split('!')[1])
        #a = await bot.fetch_user(int(message.content.split('++')[0].split('!')[1]))
        #print(a.username)
        await karma.karmaChange(message, users)

    await bot.process_commands(message)


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


@bot.command(name='test', help='This is a testing command.      `.test`')
async def test(ctx):
    print("context:{0}".format(ctx))
    await ctx.send('Bingpot!')


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
