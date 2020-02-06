import requests, os, datetime
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
username = os.getenv('DL_USERNAME')
password = os.getenv('DL_PASSWORD')


def login():
    session = requests.Session()
    login_url = "https://www.duolingo.com/login"
    data = {"login": username, "password":password}
    tries = 0
    while tries < 5:
        attempt = session.post(login_url, data).json()
        if attempt.get('response') == 'OK':
            break
        else:
            tries += 1
    if attempt.get('response') != 'OK':
        sys.exit()
    return session


async def daily(ctx):
    url = "http://duolingo.com/users/"
    authed = login()
    main = authed.get(url+username).json()
    friends = []
    for friend in main.get('language_data').get('de').get('points_ranking_data'):
        friends.append(friend.get('username'))

    UTCnow = datetime.datetime.now() 
    unformattedNow = UTCnow - datetime.timedelta(hours=5)
    now = unformattedNow.strftime("%m/%d/%Y")
    daily = {}
    users = []
    for friend in friends:
        data = authed.get(url + friend).json()
        users.append(data)

    for user in users:
        for day in user['calendar']:
            tempDate = datetime.datetime.fromtimestamp(day["datetime"] /1e3)
            newTemp = tempDate.strftime("%m/%d/%Y")
            if newTemp == now:
                if daily.get(user.get('username'), None) is None:
                    daily[user.get('username')] = int(day['improvement'])
                else:
                    tmp = int(daily.get(user.get('username')))
                    tmp += int(day['improvement'])
                    daily[user.get('username')] = tmp
    sortedDaily = {k: v for k, v in sorted(daily.items(), key=lambda item: item[1], reverse=True)}
    message = "**Leaderboard for %s** \n>>> " % now
    for person in sortedDaily:
        message += '{0}: {1}\n'.format(person, sortedDaily[person])
    await ctx.channel.send(message)


async def score(ctx):
    url = "http://duolingo.com/users/"
    authed = login()
    main = authed.get(url+username).json()
    friends = []
    for friend in main.get('language_data').get('de').get('points_ranking_data'):
        friends.append(friend.get('username'))

    mainLang = main.get("learning_language")
    score = {}
    score[username] = main.get('language_data',0).get(mainLang,0).get('points',0)
    for friend in friends:
        data = authed.get(url + friend).json()
        try:
            friendLang = data.get('learning_language')
            score[friend] = data.get('language_data',0).get(friendLang,0).get('points',0)
        except:
            score[friend] = 0

    sortedScore = {k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
    # Lets make the message!
    # TABLES
    message = "**Leaderboard** \n```css\n"
    names = []
    score = []
    data = {}
    for person in sortedScore:
        names.append(person)
        score.append(sortedScore[person])
    data['Name'] = names
    data['Score'] = score
    message += tabulate(data, headers="keys",tablefmt="fancy_grid", stralign="center",numalign="center")
    message += "```"

    ## Makes the text yellow/orange but leaves score white
    #message = "**Leaderboard** \n```apache\n"
    #for person in sortedScore:
    #    message += '{0}: {1}\n'.format(person, sortedScore[person])
    #message += "```"
    
    ## Makes an inline code block (looks good)
    #message = "**Leaderboard** \n>>> "
    #for person in sortedScore:
    #    message += '{0}: {1}\n'.format(person, sortedScore[person])
    await ctx.channel.send(message)
