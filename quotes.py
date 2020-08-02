import sys, time, emoji, os, random, requests
from tabulate import tabulate
from quoteTool import quote_api
from dotenv import load_dotenv

load_dotenv()
dbIP = os.getenv('DB_IP')
dbUser = os.getenv('DB_USERNAME')
dbPass = os.getenv('DB_PASSWORD')


async def getQuote(ctx, selected):
    quoteDB = quote_api(ip=dbIP, username=dbUser, password=dbPass, db='quotes')
    if selected:
        # If the variable is a digit then we are trying to get a SPECIFIC quote
        if selected.isdigit():
            quotes = quoteDB.query(ask=f"SELECT * FROM quotes WHERE id = '{selected}'")
            try:
                Quote = (True, quotes[0])
            except:
                Quote = (False, 'Sorry, it looks like I don\'t have that quote number in my DB!')
        # If it has content, but isnt digits, we will assume it is a name
        else:
            if '%' in selected:
                Quote = (False, 'Please try again without the % as this is a wildcard! Thank you!')
            else:
                quotes = quoteDB.query(ask=f"SELECT * FROM quotes WHERE person LIKE '%{selected}%'")
                try:
                    num = random.randint(0, len(quotes)-1)
                    Quote = (True, quotes[num])
                except:
                    Quote = (False, 'Sorry, it looks like that user doesn\'t have a quote in my DB yet!')
    # otherwise, get a random quote!
    else:
        quotes = quoteDB.query(ask='SELECT * FROM quotes')
        num = random.randint(0, len(quotes)-1)
        Quote = (True, quotes[num])

    if Quote[0]:
        await ctx.send(
                '```{0}```\n-- {1}, {2} [{3}]'.format(
                    str(Quote[1].get('quote')),
                    str(Quote[1].get('person')),
                    str(Quote[1].get('date')),
                    str(Quote[1].get('id')),
                )
        )
    else:
        await ctx.send(Quote[1])

        
async def findQuote(ctx, search, users):
    quoteDB = quote_api(ip=dbIP, username=dbUser, password=dbPass, db='quotes')
    quotes = quoteDB.query(ask=f"SELECT * FROM quotes WHERE quote LIKE '%{search}%'")
    personID = str(ctx.author.id)
    test = users.get(personID, "Empty")
    if users.get(personID, None).get('nick', None) is not None:
        user = users.get(personID).get('nick')
    else:
        user = users.get(personID).get('name')
    await ctx.send(
        f"<@!{ctx.author.id}>, I found {len(quotes)} results with that phrase: {search}"
    )
    pasteList = []
    html = '<!doctype HTML>\n<html>\n<head>\n <title>quotes!</title>\n<style>table, th, td {\n    border: 1px solid black;\n    border-collapse: collapse;\n}\nth, td {\n    padding: 5px;\n}\n</style>\n</head><body>\n <table>'
    html += '<tr><th>Person</th><th>Date</th><th>ID</th><th>Quote</th></tr>'
    for quote in quotes:
        tmp = {
            'Person': str(quote.get('person')),
            'Date': str(quote.get('date')),
            'ID': str(quote.get('id')),
            'Quote': str(quote.get('quote')),
        }
        pasteList.append(tmp)
    data = {
        'api_dev_key': 'de3799e969166e7e15767193dd7625e3',
        'api_option': 'paste',
        'api_paste_name': '{0} quotes of {1}'.format(len(quotes), search),
        'api_paste_private': '1',
        'api_paste_expire_date': '10M',
        'api_paste_code': tabulate(pasteList, headers='keys', tablefmt='fancy_grid', stralign='center'),
    }
    paste = requests.post('https://pastebin.com/api/api_post.php', data=data)
    if paste.status_code == 200:
        await ctx.send(paste.text)
    else:
        await ctx.send('Sorry! I had an issue pasting the response to pastebin.com, can you try again?')
