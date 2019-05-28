# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:33:19 2019

@author: Alex
"""

import pandas as pd
import os
import glob

os.chdir('C:/Users/Alex/Git_Repositories/Thesis/SIPP_Data')

# 1996
df1 = pd.read_csv('1996_wave_1.asc')
print(df1.TJBOCC1.value_counts())

# 2001 
df2 = pd.read_csv('2001_wave_1.asc')
print(df2.TJBOCC1.value_counts())

# 2004
df3 = pd.read_csv('2004_wave_1.asc')
print(df3.TJBOCC1.value_counts())