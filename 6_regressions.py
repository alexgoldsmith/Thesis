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

# Three month joint hypothesis
joint_hypothesis = ('(C(birth_recode)[T.22.0]:policy = 0), '
                    '(C(birth_recode)[T.23.0]:policy = 0), '
                    '(C(birth_recode)[T.24.0]:policy = 0), '
                    '(C(birth_recode)[T.25.0]:policy = 0), '
                    '(C(birth_recode)[T.26.0]:policy = 0), '
                    '(C(birth_recode)[T.27.0]:policy = 0), '
                    '(C(birth_recode)[T.28.0]:policy = 0)')

# Model Specification
specification = 'LFP ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) * policy'

# Full sample regression
model_1 = smf.ols(formula = specification, data = df)
results_1 = model_1.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_1.summary())
f_test_1 = results_1.f_test(joint_hypothesis)
print(f_test_1)


# College educated regression
model_2 = smf.ols(formula = specification, data = df[df['eeducate'] >= 44])
results_2 = model_2.fit(cov_type='cluster', cov_kwds={'groups': df[df['eeducate'] >= 44]['ssuid']})
#print(results_2.summary())
f_test_2 = results_2.f_test(joint_hypothesis)
print(f_test_2)


# Less than college educated regression
model_3 = smf.ols(formula = specification, data = df[df['eeducate'] < 44])
results_3 = model_3.fit(cov_type='cluster', cov_kwds={'groups': df[df['eeducate'] < 44]['ssuid']})
#print(results_3.summary())
f_test_3 = results_3.f_test(joint_hypothesis)
print(f_test_3)


# Blue collar regression
model_4 = smf.ols(formula = specification, data = df[df['blue_collar'] == 1])
results_4 = model_4.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 1]['ssuid']})
#print(results_4.summary())
f_test_4 = results_4.f_test(joint_hypothesis)
print(f_test_4)


# White collar regression
model_5 = smf.ols(formula = specification, data = df[df['blue_collar'] == 0])
results_5= model_5.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 0]['ssuid']})
#print(results_5.summary())
f_test_5 = results_5.f_test(joint_hypothesis)
print(f_test_5)


# Occupation group regressions
#group_models_results = [smf.ols(formula = 
#    'LFP ~ C(rhcalyr) + C(tfipsst) + C(birth_recode) * policy',
#    data = df[df['industry_pre_birth'] == i]).fit(cov_type = 'cluster',
#    cov_kwds={'groups': df[df['industry_pre_birth'] == i]['ssuid']}) for i in occ_dict]

# Summary of management regression
#print(group_models_results[2].summary())

'''Why test for three months before and after? 
   What about the directions of the coefficients, do they matter?'''