#def change(person, column, decrement=False):
#    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
##    karmaDB = karma_api(ip=db.ip, username=db.username, password=db.password, db=db.db)
#    print(person)
#    alias = karmaDB.checkAlias(person=person[0])
#    print(alias)
#    # If it was an alias, change the person variable to match the og nick
#    if alias[0]:
#        person = (alias[1], person[1])
#    time.sleep(0.25)
#    # Checking to see if the item exists in the karma db
#    ask = "select {0} from karma where person = '{1}';".format(column, person[0])
#    existence = karmaDB.query(ask=ask)
#    if decrement:
#        value = -1
#    else:
#        value = 1
#    # If they don't insert a base data piece
#    if existence == ():
#        mod = "insert into karma (person, {0}) values('{1}' , {2});".format(column, person[0], value)
#    # Otherwise UPDATE their data
#    else:
#        mod = "UPDATE karma set {0} = {1} where person = '{2}';".format(column, str(existence[0].get(column) + value if existence[0].get(column) is not None else value), person[0])
#    modified = karmaDB.modify(modification=mod)
#    rankData = karmaDB.getRank(value=column, person=person[0])
#    return rankData
#
#
#async def karmaChange(message, userList):
#    global users
#    users = userList
#    positive = []
#    negative = []
#    shame = []
#    shade = []
#    for single in message.content.split():
#        if '++' in single:
#            positive.append(single)
#        if '--' in single:
#            negative.append(single)
#        if '~~' in single:
#            shame.append(single)
#        if '``' in single:
#            shade.append(single)
#    up = []
#    down = []
#    shameUp = []
#    shadeUp = []
#    for one in positive:
#        tmp = one.split('+')
#        while("" in tmp):
#            tmp.remove("")
#        up.append(emoji.demojize(tmp[0]))
#    for one in negative:
#        tmp = one.split('-')
#        while("" in tmp):
#            tmp.remove("")
#        down.append(emoji.demojize(tmp[0]))
#    for one in shame:
#        tmp = one.split('~')
#        while("" in tmp):
#            tmp.remove("")
#        shameUp.append(emoji.demojize(tmp[0]))
#    for one in shade:
#        tmp = one.split('`')
#        while("" in tmp):
#            tmp.remove("")
#        shadeUp.append(emoji.demojize(tmp[0]))
#    for name in up:
#        sender = str(message.author).split("#")[0]
#        person = filter(name, sender)
#        if person[0].lower() == sender.lower():
#            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#            rankData = karmaDB.getRank(value='karma', person=person[0])
#        else:
#            rankData = change(person, 'karma', decrement=False)
#        await message.channel.send(
#            '{0} has {1} points of karma (rank {2})'.format(
#                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
#                str(rankData[0].get('karma')),
#                str(rankData[0].get('rank')),
#            )
#        )
#    for name in down:
#        sender = str(message.author).split("#")[0]
#        person = filter(name, sender)
#        if person[0].lower() == sender.lower():
#            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#            rankData = karmaDB.getRank(value='karma', person=person[0])
#        else:
#            rankData = change(person, 'karma', decrement=True)
#        await message.channel.send(
#            '{0} has {1} points of karma (rank {2})'.format(
#                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
#                str(rankData[0].get('karma')),
#                str(rankData[0].get('rank')),
#            )
#        )
#    for name in shameUp:
#        sender = str(message.author).split("#")[0]
#        person = filter(name, sender)
#        if person[0].lower() == sender.lower():
#            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#            rankData = karmaDB.getRank(value='shame', person=person[0])
#        else:
#            rankData = change(person, 'shame', decrement=False)
#        await message.channel.send(
#            '{0} has {1} points of shame (rank {2})'.format(
#                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
#                str(rankData[0].get('shame')),
#                str(rankData[0].get('rank')),
#            )
#        )
#    for name in shadeUp:
#        sender = str(message.author).split("#")[0]
#        person = filter(name, sender)
#        if person[0].lower() == sender.lower():
#            karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#            rankData = karmaDB.getRank(value='shade', person=person[0])
#        else:
#            rankData = change(person, 'shade', decrement=False)
#        await message.channel.send(
#            '{0} has {1} points of shade (rank {2})'.format(
#                str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':'else rankData[0].get('person')),
#                str(rankData[0].get('shade')),
#                str(rankData[0].get('rank')),
#            )
#        )
#
#
##@commands('rank','karma','shame','shade')
##@example('rank|karma (returns highest karma) | rank|karma <Name> (returns person\'s karma rank) | same for the others but for shame or shade')
##def checkRank(bot, trigger):
##    thing = 0
##    for channel in channelList:
##        if channel in trigger.sender:
##            thing+=1
##        else:
##            pass
##    if thing > 0:
##        # Make sure the trigger Actually matches one of these so I can just use that directly as the value
##        if (trigger.group(1) == 'karma') or (trigger.group(1) == 'rank') or (trigger.group(1) == 'shade') or (trigger.group(1) == 'shame'):
##            karmaDB = karma_api(ip=db.ip, username=db.username, password=db.password, db=db.db)
##            if trigger.group(1) == 'rank':
##                value = 'karma'
##            else:
##                value = trigger.group(1)
##            # if no one is specified, get the min/max
##            if trigger.group(3) is None:
##                highest = karmaDB.getRank(value=value)
##                if len(highest) > 1:
##                    # do a thing
##                    people = []
##                    for one in highest:
##                        people.append(one.get('person'))
##                    if len(people) > 2:
##                        peoplemsg = "{0}, and {1}".format(', '.join(people[:-1]), people[-1])
##                    else:
##                        peoplemsg = "{0} and {1}".format(people[0], people[1])
##                    bot.say('{0} have the most {1} with {2} points'.format(peoplemsg, value, highest[0].get(value)))
##                else:
##                    bot.say('{0} has the most {1} with {2} points'.format(highest[0].get('person'), value, highest[0].get(value)))
##            else:
##                rankData = karmaDB.getRank(value=value, person=trigger.group(3))
##                bot.say(
##                    "{0} has {1} points of {2} (rank {3})".format(
##                        str(emoji.emojize(rankData[0].get('person')) if rankData[0].get('person')[0] == ':' else rankData[0].get('person')),
##                        str(rankData[0].get(value)),
##                        value,
##                        str(rankData[0].get('rank')),
##                    )
##                )
##
##
#async def addAlias(ctx, alias, target, userList):
#    global users
#    users = userList
#    newAlias = emoji.demojize(alias)
#    name = emoji.demojize(target)
#    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#    alias = karmaDB.query(ask="select * from alias where person = '{0}';".format(name))
#    # This is the person's first alias!
#    if alias == ():
#        modified = karmaDB.modify(
#            modification="INSERT INTO alias values('{0}', '{1}');".format(
#                name,
#                newAlias,
#            )
#        )
#    # adding to their alias list
#    else:
#        alii = alias[0].get('alias')
#        new = alii + ' ' + newAlias
#        modified = karmaDB.modify(
#            modification="UPDATE alias SET alias = '{0}' where person = '{1}';".format(
#                new,
#                name,
#            )
#        )
#    await ctx.send("Thanks! {0} is now also know as {1}!".format(
#            emoji.emojize(name),
#            emoji.emojize(newAlias),
#        )
#    )
#
#
#async def delAlias(ctx, alias, userList):
#    global users
#    users = userList
#    removeAlias = emoji.demojize(alias)
#    print(removeAlias)
#    karmaDB = karma_api(ip=dbIP, username=dbUser, password=dbPass, db='karma')
#    data = karmaDB.query(ask="select * from alias where alias REGEXP '(?(?=(.|\n|\r|\r\n)) ?|){0}(?(?=(.|\n|\r|\r\n)) |)';".format(removeAlias))
#    print('this data:{0}'.format(data))
#    # This alias doesn't exist for anyone
#    if data == ():
#        await ctx.send("Well that was easy! No one was aliased to {0}".format(removeAlias))
#    else:
#        # lets make sure we get the ACTUAL person
#        personSpot = -1
#        broken = False
#        for people in data:
#            print(people)
#            for alii in people.get("alias").split():
#                print(removeAlias.lower())
#                print(alii.lower())
#                if removeAlias.lower() == alii.lower():
#                    broken = True
#                    print(broken)
#                    break
#            if broken:
#                break
#            personSpot += 1
#        if broken == False:
#            await ctx.send("Well that was easy! No one was aliased to {0}".format(removeAlias))
#            sys.exit(1)
#        aliasList = data[personSpot].get("alias").split()
#        aliasList.remove(removeAlias)
#        # That was their LAST alias! So just delete it all
#        if aliasList == []:
#            mod = "delete from alias where person = '{0}'".format(
#                    data[personSpot].get("person")
#            )
#        else:
#            mod = "UPDATE alias SET alias = '{0}' where person = '{1}'".format(
#                    ' '.join(aliasList),
#                    data[personSpot].get("person"),
#            )
#        karmaDB.modify(modification=mod)
#        await ctx.send("Alright! {0} will no longer be known as {1}!".format(
#                data[personSpot].get("person"),
#                alias,
#            )
#        )
##
##
##@commands('getalias','aliaswho')
##@example('.getalias jonesin | .aliaswho gregR')
##def getAlias(bot, trigger):
##    thing = 0
##    for channel in channelList:
##        if channel in trigger.sender:
##            thing+=1
##        else:
##            pass
##    if thing > 0:
##        if trigger.group(3) is None:
##            bot.reply('Whose aliiii do you wanna see?')
##        else:
##            karmaDB = karma_api(ip=db.ip, username=db.username, password=db.password, db=db.db)
##            data = karmaDB.query(ask="select * from alias where person = '{0}';".format(trigger.group(3)))
##            if data == ():
##                bot.reply('Sorry, that person doesn\'t appear to have any alii! Feel free to give them their first with .alias!')
##            else:
##                alii = data[0].get('alias').split()
##                if len(alii) > 2:
##                    aliimsg = "{0}, and {1}".format(', '.join(alii[:-1]), alii[-1])
##                elif len(alii) == 2:
##                    aliimsg = "{0} and {1}".format(alii[0], alii[1])
##                else:
##                    aliimsg = alii[0]
##                message = "{0} is also known as {1}".format(
##                    data[0].get('person'),
##                    aliimsg,
##                )
##                if len(message) > 385:
##                    messageParts = []
##                    times = int(len(message)/385)
##                    placeHolder = 0
##                    while placeHolder <= times:
##                        messageParts.append(message[(placeHolder*385):((placeHolder+1)*385)])
##                        placeHolder += 1
##                    bot.reply(messageParts[0])
##                    for part in messageParts[1:]:
##                        bot.say(part)
##                else:
##                    bot.say(message)
