# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 20:28:02 2019

@author: Alex
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
ols = pd.read_pickle('Results/results_lfp_ols_3')

fig, axes = plt.subplots(figsize = (10,12), nrows = 5)


def coef_plot(ax, array):
    ax.plot(list(range(-24, 25)), array[-51:-2], marker = 'o')
    ax.set_xticks(list(range(-24, 25, 3)))
    ax.axhline(linestyle = '--')
    ax.set_ylabel('LFP')
    ax.set_xlabel('Months Since Birth')

coef_plot(axes[0], ols['model_1'])
axes[0].set_title('Full Sample')
coef_plot(axes[1], ols['model_2'])
axes[1].set_title('College Educated')
coef_plot(axes[2], ols['model_3'])
axes[2].set_title('Less than College')
coef_plot(axes[3], ols['model_4'])
axes[3].set_title('Blue Collar')
coef_plot(axes[4], ols['model_5'])
axes[4].set_title('White Collar')


fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle('LFP Difference in Difference Coefficients', fontsize = 16)
plt.show()
fig.savefig('Figures/figure_lfp_ols_3.png')