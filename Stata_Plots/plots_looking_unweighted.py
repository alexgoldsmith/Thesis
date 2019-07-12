# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 20:28:02 2019

@author: Alex
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')

ols = pd.read_stata('Stata_Results/results_main_unweighted.dta')
wls = pd.read_stata('Stata_Results/results_main_weighted.dta')

fig, axes = plt.subplots(figsize = (10,12), nrows = 5)


def coef_plot(ax, array_1, array_2):
    ax.plot(list(range(-24, 25)), array_1, marker = 'o', label = 'Unweighted')
    ax.plot(list(range(-24, 25)), array_2, marker = 'o', label = 'Weighted')
    ax.set_xticks(list(range(-24, 25, 3)))
    ax.axhline(linestyle = '--')
    ax.axvline()
    ax.set_xlabel('Months Since Birth')
    ax.legend(loc = 'upper left')

coef_plot(axes[0], ols['b_looking_X1'], wls['b_looking_X1'])
axes[0].set_title('Full Sample')
coef_plot(axes[1], ols['b_looking_X2'], wls['b_looking_X2'])
axes[1].set_title('College Educated')
coef_plot(axes[2], ols['b_looking_X3'], wls['b_looking_X3'])
axes[2].set_title('Less than College')
coef_plot(axes[3], ols['b_looking_X4'], wls['b_looking_X4'])
axes[3].set_title('White Collar')
coef_plot(axes[4], ols['b_looking_X5'], wls['b_looking_X5'])
axes[4].set_title('Blue Collar')



fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle('Job Search Difference in Difference Coefficients', fontsize = 16)
plt.show()
fig.savefig('Stata_Figures/figure_looking_unweighted.png')