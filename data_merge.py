# -*- coding: utf-8 -*-
"""
Created on Sat May 18 17:13:49 2019

@author: Alex
"""

# Import packages
import pandas as pd
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis/P2016_1118_data')

SIPP_base = pd.read_stata('SIPP_Paid_Leave.dta')

SIPP_base.ssuid = SIPP_base.ssuid.astype('int64')
SIPP_base.epppnum = SIPP_base.epppnum.astype('int64')
SIPP_base.spanel = SIPP_base.spanel.astype('int64')
SIPP_base.swave = SIPP_base.swave.astype('int64')
SIPP_base.srefmon = SIPP_base.srefmon.astype('int64')

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')

SIPP_2008_addendum = pd.read_csv('SIPP_2008_addendum.asc')

SIPP_2004_addendum = pd.read_csv('SIPP_2004_addendum.asc')

SIPP_addendum = pd.concat([SIPP_2008_addendum, SIPP_2004_addendum], ignore_index = True)

SIPP_addendum.rename(columns = {'SSUID': 'ssuid', 'SPANEL': 'spanel', 'SWAVE': 'swave',
                            'SREFMON': 'srefmon', 'EPPPNUM': 'epppnum'}, inplace = True)

df = pd.merge(SIPP_base, SIPP_addendum, on = ['ssuid', 'epppnum', 'spanel', 'swave', 'srefmon'])

datetime_dict = {'birth_month': 'tm'}

df.to_stata('SIPP_Stata_Dataset.dta', convert_dates = datetime_dict)