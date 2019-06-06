# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:49:16 2019

@author: Alex
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')

# Education summary statistics
df = pd.read_pickle('SIPP_Dataset_3')
education_counts = df.groupby('unique_id').first()['eeducate'].value_counts(sort = False)
fig, ax = plt.subplots()
ax.bar(education_counts.index, education_counts)
ax.set_xticks(education_counts.index)
plt.show()

#LFP summary statistics
