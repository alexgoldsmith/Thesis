# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:49:41 2019

@author: Alex
"""

# Import packages
import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_csv('SIPP_CSV_Dataset.csv')

# Create industry sector variable
# TJBOCC1 : Occupation classification code

# Recode missing values to pandas 'NaN'
df['TJBOCC1'].where(df['TJBOCC1'] != -1, inplace = True)

# Fix difference in coding between 1996/2001 panels and 2004/2008 panels
mask = np.logical_or(df.spanel == 1996, df.spanel == 2001)
df.loc[mask, 'TJBOCC1'] = df.loc[mask, 'TJBOCC1'] * 10

# Sector codebook (Uses Standard Occupational Classification System)
## 10-430       : 11 Management Occupations
## 500-950      : 13 Business and Financtial Operations Occupations
## 1000-1240    : 15 Computer and Mathematical Occupations
## 1300-1560    : 17 Architecture and Engineering Occupations
## 1600-1960    : 19 Life, Physical, and Social Science Occupations
## 2000-2060    : 21 Community and Social Service Occupations
## 2100-2150    : 23 Legal Occupations
## 2200-2550    : 25 Education, Training, and Library Occupations
## 2600-2960    : 27 Arts, Design, Entertainment, Sports, and Media Occupations
## 3000-3540    : 29 Healthcare Practitioners and Technical Occupations
## 3600-3650    : 31 Healthcare Support Occupations
## 3700-3950    : 33 Personal Care and Service Occupations
## 4000-4160    : 35 Food Preparation and Serving Related Occupations

bins = [0, 450, 970, 1250, 1570, 1970, 2070, 2170, 2570, 2970, 3550, 3670,
        3970, 4170, np.inf]
names = ['11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31',
         '33', '35', 'other']

df['industry'] = pd.cut(df['TJBOCC1'], bins, labels = names)
print(df.industry.value_counts(sort = False))
print(sum(df.industry.isnull()))