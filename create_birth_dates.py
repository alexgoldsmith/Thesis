# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:23:05 2019

@author: Alex
"""

import pandas as pd

df = pd.read_csv('SIPP_2008_panel.asc')

df.info()

## Pseudocode
# for household in SSUID: # for each sample unit
#   if RFNKIDS != 0: # If children under 18 exist in family
#       child_birth_year 