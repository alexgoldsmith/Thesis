# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:53:17 2019

@author: Alex
"""

# Import packages
import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_3')

sample_size_by_occ_group = df.groupby('industry_pre_birth')['unique_id'].nunique()

# Number of individuals in sample
print(df['unique_id'].nunique())
# Number of individuals with data for pre-birth occupation group
print(sample_size_by_occ_group.sum())

# Basic Summary statistics
variables = ['rhcalyr', 'tage', 'eeducate', 'months_since_birth']
df2 = df.loc[:, variables]
sum_stats = df2.describe().transpose().round(2)
#sum_stats.to_csv('summary_statistics.csv')

# LFP variable counts
df['rmesr'].value_counts(dropna = True)

# Encode education as binary for college educated
df['college'] = np.nan
df['college'].mask(df['eeducate'] >= 44, 1, inplace = True)
df['college'].mask(df['eeducate'] < 44, 0, inplace = True)

# Crosstab college and blue collar
pd.crosstab(df['college'], df['blue_collar'], margins = True)