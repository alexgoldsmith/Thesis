# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:24:35 2019

@author: Alex
"""

import pandas as pd
import os
os.chdir('C:/Users/Alex/Git_Repositories/Thesis/SIPP_Data_1996_2001')
df_1996 = pd.read_csv('1996_wave_1.asc')
os.chdir('C:/Users/Alex/Git_Repositories/Thesis/SIPP_Data')
df_2004 = pd.read_csv('2004_wave_1.asc')
