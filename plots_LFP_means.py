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

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')

# Read dataset
df = pd.read_pickle('SIPP_Dataset_2')


# National LFP pattern
lfp_all = df.groupby(['months_since_birth', 'policy'])['LFP'].mean().unstack().loc[-24:24]
lfp_all.plot()

# CA and NJ LFP pattern
df_CA_NJ = df.loc[np.logical_or(df['tfipsst'] == 6, df['tfipsst'] == 34),:]
lfp_CA_NJ = df_CA_NJ.groupby(['months_since_birth', 'policy'])['LFP'].mean().unstack().loc[-24:24]
lfp_CA_NJ.plot()

# Create dictionary for plot titles (will be used later)
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

''' Code for LFP by mode occupation group'''
# Create dataframe of only the 12 highest populated industries (in sample)
industry_list = ['43', '25', '41', '29', '39', '11', '35', '31', '13', '37', '51', '21']
df_of_12_mode = df[df['industry_mode'].isin(industry_list)]
lfp_by_12_mode = (df_of_12_mode.groupby(['months_since_birth', 'industry_mode', 'policy'])['LFP']
                .mean().loc[-24:24].reset_index())

# Map titles to occupation group codes
lfp_by_12_mode['titles_mode'] = lfp_by_12_mode['industry_mode'].map(title_dict)

# Plot facet grid for mode occupation group
fgrid = sns.FacetGrid(lfp_by_12_mode, col = 'titles_mode', hue = 'policy', sharex = False,
                      col_wrap = 3, height = 4, aspect = 1)
fgrid.map(plt.plot, 'months_since_birth', 'LFP')
fgrid.set_titles(col_template = "{col_name}")
plt.subplots_adjust(top = .95, wspace = .2, hspace = .3)
fgrid.add_legend()
fgrid.fig.suptitle('Labor Force Participation Pattern by Mode Occupation Group')
fgrid.set_xlabels('Months Since Birth')
plt.show()

# Save figure
fgrid.savefig('Figures/LFP_by_mode_occupation_group.png')

'''Code for LFP by post birth occupation group'''
# Create dataframe of only the 12 highest populated industries (in sample)
df_of_12_birth = df[df['industry_post_birth'].isin(industry_list)]
lfp_by_12_birth = (df_of_12_birth.groupby(['months_since_birth', 'industry_post_birth', 'policy'])['LFP']
                .mean().loc[-24:24].reset_index())

# Map titles to occupation group codes
lfp_by_12_birth['titles_post_birth'] = lfp_by_12_birth['industry_post_birth'].map(title_dict)

# Plot facet grid for post birth occupation group
fgrid2 = sns.FacetGrid(lfp_by_12_birth, col = 'titles_post_birth', hue = 'policy', sharex = False,
                      col_wrap = 3, height = 4, aspect = 1)
fgrid2.map(plt.plot, 'months_since_birth', 'LFP')
fgrid2.set_titles(col_template = "{col_name}")
plt.subplots_adjust(top = .95, wspace = .2, hspace = .3)
fgrid2.add_legend()
fgrid2.fig.suptitle('Labor Force Participation Pattern by Post Birth Occupation Group')
fgrid2.set_xlabels('Months Since Birth')
plt.show()

fgrid2.savefig('Figures/LFP_by_post_birth_occupation_group.png')

'''Code for LFP by post birth occupation group'''
# Create dataframe of only the 12 highest populated industries (in sample)
df_of_12_pre_birth = df[df['industry_pre_birth'].isin(industry_list)]
lfp_by_12_pre_birth = (df_of_12_pre_birth.groupby(['months_since_birth', 'industry_pre_birth', 'policy'])['LFP']
                .mean().loc[-24:24].reset_index())

# Map titles to occupation group codes
lfp_by_12_pre_birth['titles_pre_birth'] = lfp_by_12_pre_birth['industry_pre_birth'].map(title_dict)

# Plot facet grid for post birth occupation group
fgrid3 = sns.FacetGrid(lfp_by_12_pre_birth, col = 'titles_pre_birth', hue = 'policy', sharex = False,
                      col_wrap = 3, height = 4, aspect = 1)
fgrid3.map(plt.plot, 'months_since_birth', 'LFP')
fgrid3.set_titles(col_template = "{col_name}")
plt.subplots_adjust(top = .95, wspace = .2, hspace = .3)
fgrid3.add_legend()
fgrid3.fig.suptitle('Labor Force Participation Pattern by Pre Birth Occupation Group')
fgrid3.set_xlabels('Months Since Birth')
plt.show()

fgrid3.savefig('Figures/LFP_by_pre_birth_occupation_group.png')