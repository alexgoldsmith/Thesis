# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:54:17 2019

@author: Alex
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')

# Read datasets
policy_props = pd.read_pickle('Tables/policy_props')
non_policy_props = pd.read_pickle('Tables/non_policy_props')

# Rank increase plot
fig, ax, = plt.subplots()
ind = policy_props[0:12].index
width = .4
ax.bar(ind - width/2, policy_props[0:12].iloc[:,2], width, label = 'Policy in effect')
ax.bar(ind + width/2, non_policy_props[0:12].iloc[:,2], width, label = 'Policy not in effect')
ax.legend()
ax.set_title('Occupation Rank Increase: Proportion of Population')
ax.set_ylabel('Percentage Points')
ax.set_xlabel('Months Since Birth')
plt.show()

# Rank decrease plot
fig, ax, = plt.subplots()
ind = policy_props[0:12].index
width = .4
ax.bar(ind - width/2, policy_props[0:12].iloc[:,0], width, label = 'Policy in effect')
ax.bar(ind + width/2, non_policy_props[0:12].iloc[:,0], width, label = 'Policy not in effect')
ax.legend()
ax.set_title('Occupation Rank Decrease: Proportion of Population')
ax.set_ylabel('Percentage Points')
ax.set_xlabel('Months Since Birth')
plt.show()