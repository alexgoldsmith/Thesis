# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:12:34 2019

@author: Alex
"""

import pandas as pd

df = pd.read_csv('SIPP_2014_panel.asc')

df.info()

sample_household = df[df['SSUID'] == 19925587235]

sample_household['SWAVE'].value_counts()

sample_household['EPPPNUM'].value_counts()

sample_household['EPNMOM'].value_counts()

sample_child_observation = sample_household[sample_household['EPPPNUM'] == 1203]

sample_child['TBYEAR']
sample_child['EBMNTH']