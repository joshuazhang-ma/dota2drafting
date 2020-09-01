'''
Created on Jul 31, 2020

@author: Joshua Zhang
'''

'''
Suppose you are hired by a team to try and improve their chances of winning games through better drafting.
The client has scouted a tremendous number of talented players and have put together a team with lots of potential.
The client is under pressure to perform well quickly. Their goal is to compete on the international stage.
The client believes that drafting plays a pivotal role in determining the success of the team.
You are asked to do an analysis to put the team in the best position possible to win tournaments. Each of their
players have the capacity to train three heros to a competitive level. Which heros would you recommend each of their
players to train in?
'''

import requests
import json
import shutil
import pandas as pd
import numpy as np

# June 28th, 2020 was the release date for Dota 2 patch 7.27, which implemented a big change in the drafting process:
# Captain's Mode ban count has changed from 4/1/1 for the three ban phases to 2/3/2
# Captain's Mode first pick phase is changed from Radiant/Dire/Dire/Radiant to Radiant/Dire/Radiant/Dire (assuming Radiant is first pick)
# Captain's Mode third ban phase is changed from Dire/Radiant to Radiant/Dire/Radiant/Dire

# 24 Total Bans and Picks between the two team. Below is the Ban/Pick Sequence.
# Ban 1: 1-4
# Pick 1: 5-8
# Ban 2: 9-14
# Pick 2: 15-18
# Ban 3: 19-22
# Pick 3: 23-24
pickBanSequence = [['Placeholder', 'Convenience for "Order" Data'], ['A', 'Ban'], ['B', 'Ban'], ['A', 'Ban'], ['B', 'Ban'], ['A', 'Pick'], ['B', 'Pick'], ['A', 'Pick'], ['B', 'Pick'], ['A', 'Ban'], ['B', 'Ban'], ['A', 'Ban'], ['B', 'Ban'], ['A', 'Ban'], ['B', 'Ban'], ['B', 'Pick'], ['A', 'Pick'], ['B', 'Pick'], ['A', 'Pick'], ['A', 'Ban'], ['B', 'Ban'], ['A', 'Ban'], ['B', 'Ban'], ['A', 'Pick'], ['B', 'Pick']]

def teamWinCounts(data):
    radiantWins = len(data.loc[data['radiant_win']==True,])
    direWins = len(data.loc[data['radiant_win']==False,])

    return [radiantWins, direWins]

def getIndexWithCriteria(data, top_n, var_name, boolean_comp, criteria):
    if (boolean_comp == '<'):
        filteredData = data.loc[data[var_name] < criteria,]
        indexList = data.index[0:top_n]
    elif (boolean_comp == '<='):
        filteredData = data.loc[data[var_name] <= criteria,]
        indexList = data.index[0:top_n]
    elif (boolean_comp == '>'):
        filteredData = data.loc[data[var_name] > criteria,]
        indexList = data.index[0:top_n]
    elif (boolean_comp == '>='):
        filteredData = data.loc[data[var_name] >= criteria,]
        indexList = data.index[0:top_n]
    else:
        filteredData = data.loc[data[var_name] == criteria,]
        indexList = data.index[0:top_n]

    return indexList

shutil.copy('C:\\Users\\Joshua Zhang\\Desktop\\scraping resources\\drafting with names.csv', 'C:\\Users\\Joshua Zhang\\github\\dota2drafting\\dota2draft\\dota2\\drafting with names.csv')
draft = pd.read_csv('C:\\Users\\Joshua Zhang\\github\\dota2drafting\\dota2draft\\dota2\\drafting with names.csv')
bans = draft.loc[draft['is_pick']==False,]
picks = draft.loc[draft['is_pick']==True,]

# Overview of current gameplay landscape.

#### How many matches are analyzed?
numMatches = (len(draft.index)-1)/22
numMatches = np.int64(numMatches)

# What percentage of games are won by Radiant and Dire?
radiantW, direW = teamWinCounts(draft)

