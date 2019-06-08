# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:01:34 2019

@author: Alex
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')

# Education summary statistics
df = pd.read_pickle('SIPP_Dataset_3')
education_counts = df.groupby('unique_id').first()['eeducate'].value_counts(sort = False)
fig, ax = plt.subplots()
ax.bar(education_counts.index, education_counts)
ax.set_xticks(education_counts.index)
plt.show()