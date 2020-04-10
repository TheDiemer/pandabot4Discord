import requests, datetime


#async def covid(message):
#    try:
#        data = requests.get(
#            "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/cases_time_v3/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Report_Date_String%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true"
#        )
#        print(f"data requests status: {data.status_code}")
#        if data.status_code == 200:
#            confirmed = (
#                data.json().get("features")[-1].get("attributes").get("Total_Confirmed")
#            )
#            recovered = (
#                data.json().get("features")[-1].get("attributes").get("Total_Recovered")
#            )
#            date = (
#                data.json().get("features")[-1].get("attributes").get("Report_Date_String")
#            )
#            await message.channel.send(
#                f"```css\nAs of {date}, there are {confirmed} confirmed cases and {recovered} total recoveries.\n```"
#            )
#        else:
#            print(f"issue getting the data: {data.status_code}\noutput: {data.text}")
#            # pm a failure
#    except Exception as e:
#        print(f"issue making the call at all: {e}")
#        # pm a failure

async def covid(message, location):
    now = datetime.datetime.now()
    if datetime.datetime.strftime(now, "%H:%M") >= "23:59":
        fileDate = "{0}".format(datetime.datetime.strftime(now, "%m-%d-%Y"))
    else:
        yesterday = now - datetime.timedelta(days=1)
        fileDate = "{0}".format(datetime.datetime.strftime(yesterday, "%m-%d-%Y"))
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{0}.csv'.format(fileDate)
    print(url)
    #try:
    r = requests.get(url, verify=False)
    if r.status_code == 200:
        # split by newline
        lines = r.text.splitlines()
        # now split by comma
        rows = []
        for b in lines:
            rows.append(b.split(','))
        # now to fix any stupid EXTRA commas, like "Korea, South"
        data = []
        for entry in rows:
            combined = False
            tmprow = []
            for place in range(0,len(entry)):
                tmp = ""
                if combined:
                    combined = False
                    pass
                else:
                    if place < len(entry)-2:
                        if '"' in entry[place] and '"' in entry[place+2]:
                            tmp = str(entry[place][1:])+','+str(entry[place+1])+','+str(entry[place+2][:-1])
                            tmprow.append(tmp)
                            combined = True
                        elif '"' in entry[place] and '"' in entry[place+1]:
                            tmp = str(entry[place][1:])+','+str(entry[place+1][:-1])
                            tmprow.append(tmp)
                            combined = True
                        else:
                            tmprow.append(entry[place])
                            combined = False
                    elif place < len(entry)-1:
                        if '"' in entry[place] and '"' in entry[place+1]:
                            tmp = str(entry[place][1:])+','+str(entry[place+1][:-1])
                            tmprow.append(tmp)
                            combined = True
                        else:
                            tmprow.append(entry[place])
                            combined = False
                    else:
                        tmprow.append(entry[place])
                        combined = False
            if len(tmprow) == 13:
                tmprow.pop()
            data.append(tmprow)
        if location is None:
            confirmed = 0
            deaths = 0
            recoveries = 0
            for entry in data[1:]:
                confirmed += int(entry[7])
                deaths += int(entry[8])
                recoveries += int(entry[9])
            await message.channel.send(
                    f"```css\nAs of {fileDate}, there have been {confirmed} confirmed cases, {deaths} total deaths, and {recoveries} total recoveries.```"
            )
        else:
            confirmed = 0
            deaths = 0
            recoveries = 0
            for entry in data:
                if location.lower() in entry[11].lower():
                    confirmed += int(entry[7])
                    deaths += int(entry[8])
                    recoveries += int(entry[9])
            await message.channel.send(
                f"```css\nAs of {fileDate}, there are {confirmed} confirmed cases, {deaths} total deaths, and {recoveries} total recoveries for {location}.```"
            )
