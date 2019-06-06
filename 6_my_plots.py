# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:54:17 2019

@author: Alex
"""

# Read datasets
policy_props = pd.read_pickle('policy_props')
non_policy_props = pd.read_pickle('non_policy_props')

# Rank increase plot
fig, ax, = plt.subplots(figsize = (20,10))
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
fig, ax, = plt.subplots(figsize = (20,10))
ind = policy_props[0:6].index
width = .4
ax.bar(ind - width/2, policy_props[0:6].iloc[:,0], width, label = 'Policy in effect')
ax.bar(ind + width/2, non_policy_props[0:6].iloc[:,0], width, label = 'Policy not in effect')
ax.legend()
ax.set_title('Occupation Rank Decrease: Proportion of Population')
ax.set_ylabel('Percentage Points')
ax.set_xlabel('Months Since Birth')
plt.show()