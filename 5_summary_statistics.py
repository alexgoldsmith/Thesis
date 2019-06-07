# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:49:16 2019

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

# National LFP pattern
lfp_all = df.groupby(['months_since_birth', 'policy'])['LFP'].mean().unstack().loc[-24:24]
lfp_all.plot()

# CA and NJ LFP pattern
df_CA_NJ = df.loc[np.logical_or(df['tfipsst'] == 6, df['tfipsst'] == 34),:]
lfp_CA_NJ = df_CA_NJ.groupby(['months_since_birth', 'policy'])['LFP'].mean().unstack().loc[-24:24]
lfp_CA_NJ.plot()

# National LFP pattern by industry
industry_list = ['43', '25', '41', '29', '39', '11', '35', '31', '13', '37', '51', '21']
df_of_12_ind = df[df['industry_mode'].isin(industry_list)]
lfp_by_12_ind = (df.groupby(['months_since_birth', 'industry_mode', 'policy'])['LFP']
                .mean().loc[-24:24].reset_index())

fgrid = sns.FacetGrid(lfp_by_12_ind, col = 'industry_mode', hue = 'policy')
fgrid.map(plt.plot, 'months_since_birth', 'LFP')
fgrid.add_legend()






