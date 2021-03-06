import sys, time, emoji, os
from karmaTool import karma_api
from dotenv import load_dotenv

load_dotenv()
dbIP = os.getenv('DB_IP')
dbUser = os.getenv('DB_USERNAME')
dbPass = os.getenv('DB_PASSWORD')


def filter(name, sender):
    if '<@' in name:
        person = name.split('<@')[1]
        if person[0] == '!':
            person = person[1:]
        print(person)
        user = users.get(person.split('>')[0])
        try:
            if user.get('nick', None):
                person = (user.get('nick'), False)
            else:
                person = (user.get('name'), False)
        except:
            person = (name, False)
    elif name.lower() == 'me':
        person = (sender, True)
    else:
        person = (name, False)
    return person


def change(person, column, decrement=False):
    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#    karmaDB = karma_api(ip=db.ip, username=db.username, password=db.password, db=db.db)
    print(person)
    alias = karmaDB.checkAlias(person=person[0])
    print(alias)
    # If it was an alias, change the person variable to match the og nick
    if alias[0]:
        person = (alias[1], person[1])
    time.sleep(0.25)
    # Checking to see if the item exists in the karma db
    ask = "select {0} from karma where person = '{1}';".format(column, person[0])
    existence = karmaDB.query(ask=ask)
    if decrement:
        value = -1
    else:
        value = 1
    # If they don't insert a base data piece
    if existence == ():
        mod = "insert into karma (person, {0}) values('{1}' , {2});".format(column, person[0], value)
    # Otherwise UPDATE their data
    else:
        mod = "UPDATE karma set {0} = {1} where person = '{2}';".format(column, str(existence[0].get(column) + value if existence[0].get(column) is not None else value), person[0])
    modified = karmaDB.modify(modification=mod)
    rankData = karmaDB.getRank(value=column, person=person[0])
    return rankData


async def karmaChange(message, userList):
    global users
    users = userList
    positive = []
    negative = []
    shame = []
    shade = []
    for single in message.content.split():
        if '++' in single:
            positive.append(single)
        if '--' in single:
            negative.append(single)
        if '~~' in single:
            shame.append(single)
        if '``' in single:
            shade.append(single)
    print(f"positive: {positive}")
    print(f"negative: {negative}")
    print(f"shame: {shame}")
    print(f"shade: {shade}")
    up = []
    down = []
    shameUp = []
    shadeUp = []
    for one in positive:
        if one[0] == '+':
            pass
        else:
            tmp = one.split('+')
            while("" in tmp):
                tmp.remove("")
            up.append(emoji.demojize(tmp[0]))
    for one in negative:
        if one[0] == '-':
            pass
        else:
            tmp = one.split('-')
            while("" in tmp):
                tmp.remove("")
            print(f"tmp: {tmp}")
            down.append(emoji.demojize(tmp[0]))
    for one in shame:
        if one[0] == '~':
            pass
        else:
            tmp = one.split('~')
            while("" in tmp):
                tmp.remove("")
            shameUp.append(emoji.demojize(tmp[0]))
    for one in shade:
        if one[0] == '`':
            pass
        else:
            tmp = one.split('`')
            while("" in tmp):
                tmp.remove("")
            shadeUp.append(emoji.demojize(tmp[0]))
    for name in up:
        sender = str(message.author).split("#")[0]
        person = filter(name, sender)
        if person[0].lower() == sender.lower():
            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
            rankData = karmaDB.getRank(value='karma', person=person[0])
        else:
            rankData = change(person, 'karma', decrement=False)
        await message.channel.send(
            '{0} has {1} points of karma (rank {2})'.format(
                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
                str(rankData[0].get('karma')),
                str(rankData[0].get('rank')),
            )
        )
    for name in down:
        sender = str(message.author).split("#")[0]
        person = filter(name, sender)
        if person[0].lower() == sender.lower():
            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
            rankData = karmaDB.getRank(value='karma', person=person[0])
        else:
            rankData = change(person, 'karma', decrement=True)
        await message.channel.send(
            '{0} has {1} points of karma (rank {2})'.format(
                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
                str(rankData[0].get('karma')),
                str(rankData[0].get('rank')),
            )
        )
    for name in shameUp:
        sender = str(message.author).split("#")[0]
        person = filter(name, sender)
        if person[0].lower() == sender.lower():
            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
            rankData = karmaDB.getRank(value='shame', person=person[0])
        else:
            rankData = change(person, 'shame', decrement=False)
        await message.channel.send(
            '{0} has {1} points of shame (rank {2})'.format(
                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
                str(rankData[0].get('shame')),
                str(rankData[0].get('rank')),
            )
        )
    for name in shadeUp:
        sender = str(message.author).split("#")[0]
        person = filter(name, sender)
        if person[0].lower() == sender.lower():
            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
            rankData = karmaDB.getRank(value='shade', person=person[0])
        else:
            rankData = change(person, 'shade', decrement=False)
        await message.channel.send(
            '{0} has {1} points of shade (rank {2})'.format(
                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
                str(rankData[0].get('shade')),
                str(rankData[0].get('rank')),
            )
        )


