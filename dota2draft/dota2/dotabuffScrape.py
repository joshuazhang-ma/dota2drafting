'''
Created on Jul 28, 2020

@author: Joshua Zhang
'''

import requests
import json
import os.path
import pandas as pd
import time

### Keys ###
api_key = '8916ae54-72b8-4dc0-a923-daaa6a0f9b85'

def getHero():
    if not os.path.isfile('heroList.csv'):
        request = requests.get("https://api.opendota.com/api/constants/heroes").json()
        matchesDF = pd.DataFrame(request).transpose()
        matchesDF.to_csv('heroList.csv')
    
    return

def getMatches():
    ### File Name ###
    filename = "matchList.csv"
    
    # Link to the list of matches = "Professional Matches"
    html = "https://api.opendota.com/api/proMatches"
    
    # Get json from html, if the corresponding match data is not already on computer file.
    request = requests.get(html).json()
    print("getMatches - Data successfully received from API.")

    matchesDF = pd.DataFrame(request)

    if not os.path.isfile(filename):
        matchesDF.to_csv(filename)
    else: # else it exists so append without writing the header
        matchesDF.to_csv(filename, mode='a', header=False)
    
    return

def getDraft(api, match):
    ### File Name ###
    filename = str(match) + ".json"

    # Set the match to get drafting results from
    html = "https://api.opendota.com/api/matches/" + str(match) # + "?api_key=" + api

    # Get json from html, if the corresponding match data is not already on computer file.
    if (not os.path.exists(filename)):
        request = requests.get(html).json()
        print("getDraft - Match #" + str(match) + ":  Data successfully received from API.")

        # Write data to json file
        with open(filename, "w") as save_file:
            json.dump(request, save_file)
    
        # with open(filename, "r") as load_file:
        jsonData = request # json.load(load_file)
    
        # With the data loaded, create a DF for picks and bans
        pb = jsonData['draft_timings']
        matchResult = jsonData['radiant_win']
        pbDF = pd.DataFrame(pb)
        pbDF['radiant_win'] = matchResult
        pbDF['match_id'] = match

        if not os.path.isfile('drafting.csv'):
            pbDF.to_csv('drafting.csv')
        else: # else it exists so append without writing the header
            pbDF.to_csv('drafting.csv', mode='a', header=False)

    return

def addHeroNames():
    draft = pd.read_csv('drafting.csv')
    names = pd.read_csv('heroList.csv', usecols = ['id', 'localized_name'])
    
    combined = draft.merge(names, how = 'inner', left_on = 'hero_id', right_on = 'id')
    combined.to_csv('drafting with names.csv', index = False)
    
    return 

def main():
    # Grab hero list
    getHero()
    # Grab some more match data
    getMatches()
    
    # get a unique list of matchID from matchList.csv
    matchList = list(set(pd.read_csv("matchList.csv")['match_id']))
    for match in matchList:
        getDraft(api_key, match)
        time.sleep(1.1)
      
    addHeroNames()
    
    return

main()
    
    
    
    
    
    
    
    


