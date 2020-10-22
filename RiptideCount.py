from urllib.request import Request, urlopen
from datetime import datetime
import re, winsound, os

#bundleIDcreator: Takes in the ID of a bundle and returns the ID of one of the parts of the Bundle.
#There is a known issue with this part of the program that will cause the program to return an inaccurate number count, so doing this method is not reliable for any bundle
#created before the first Rthro bundle. If you're doing this on one of the Bundles that won in the Rthro Design Contest, you'll be fine.
def bundleIDcreator(id):
    #DO NOT REMOVE THIS WHILE LOOP!
    #This while loop allows the program to try again if Roblox rejects or never receives your request for the IDs that belong to the Bundle.
    while True:
        try:
            global bundleID
            req = Request('https://catalog.roblox.com/v1/bundles/'+str(id)+'/details', headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read().decode('utf-8')
            regex = ',"id":(.+?),'
            pattern = re.compile(regex)
            bundleID = re.findall(pattern, webpage)[0]
        except:
            print("Avoiding ERROR (bundleIDcreator)")
#Placeholder global value for the ID for one of the parts of a Bundle.
bundleID=0
createdDates = []
count = []
#Tells the program if it should continue counting up owners or not. Becomes false when the final page is reached.
keepCounting = True
#This is the part that calculates it all!
while True:
    page = 0
    owners = 0
    cursor = ""
    bundleMode = False
    id = int(input("Input ID: "))
    if id < 1000: #This line will have to be updated once Roblox makes their 1000th Bundle. This shouldn't be for a while.
        bundleMode = True
    while keepCounting:
        if page == 0:
            #Does some shuffling to see if you input a bundle or not.
            if bundleMode == True:
                if bundleID == 0:
                    bundleIDcreator(id)
                req = Request('https://inventory.roblox.com/v2/assets/'+str(bundleID)+"/owners?sortOrder=Asc&limit=100", headers={'User-Agent': 'Mozilla/5.0'})
            else:
                req = Request('https://inventory.roblox.com/v2/assets/'+str(id)+"/owners?sortOrder=Asc&limit=100", headers={'User-Agent': 'Mozilla/5.0'})
        else:
            if bundleMode:
                req = Request('https://inventory.roblox.com/v2/assets/'+str(bundleID)+"/owners?sortOrder=Asc&limit=100&cursor="+cursor, headers={'User-Agent': 'Mozilla/5.0'})
            else:
                req = Request('https://inventory.roblox.com/v2/assets/'+str(id)+"/owners?sortOrder=Asc&limit=100&cursor="+cursor, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read().decode('utf-8')
            regex = ',"created":"(.+?)T'
            pattern = re.compile(regex)
            html = re.findall(pattern, webpage)
            for i in range(len(html)):
                if len(createdDates) == 0 or html[i] not in createdDates:
                    createdDates.append(html[i])
                    count.append(1)
                elif html[i] in createdDates:
                    count[createdDates.index(html[i])] += 1
            if len(html) == 100:
                regex = '"nextPageCursor":"(.+?)",'
                pattern = re.compile(regex)
                try:
                    cursor = re.findall(pattern, webpage)[0]
                except:
                    break
                page = page + 1
            else:
                break
        except:
            print("Avoiding error (main)")
    for i in range(len(createdDates)):
        print(createdDates[i] + "\t" + str(count[i]))
    # winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
    # Remove this hashtag ^^^ if you want a sound to play when the program finishes counting.
