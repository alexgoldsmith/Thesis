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
df = pd.read_pickle('SIPP_Dataset_2')

sample_size_by_occ_group = df.groupby('industry_pre_birth')['unique_id'].nunique()

# Number of individuals in sample
print(df['unique_id'].nunique())
# Number of individuals with data for pre-birth occupation group
print(sample_size_by_occ_group.sum())

# Basic Summary statistics
variables = ['rhcalyr', 'tage', 'eeducate', 'months_since_birth']
df2 = df.loc[:, variables]
sum_stats = df2.describe().transpose().round(2)
sum_stats.to_csv('summary_statistics.csv')

# LFP variable counts
df['rmesr'].value_counts(dropna = False, ascending = False)

# Crosstab college and blue collar observations
college_collar_obs = pd.crosstab(df['college'], df['blue_collar'], margins = True)

# Crosstab college and blue collar individuals
college_collar_ind = df.pivot_table(values='unique_id', index='college', columns='blue_collar',
                      aggfunc=pd.Series.nunique, margins = True)

# Table of unique individuals per state-year
year_state_table = df.pivot_table(values='unique_id', index='rhcalyr', columns='tfipsst',
                      aggfunc=pd.Series.nunique, margins = True)
year_state_table.to_csv('year_state_table.csv')

# Table of unique individuals for months since birth - policy combinations
birth_policy_table = df.pivot_table(values='unique_id', index='months_since_birth',
                                    columns='policy', aggfunc=pd.Series.nunique).loc[-24:24,:]
