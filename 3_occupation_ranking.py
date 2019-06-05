# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:34:51 2019

@author: Alex
"""

import pandas as pd
import numpy as np
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')
column_titles = ['SIPP_name', 'TJBOCC1', 'occ_code']
occ_codes = pd.read_excel('2008_SIPP_SOC_crosswalk.xls', header = None,
                          names = column_titles)
occ_wages = pd.read_excel('national_M2008_dl.xls', na_values = ['*', '#'])


# Check for duplciates
print(occ_codes[occ_codes.duplicated('occ_code', keep = False)])
print(occ_wages[occ_wages.duplicated('occ_code', keep = False)])

# Strip whitespace
occ_codes['occ_code'] = occ_codes['occ_code'].str.strip()
occ_wages['occ_code'] = occ_wages['occ_code'].str.strip()

# Merge
occ_merged = pd.merge(occ_codes, occ_wages, how = 'left', on = ['occ_code'], validate = '1:1')

# Rank occupations
# Warning: Ranking by hourly rather than annual wages leads to missing data
occ_merged['occ_rank'] = occ_merged['h_median'].rank(ascending = False)

# Drop superfluous columns
occ_small = occ_merged[['TJBOCC1', 'SIPP_name', 'occ_rank']]

# Read SIPP dataset
SIPP_Data = pd.read_pickle('SIPP_Dataset_2')

# Merge
df = pd.merge(SIPP_Data, occ_small, how = 'left', on = ['TJBOCC1'], validate = 'm:1')

# Sort 
df.sort_values(['unique_id', 'ref_date'], inplace=True)

# Take first differences of rank
df['rank_diff'] = df.groupby('unique_id')['occ_rank'].diff()

# Codify to moving up or down rank
df['occ_change'] = np.nan
df['occ_change'].mask(df['rank_diff'] == 0, 0, inplace = True)
df['occ_change'].mask(df['rank_diff'] < 0, 1, inplace = True)
df['occ_change'].mask(df['rank_diff'] > 0, -1, inplace = True)

# Create binary to indicate post birth
df['post_birth'] = np.nan
df['post_birth'].mask(df['months_since_birth'] <= 0, 0, inplace = True)
df['post_birth'].mask(df['months_since_birth'] > 0, 1, inplace = True)

df.to_pickle('SIPP_Dataset_3')

table = pd.crosstab(df['months_since_birth'],df['occ_change'])
table[-24:24]

# Create cross tab of occ change by months since birth for policy enacted and non policy enacted