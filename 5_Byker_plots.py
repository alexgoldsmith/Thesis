# -*- coding: utf-8 -*-
"""
Created on Sun May 26 16:47:12 2019

@author: Alex
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
estimates = pd.read_stata('ES_DD_estimates_altered.dta')

# LFP plot
fig, ax = plt.subplots()
ax.plot(estimates['time'], estimates['b_X1'],
        marker = 'o', markersize = '4', color = 'k', label = 'After policy LFP')
ax.plot(estimates['time'], estimates['b_X2'],
        marker = 'o', markersize = '4', color = 'k', alpha = .5, label = 'Before policy LFP')
ax.fill_between(estimates['time'], estimates['b_X1'], estimates['b_X2'],
                color = 'k', alpha = .2, label = 'Difference')
ax.axvline(x = 0, color = 'k')
ax.set_ylim(.45,.85)
ax.set_title('LFP in California and New Jersey')
ax.set_xlabel('Months relative to birth')
ax.set_ylabel('Labor-force participation')
ax.legend()
plt.show()

