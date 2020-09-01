import requests
import json
import shutil
import pandas as pd
import numpy as np
import os

#### Helper Functions
# Check if file was processed already
def savedPlayerData(saveFile, matchId):
    skip = False
    save = pd.read_csv(saveFile)
    list_of_matches = save['match_id']
    if (matchId in list_of_matches):
        skip = True

    return skip

folder_path = "C:\\Users\\Joshua Zhang\\Desktop\\scraping resources\\"
previousSave = "C:\\Users\\Joshua Zhang\\github\\dota2drafting\\dota2draft\\dota2\\processedMatches.csv"
jsons = [pos_json for pos_json in os.listdir(folder_path) if pos_json.endswith(".json")]

# dataframe with all players information in it
keys_to_extract = ['match_id', 'player_slot', 'hero_id', 'dn_t', 'gold_t', 'lh_t', 'times', 'xp_t']
df_playerData = pd.DataFrame(columns = keys_to_extract)

# Pull out data that evolves over time

for index, js in enumerate(jsons):
    if (not savedPlayerData(saveFile, js.split('.')[0])):
        with open(os.path.join(folder_path, js)) as json_file:
            json_data = json.load(json_file)

            for playerRadiant in range(5): # range should be 5
                players = json_data['players'][playerRadiant]
                playerData = {key: players[key] for key in keys_to_extract}
                df_playerData = df_playerData.append(playerData, ignore_index = True)

print(df_playerData)
