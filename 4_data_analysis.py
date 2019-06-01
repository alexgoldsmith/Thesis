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
df = pd.read_pickle('SIPP_Dataset_2')

# TO DO
# Tabulate by occupation groups and mean wage