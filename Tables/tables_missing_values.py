# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:46:25 2019

@author: Alex
"""

import pandas as pd
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_2')

df.isnull().sum()

# Missing data of TJBOCC1 grouped by RMESR code
print(df.groupby('rmesr')['TJBOCC1'].apply(lambda x: x.isnull().sum()/len(x)*100))

# Missing data of TJBOCC1 grouped by calendar year
print(df.groupby('rhcalyr')['TJBOCC1'].apply(lambda x: x.isnull().sum()/len(x)*100))

# Missing data of rank grouped by RMESR code
#print(df.groupby('rmesr')['occ_rank'].apply(lambda x: x.isnull().sum()/len(x)*100))

# 
missing_series = df.groupby('TJBOCC1')['occ_rank'].apply(lambda x: x.isnull().sum()/len(x)*100)