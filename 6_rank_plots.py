# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:54:17 2019

@author: Alex
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')
estimates = pd.read_stata('my_estimates.dta')

# LFP plot
fig, ax = plt.subplots()
ax.plot(estimates['time'], estimates['b_X1'],
        marker = 'o', markersize = '4', color = 'k', label = 'After policy LFP')
ax.plot(estimates['time'], estimates['b_X2'],
        marker = 'o', markersize = '4', color = 'k', alpha = .5, label = 'Before policy LFP')
#ax.fill_between(estimates['time'], estimates['b_X1'], estimates['b_X2'],
#                color = 'k', alpha = .2, label = 'Difference')
ax.axvline(x = 0, color = 'k')
#ax.set_ylim(.45,.85)
ax.set_title('LFP in California and New Jersey')
ax.set_xlabel('Months relative to birth')
ax.set_ylabel('Labor-force participation')
ax.legend()
plt.show()

# Read datasets
policy_props = pd.read_pickle('policy_props')
non_policy_props = pd.read_pickle('non_policy_props')

# Rank increase plot
fig, ax, = plt.subplots()
ind = policy_props[0:6].index
width = .4
ax.bar(ind - width/2, policy_props[0:6].iloc[:,2], width, label = 'Policy in effect')
ax.bar(ind + width/2, non_policy_props[0:6].iloc[:,2], width, label = 'Policy not in effect')
ax.legend()
ax.set_title('Occupation Rank Increase: Proportion of Population')
ax.set_ylabel('Percentage Points')
ax.set_xlabel('Months Since Birth')
plt.show()

# Rank decrease plot
fig, ax, = plt.subplots()
ind = policy_props[0:6].index
width = .4
ax.bar(ind - width/2, policy_props[0:6].iloc[:,0], width, label = 'Policy in effect')
ax.bar(ind + width/2, non_policy_props[0:6].iloc[:,0], width, label = 'Policy not in effect')
ax.legend()
ax.set_title('Occupation Rank Decrease: Proportion of Population')
ax.set_ylabel('Percentage Points')
ax.set_xlabel('Months Since Birth')
plt.show()