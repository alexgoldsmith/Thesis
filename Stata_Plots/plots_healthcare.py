# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 20:28:02 2019

@author: Alex
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')

ols = pd.read_stata('Stata_Results/results_occs_weighted.dta')

fig, axes = plt.subplots(figsize = (10,6), nrows = 3)


def coef_plot(ax, array):
    ax.plot(list(range(-24, 25)), array, marker = 'o')
    ax.set_xticks(list(range(-24, 25, 3)))
    ax.axhline(linestyle = '--')
    ax.axvline()
    ax.set_xlabel('Months Since Birth')

coef_plot(axes[0], ols['b_rm_lfp_X29'])
axes[0].set_title('Labor-force Participation')
coef_plot(axes[1], ols['b_working_X29'])
axes[1].set_title('Employment')
coef_plot(axes[2], ols['b_looking_X29'])
axes[2].set_title('Job Search')



fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle('Healthcare Practicioners and Technicians Difference in Difference Coefficients', fontsize = 16)
plt.show()
fig.savefig('Stata_Figures/figure_healthcare.png')