'''
Created on Jul 31, 2020

@author: Joshua Zhang
'''

import requests
import json
import os.path
import pandas as pd
import time
import scipy
import tensorflow

draft = pd.read_csv("drafting.csv")

print(draft.head(10))

r1bans = draft.loc[draft['order']<4,]
print(r1bans)

firstBanGroup = r1bans.groupby('hero_id').count()
