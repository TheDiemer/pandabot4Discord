import requests, os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('DL_USERNAME')
password = os.getenv('DL_PASSWORD')


async def score(ctx):
    url = "http://duolingo.com/users/"
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

    main = session.get(url+username).json()
    friends = []
    for friend in main.get('language_data').get('de').get('points_ranking_data'):
          friends.append(friend.get('username'))

    score = {}
    score[username] = main.get('language_data',0).get('de',0).get('points',0)
    for friend in friends:
        data = session.get(url + friend).json()
        score[friend] = data.get('language_data',0).get('de',0).get('points',0)

    sortedScore = {k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}
    message = "```\n"
    for person in sortedScore:
        message += '{0}: {1}\n'.format(person, sortedScore[person])
    message += "```"
    await ctx.channel.send(message)