#@commands('rank','karma','shame','shade')
#@example('rank|karma (returns highest karma) | rank|karma <Name> (returns person\'s karma rank) | same for the others but for shame or shade')
#def checkRank(bot, trigger):
#    thing = 0
#    for channel in channelList:
#        if channel in trigger.sender:
#            thing+=1
#        else:
#            pass
#    if thing > 0:
#        # Make sure the trigger Actually matches one of these so I can just use that directly as the value
#        if (trigger.group(1) == 'karma') or (trigger.group(1) == 'rank') or (trigger.group(1) == 'shade') or (trigger.group(1) == 'shame'):
#            karmaDB = karma_api(ip=db.ip, username=db.username, password=db.password, db=db.db)
#            if trigger.group(1) == 'rank':
#                value = 'karma'
#            else:
#                value = trigger.group(1)
#            # if no one is specified, get the min/max
#            if trigger.group(3) is None:
#                highest = karmaDB.getRank(value=value)
#                if len(highest) > 1:
#                    # do a thing
#                    people = []
#                    for one in highest:
#                        people.append(one.get('person'))
#                    if len(people) > 2:
#                        peoplemsg = "{0}, and {1}".format(', '.join(people[:-1]), people[-1])
#                    else:
#                        peoplemsg = "{0} and {1}".format(people[0], people[1])
#                    bot.say('{0} have the most {1} with {2} points'.format(peoplemsg, value, highest[0].get(value)))
#                else:
#                    bot.say('{0} has the most {1} with {2} points'.format(highest[0].get('person'), value, highest[0].get(value)))
#            else:
#                rankData = karmaDB.getRank(value=value, person=trigger.group(3))
#                bot.say(
#                    "{0} has {1} points of {2} (rank {3})".format(
#                        str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':' else rankData[0].get('person')),
#                        str(rankData[0].get(value)),
#                        value,
#                        str(rankData[0].get('rank')),
#                    )
#                )
#
#
async def addAlias(ctx, alias, target, userList):
    global users
    users = userList
    newAlias = emoji.demojize(alias)
    name = emoji.demojize(target)
    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
    alias = karmaDB.query(ask="select * from alias where alias = '{0}';".format(newAlias))
    # this alias was not already in the db
    if alias == ():
        modified = karmaDB.modify(
            modification="INSERT INTO alias values('{0}', '{1}');".format(
                name,
                newAlias,
            )
        )
        await ctx.send("Thanks! {0} is now also known as {1}!".format(
                emoji.emojize(name),
                emoji.emojize(newAlias),
            )
        )
    # a nick already has this alias
    else:
        await ctx.send("Thanks! But {0} was already known as {1}!".format(
                emoji.emojize(alias[0].get("person")),
                emoji.emojize(newAlias),
            )
        )


async def delAlias(ctx, alias, userList):
    global users
    users = userList
    removeAlias = emoji.demojize(alias)
    print(removeAlias)
    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
    data = karmaDB.query(ask="select * from alias where alias =  '{0}';".format(removeAlias))
    print('this data:{0}'.format(data))
    # This alias doesn't exist for anyone
    if data == ():
        await ctx.send("Well that was easy! No one was aliased to {0}".format(removeAlias))
    else:
        mod = "delete from alias where alias = '{0}';".format(removeAlias)
        karmaDB.modify(modification=mod)
        await ctx.send("Alright! {0} will no longer be known as {1}!".format(
                data[0].get("person"),
                alias,
            )
        )


async def getAlias(ctx, name):
    name = emoji.demojize(name)
    print(name)
    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
    data = karmaDB.query(ask="select * from alias where person = '{0}';".format(name))
    if data == ():
        data2 = karmaDB.query(ask="select * from alias where alias = '{0}';".format(name))
        if data2 == ():
            await ctx.send('Sorry, that person doesn\'t appear to have any alii! (Nor is it an alias) Feel free to give them their first with .alias!')
        else:
            message = "That doesn't *have* any alii, but it *is* one! {0} is an alias for {1}".format(name, data2[0].get("person"))
            await ctx.send(message)
    else:
        alii = []
        for resp in data:
            alii.append(resp.get("alias"))
        if len(alii) > 2:
            aliimsg = "{0}, and {1}".format(', '.join(alii[:-1]), alii[-1])
        elif len(alii) == 2:
            aliimsg = "{0} and {1}".format(alii[0], alii[1])
        else:
            aliimsg = alii[0]
        message = "{0} is also known as {1}".format(
            data[0].get('person'),
            aliimsg,
        )
        await ctx.send(message)
