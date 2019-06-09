# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:34:41 2019

@author: Alex
"""

import pandas as pd
import statsmodels.formula.api as smf
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_3')

# Restrict sample to 24 months before and after birth

# Full sample regression
model = smf.ols(formula = \
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy', data = df)
results = model.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results.summary())


# College educated regression
df_college = df[df['eeducate'] >= 44]
model_2 = smf.ols(formula = \
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy', data = df_college)
results_2 = model.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_2.summary())

# Less than college educated regression
df_hs = df[df['eeducate'] < 44]
model_3 = smf.ols(formula = \
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy', data = df_hs)
results_3 = model.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_3.summary())