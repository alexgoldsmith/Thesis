# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:34:51 2019

@author: Alex
"""

import pandas as pd
import numpy as np
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')
column_names = ['TJBOCC1', 'occ_name', 'OCC_CODE']
occ_codes = pd.read_csv('occ_codes.txt', sep = '  ', names = column_names)
occ_wages = pd.read_excel('national_M2018_dl.xlsx', na_values = ['*', '#'])

occ_codes['OCC_CODE'] = occ_codes['OCC_CODE'].str.replace('(','')
occ_codes['OCC_CODE'] = occ_codes['OCC_CODE'].str.replace(')','')

# Check for duplciates
print(occ_codes[occ_codes.duplicated('OCC_CODE', keep = False)])
print(occ_wages[occ_wages.duplicated('OCC_CODE', keep = False)])

# Drop duplicates
occ_wages = occ_wages.drop_duplicates('OCC_CODE', keep = 'last')
print(occ_wages[occ_wages.duplicated('OCC_CODE', keep = False)])

# Merge
occ_merged = pd.merge(occ_codes, occ_wages, on = ['OCC_CODE'], validate = '1:1')

# Sort and rank occupations
# Warning: Ranking by hourly rather than annual wages leads to missing data
occ_merged.sort_values('H_MEDIAN', ascending = False, inplace = True)
occ_merged['occ_rank'] = occ_merged['H_MEDIAN'].rank(ascending = False)

# Drop superfluous columns
occ_small = occ_merged[['TJBOCC1', 'occ_rank']]

# Read SIPP dataset
SIPP_Data = pd.read_pickle('SIPP_Dataset_2')

# Merge
df = pd.merge(SIPP_Data, occ_small, how = 'left', on = ['TJBOCC1'], validate = 'm:1')

print(sum(df['occ_rank'].isna()))




