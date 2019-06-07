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
## Create dataframe of only the 12 highest populated industries (in sample)
industry_list = ['43', '25', '41', '29', '39', '11', '35', '31', '13', '37', '51', '21']
df_of_12_ind = df[df['industry_mode'].isin(industry_list)]
lfp_by_12_ind = (df_of_12_ind.groupby(['months_since_birth', 'industry_mode', 'policy'])['LFP']
                .mean().loc[-24:24].reset_index())

## Create dictionary for plot titles
title_dict = {'11' : 'Management',
              '13' : 'Business and Finance',
              '21' : 'Community and Social Service',
              '25' : 'Education, Training, and Library',
              '29' : 'Healthcare Practitioners and Technicians',
              '31' : 'Healthcare Support',
              '35' : 'Food Preparation and Servers',
              '37' : 'Building and Grounds Cleaning and Maintenance',
              '39' : 'Personal Care and Service',
              '41' : 'Sales and Related Occupations',
              '43' : 'Office and Administrative Support',
              '51' : 'Production Occuptions'}

## Add column to df for plot titles
lfp_by_12_ind['titles'] = lfp_by_12_ind['industry_mode'].map(title_dict)

## Plot facet grid
fgrid = sns.FacetGrid(lfp_by_12_ind, col = 'titles', hue = 'policy', sharex = False,
                      col_wrap = 3, height = 4, aspect = 1)
fgrid.map(plt.plot, 'months_since_birth', 'LFP')
fgrid.set_titles(col_template = "{col_name}")
plt.subplots_adjust(top = .95, wspace = .2, hspace = .3)
fgrid.add_legend()
fgrid.fig.suptitle('Labor Force Participation Pattern by Industry')
fgrid.set_xlabels('Months Since Birth')
plt.show()

# Save figure
fgrid.savefig('LFP_pattern_by_industry.png')







