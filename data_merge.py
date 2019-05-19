# -*- coding: utf-8 -*-
"""
Created on Sat May 18 17:13:49 2019

@author: Alex
"""

import pandas as pd

SIPP_base = pd.read_stata('SIPP_Paid_Leave.dta')

SIPP_base.rename(columns = {'ssuid': 'SSUID', 'spanel': 'SPANEL', 'swave': 'SWAVE',
                            'srefmon': 'SREFMON', 'epppnum': 'EPPPNUM'}, inplace = True)

SIPP_base.SSUID = SIPP_base.SSUID.astype('int64')
SIPP_base.EPPPNUM = SIPP_base.EPPPNUM.astype('int64')
SIPP_base.SPANEL = SIPP_base.SPANEL.astype('int64')
SIPP_base.SWAVE = SIPP_base.SWAVE.astype('int64')
SIPP_base.SREFMON = SIPP_base.SREFMON.astype('int64')

SIPP_2008_addendum = pd.read_csv('SIPP_2008_addendum.asc')

SIPP_2004_addendum = pd.read_csv('SIPP_2004_addendum.asc')

SIPP_addendum = pd.concat([SIPP_2008_addendum, SIPP_2004_addendum], ignore_index = True)

df = pd.merge(SIPP_base, SIPP_addendum, on = ['SSUID', 'EPPPNUM', 'SPANEL', 'SWAVE', 'SREFMON'])
