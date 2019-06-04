# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:25:38 2019

@author: Alex
"""

# Import packages
import pandas as pd
import numpy as np
import os
import statsmodels

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_3')

# Separate dataframe
non_policy_df = df.loc[df['policy'] == 0]
policy_df = df.loc[df['policy'] == 1]

# Create tables for people not affected by a paid leave policy
non_policy_counts = pd.crosstab(non_policy_df['months_since_birth'], 
                                non_policy_df['occ_change'])[-24:24]

non_policy_props = pd.crosstab(non_policy_df['months_since_birth'],
                               non_policy_df['occ_change'],
                               normalize = 'index')[-24:24]*100

# Create tables for people affected by a paid leave policy
policy_counts = pd.crosstab(policy_df['months_since_birth'], 
                            policy_df['occ_change'])[-24:24]

policy_props = pd.crosstab(policy_df['months_since_birth'],
                           policy_df['occ_change'],
                           normalize = 'index')[-24:24]*100
