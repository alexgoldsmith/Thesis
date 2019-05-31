# -*- coding: utf-8 -*-
"""
Created on Sat May 18 17:13:49 2019

@author: Alex
"""

# Import packages
import pandas as pd
import os
import glob

os.chdir('D:/Users/Alex/Git_Repositories/Thesis/SIPP_Data')

# Create list of filenmaes
datafiles = glob.glob('*.asc')

# Read and concatenate datafiles
SIPP_addendum = pd.concat(pd.read_csv(f) for f in datafiles)

# Drop extra column
SIPP_addendum.drop(columns = 'RPYPER1', inplace = True)


SIPP_addendum.rename(columns = {'SSUID': 'ssuid', 'SPANEL': 'spanel', 'SWAVE': 'swave',
                            'SREFMON': 'srefmon', 'EPPPNUM': 'epppnum'}, inplace = True)

os.chdir('D:/Users/Alex/Git_Repositories/Thesis/P2016_1118_data')

# Read base data
SIPP_base = pd.read_stata('SIPP_Paid_Leave.dta')

# Reassign datatypes
#SIPP_addendum['ssuid'] = SIPP_addendum['ssuid'].astype('object')
#SIPP_addendum['spanel'] = SIPP_addendum['spanel'].astype('int16')
#SIPP_addendum['swave'] = SIPP_addendum['swave'].astype('int8')
#SIPP_addendum['srefmon'] = SIPP_addendum['srefmon'].astype('int8')
#SIPP_addendum['epppnum'] = SIPP_addendum['epppnum'].astype('int16')
SIPP_base['ssuid'] = SIPP_base['ssuid'].astype('int64')
SIPP_base['spanel'] = SIPP_base['spanel'].astype('int64')
SIPP_base['swave'] = SIPP_base['swave'].astype('int64')
SIPP_base['srefmon'] = SIPP_base['srefmon'].astype('int64')
SIPP_base['epppnum'] = SIPP_base['epppnum'].astype('int64')




SIPP_addendum.loc[:,['ssuid', 'spanel', 'swave', 'srefmon', 'epppnum']].head()

# Merge dataframes, keep intersection
df = pd.merge(SIPP_base, SIPP_addendum, on = ['ssuid', 'epppnum', 'spanel', 'swave', 'srefmon'],
              validate = '1:1')

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')

# Save dataframe to pickle
df.to_pickle('SIPP_Dataset')

# Code birthmonth as stata time type and write as stata file
datetime_dict = {'birth_month': 'tm'}
df.to_stata('SIPP_Stata_Dataset.dta', convert_dates = datetime_dict)