# What heros are most contested, and how often are they banned and picked?
mostContested = pd.DataFrame({"Contested":draft['localized_name'].groupby(draft['localized_name']).count()})
mostBanned = pd.DataFrame({"Banned":bans['localized_name'].groupby(bans['localized_name']).count()})
mostPicked = pd.DataFrame({"Picked":picks['localized_name'].groupby(picks['localized_name']).count()})
combined = pd.merge(mostContested, mostBanned, on='localized_name', how='outer')
combined = pd.merge(combined, mostPicked, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Picked'] = combined['Picked'].apply(lambda x: np.int64(x))
combined['Banned%'] = round(combined['Banned']/combined['Contested']*100, 1)
combined['Picked%'] = round(combined['Picked']/combined['Contested']*100, 1)

# What heros are commonly banned in the first round (Most likely not possible to be picked)
firstRoundBan = pd.DataFrame({"Banned_R1":bans['localized_name'].loc[bans['order'] < 5,].groupby(bans['localized_name']).count()})
firstRoundBan.sort_values(by=['Banned_R1'], ascending=False, inplace=True)

# Combine first round ban info to combined DataFrame
combined = pd.merge(combined, firstRoundBan, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Banned_R1'] = combined['Banned_R1'].apply(lambda x: np.int64(x))

# What heros are commonly picked in the first round
firstRoundPick = pd.DataFrame({"Picked_R1":picks['localized_name'].loc[picks['order'] < 9,].groupby(picks['localized_name']).count()})
firstRoundPick.sort_values(by=['Picked_R1'], ascending=False, inplace=True)

# Combine first round pick info to combined DataFrame
combined = pd.merge(combined, firstRoundPick, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Picked_R1'] = combined['Picked_R1'].apply(lambda x: np.int64(x))

# Heros that are contested in the first round are typically high value picks. These heros are of highest value!
combined['Contested_R1'] = combined['Banned_R1'] + combined['Picked_R1']
combined['Banned_R1%'] = round(combined['Banned_R1']/combined['Contested_R1']*100, 1)
combined['Picked_R1%'] = round(combined['Picked_R1']/combined['Contested_R1']*100, 1)
combined['Contested_R1%'] = round(combined['Contested_R1']/combined['Contested']*100, 1)

# What heros are commonly banned in the second round
secondRoundBan = pd.DataFrame({"Banned_R2":bans['localized_name'].loc[(bans['order'] > 8) & (bans['order'] < 15),].groupby(bans['localized_name']).count()})
secondRoundBan.sort_values(by=['Banned_R2'], ascending=False, inplace=True)

# Combine second round ban info to combined DataFrame
combined = pd.merge(combined, secondRoundBan, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Banned_R2'] = combined['Banned_R2'].apply(lambda x: np.int64(x))

# What heros are commonly picked in the second round
secondRoundPick = pd.DataFrame({"Picked_R2":picks['localized_name'].loc[(picks['order'] > 14) & (picks['order'] < 19),].groupby(picks['localized_name']).count()})
secondRoundPick.sort_values(by=['Picked_R2'], ascending=False, inplace=True)

# Combine second round pick info to combined DataFrame
combined = pd.merge(combined, secondRoundPick, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Picked_R2'] = combined['Picked_R2'].apply(lambda x: np.int64(x))

#
combined['Contested_R2'] = combined['Banned_R2'] + combined['Picked_R2']
combined['Banned_R2%'] = round(combined['Banned_R2']/combined['Contested_R2']*100, 1)
combined['Picked_R2%'] = round(combined['Picked_R2']/combined['Contested_R2']*100, 1)
combined['Contested_R2%'] = round(combined['Contested_R2']/combined['Contested']*100, 1)

# What heros are commonly banned in the third round
thirdRoundBan = pd.DataFrame({"Banned_R3":bans['localized_name'].loc[(bans['order'] > 18),].groupby(bans['localized_name']).count()})
thirdRoundBan.sort_values(by=['Banned_R3'], ascending=False, inplace=True)

# Combine third round ban info to combined DataFrame
combined = pd.merge(combined, thirdRoundBan, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Banned_R3'] = combined['Banned_R3'].apply(lambda x: np.int64(x))

# What heros are commonly picked in the third round
thirdRoundPick = pd.DataFrame({"Picked_R3":picks['localized_name'].loc[(picks['order'] > 20),].groupby(picks['localized_name']).count()})
thirdRoundPick.sort_values(by=['Picked_R3'], ascending=False, inplace=True)

# Combine third round pick info to combined DataFrame
combined = pd.merge(combined, thirdRoundPick, on='localized_name', how='outer')
combined.fillna(0, inplace=True)
combined['Picked_R3'] = combined['Picked_R3'].apply(lambda x: np.int64(x))

#
combined['Contested_R3'] = combined['Banned_R3'] + combined['Picked_R3']
combined['Banned_R3%'] = round(combined['Banned_R3']/combined['Contested_R3']*100, 1)
combined['Picked_R3%'] = round(combined['Picked_R3']/combined['Contested_R3']*100, 1)
combined['Contested_R3%'] = round(combined['Contested_R3']/combined['Contested']*100, 1)

# Export to csv
combined.sort_values(by=['Contested'], ascending=False, inplace=True)
combined.to_csv("draftingEDA.csv")

'''
At this point, there are a few statements I can make. First, we have identified some interesting findings about the current
professional landscape.
'''
# Reporting:
print("Analyzed " + str(numMatches) + " matches")
print("Out of these matches, " + str(round(radiantW/(radiantW + direW)*100, 1)) + "% were Radiant victories.")
top_contested = ', '.join(getIndexWithCriteria(combined, 5, 'Contested', '>=', 200))
print("The top five most contested heros overall in descending order are: " + top_contested)
print("However, it is important to recognize that these contests need context.")
print("A hero banned in the first round are ones that have immense impact on the curent meta.")
r1_top_contested = ', '.join(getIndexWithCriteria(combined, 5, 'Contested_R1', '>=', 200))
print("The top five most contested heros in the first round in descending order are: " + r1_top_contested)
if (top_contested == r1_top_contested):
    print("The fact that the most contested heros are the same as the most contested heros in round one are the same implies that this set of heros are particularly meta-defining and are highly sought after.")
    print("I would recommend having a team member master these meta heros in order to gain a respect ban from the opposing team.")
else:
    print("The fact that the most contested heros are not the same as the most contested heros in round one requires more insight.")

'''
Next, I would look into which heros are the winningest.
'''

# Use player_slot to determine which team, then compare to radiant_win to see if the hero won that game

heroGP = pd.DataFrame({"GP":picks['localized_name'].groupby(picks['localized_name']).count()})
heroGP['GPGroup'] = round(heroGP['GP']/20,0)+1
heroGP['heroWins'] = picks['localized_name'].loc[(((picks['radiant_win']==True) & (picks['team']==0)) | ((picks['radiant_win']==False) & (picks['team']==1))),].groupby(picks['localized_name']).count()
heroGP.fillna(0, inplace=True)
heroGP['heroWins%'] = round(100*heroGP['heroWins']/heroGP['GP'],1)
heroGP.sort_values(by=['GPGroup', 'heroWins%'], ascending=False, inplace=True)
print(heroGP.head(20))
