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
model = smf.ols(formula = 
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy', data = df)
results = model.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results.summary())


# College educated regression
model_2 = smf.ols(formula = 
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy', data = df[df['eeducate'] >= 44])
results_2 = model.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_2.summary())

# Less than college educated regression
model_3 = smf.ols(formula = 
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy', data = df[df['eeducate'] < 44])
results_3 = model.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_3.summary())

# Codes / labels translator
occ_dict   = {'11' : 'Management',
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

# Occupation group regressions
group_models_results = [smf.ols(formula = 
    'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy',
    data = df[df['industry_pre_birth'] == i]).fit(cov_type = 'cluster',
    cov_kwds={'groups': df[df['industry_pre_birth'] == i]['ssuid']}) for i in occ_dict]

# Summary of management regression
print(group_models_results[0].summary())


