import requests, os, datetime
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
username = os.getenv('DL_USERNAME')
password = os.getenv('DL_PASSWORD')


def login():
    # Starting a http session so we can get/keep cookies and headers
    session = requests.Session()
    login_url = "https://www.duolingo.com/login"
    data = {"login": username, "password":password}
    tries = 0
    # Want to provide a window for this to fail and quit eventually but if we just hit some network hiccup I don't want it to die completely on the first failed attempt.
    while tries < 5:
        attempt = session.post(login_url, data).json()
        # Assuming we logged in properly lets break out and move on
        if attempt.get('response') == 'OK':
            break
        # Otherwise keep trying
        else:
            tries += 1
    # If it failed to login at all! Lets quit
    if attempt.get('response') != 'OK':
        sys.exit()
    # Now lets hand this logged in session Back to the function that called it
    return session


async def message(ctx, sortedData, content):
    # The Users will go here
    names = []
    # Their scores go in here
    score = []
    # And this is where we will connect the dots!
    data = {}
    for person in sortedData:
        names.append(person)
        score.append(sortedData[person])
    data['Name'] = names
    data['Score'] = score
    # Now we are generating a Table with the Names and Scores as the data!
    content += tabulate(data, headers="keys",tablefmt="fancy_grid", stralign="center",numalign="center")
    # And to close out the code block
    content += "```"

    ## For the yellow/orange text with white score from apache
    #for person in sortedData:
    #    content += '{0}: {1}\n'.format(person, sortedData[person])
    #content += "```"

    ## For the inline code block
    #for person in sortedData:
    #    content += '{0}: {1}\n'.format(person, sortedData[person])

    # And to send the data into the channel!
    await ctx.channel.send(content)


# Getting the DAILY score
async def daily(ctx):
    # Set the DL url we will use
    url = "http://duolingo.com/users/"
    # go get a session to do things with
    authed = login()
    # Get MY data
    main = authed.get(url+username).json()

    # Getting my learning language (so if we move on from German it isn't stuck looking at that!
    mainLang = main.get("learning_language")
    friends = []
    # Parse through data to find my Friends' usernames
    for friend in main.get('language_data').get(mainLang).get('points_ranking_data'):
        friends.append(friend.get('username'))

    # Now identifying UTC right now
    UTCnow = datetime.datetime.now() 
    # Changing it to EST (so "today" doesn't end 5 hours earlier than it should)
    unformattedNow = UTCnow - datetime.timedelta(hours=5)
    # Format it for comparison
    now = unformattedNow.strftime("%m/%d/%Y")
    daily = {}
    users = []
    # Now we are gonna go get all of my friends' data!
    for friend in friends:
        data = authed.get(url + friend).json()
        users.append(data)

    # Looping through each friend
    for user in users:
        # we are gonna look at Each calender entry (each entry is a score update, not necessarily a day but that was easier for writing the code)
        for day in user['calendar']:
            # Formatting the date string
            tempDate = datetime.datetime.fromtimestamp(day["datetime"] /1e3)
            newTemp = tempDate.strftime("%m/%d/%Y")
            # So if the date is Today then lets do things with it!
            if newTemp == now:
                # If that user Doesn't have any score entered yet
                if daily.get(user.get('username'), None) is None:
                    # Then lets just set it as this data point
                    daily[user.get('username')] = int(day['improvement'])
                # Otherwise
                else:
                    # Lets get the current value
                    tmp = int(daily.get(user.get('username')))
                    # Add this new data point to it
                    tmp += int(day['improvement'])
                    # Reset the user's value to the NEW value
                    daily[user.get('username')] = tmp

    # Sort it!!! The person with the highest score should be at the top!
    sortedDaily = {k: v for k, v in sorted(daily.items(), key=lambda item: item[1], reverse=True)}

    # Tables
    content = "**Leaderboard for %s** \n```css\n" % now

    ## Makes the text yellow/orange but leaves score white
    #content = "**Leaderboard** \n```apache\n"
    
    ## Makes an inline code block (looks good)
    #content = "**Leaderboard** \n>>> "

    # Now lets hand things off to actually finish the message and Send it!
    await message(ctx, sortedDaily, content)


async def score(ctx):
    # Set the DL url we will use
    url = "http://duolingo.com/users/"
    # go get a session to do things with
    authed = login()
    # Get MY Data
    main = authed.get(url+username).json()
    # Getting my learning language (so if we move on from German it isn't stuck looking at that!
    mainLang = main.get("learning_language")
    friends = []
    # Parse through my data to find my Friends' usernames
    for friend in main.get('language_data').get(mainLang).get('points_ranking_data'):
        friends.append(friend.get('username'))

    score = {}
    # Now to get my overall score for the language I am learning!
    score[username] = main.get('language_data',0).get(mainLang,0).get('points',0)
    # Looping through each friend
    for friend in friends:
        # Getting their data
        data = authed.get(url + friend).json()
        # Putting this into a try JUST incase something fails I can set them to 0 as a safety net
        try:
            # get their language. This is so they can learn Any language they want and still compete!
            friendLang = data.get('learning_language')
            # Now to GET their score and associate it with their name!
            score[friend] = data.get('language_data',0).get(friendLang,0).get('points',0)
        except:
            score[friend] = 0

    # Sort it!!! The person with the highest score should be at the top!
    sortedScore = {k: v for k, v in sorted(score.items(), key=lambda item: item[1], reverse=True)}

    # TABLES
    content = "**Leaderboard** \n```css\n"

    ## Makes the text yellow/orange but leaves score white
    #content = "**Leaderboard** \n```apache\n"
    
    ## Makes an inline code block (looks good)
    #content = "**Leaderboard** \n>>> "

    # Now lets hand things off to actually finish the message and Send it!
    await message(ctx, sortedScore, content)
