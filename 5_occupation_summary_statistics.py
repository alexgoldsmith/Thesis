# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 12:53:17 2019

@author: Alex
"""

# Import packages
import pandas as pd
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_3')


sample_size_by_occ_group = df.groupby('industry_pre_birth')['unique_id'].nunique()
print(sample_size_by_occ_group.sum())