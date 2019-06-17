# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:34:41 2019

@author: Alex
"""

import pandas as pd
import statsmodels.formula.api as smf
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_2')

# Initialize dataframe to store regression results
headers = ['model_1', 'model_2', 'model_3', 'model_4', 'model_5']
ols_results = pd.DataFrame(columns = headers)

# Three month joint hypothesis
joint_hypothesis = ('(C(birth_recode)[22.0]:policy = 0), '
                    '(C(birth_recode)[23.0]:policy = 0), '
                    '(C(birth_recode)[24.0]:policy = 0), '
                    '(C(birth_recode)[25.0]:policy = 0), '
                    '(C(birth_recode)[26.0]:policy = 0), '
                    '(C(birth_recode)[27.0]:policy = 0), '
                    '(C(birth_recode)[28.0]:policy = 0)')

# Model Specification
specification = '''LFP ~ C(rhcalyr) : C(tfipsst) + C(birth_recode) : C(tfipsst)
                   + C(birth_recode) * C(rhcalyr) + C(birth_recode) : policy'''

# Full sample regression
model_1 = smf.ols(formula = specification, data = df)
results_1 = model_1.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_1.summary())
ols_results['model_1'] = results_1.params
f_test_1 = results_1.f_test(joint_hypothesis)
print(f_test_1)


# College educated regression
model_2 = smf.ols(formula = specification, data = df[df['eeducate'] >= 44])
results_2 = model_2.fit(cov_type='cluster', cov_kwds={'groups': df[df['eeducate'] >= 44]['ssuid']})
#print(results_2.summary())
ols_results['model_2'] = results_2.params
f_test_2 = results_2.f_test(joint_hypothesis)
print(f_test_2)


# Less than college educated regression
model_3 = smf.ols(formula = specification, data = df[df['eeducate'] < 44])
results_3 = model_3.fit(cov_type='cluster', cov_kwds={'groups': df[df['eeducate'] < 44]['ssuid']})
#print(results_3.summary())
ols_results['model_3'] = results_3.params
f_test_3 = results_3.f_test(joint_hypothesis)
print(f_test_3)


# Blue collar regression
model_4 = smf.ols(formula = specification, data = df[df['blue_collar'] == 1])
results_4 = model_4.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 1]['ssuid']})
#print(results_4.summary())
ols_results['model_4'] = results_4.params
f_test_4 = results_4.f_test(joint_hypothesis)
print(f_test_4)


# White collar regression
model_5 = smf.ols(formula = specification, data = df[df['blue_collar'] == 0])
results_5= model_5.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 0]['ssuid']})
#print(results_5.summary())
ols_results['model_5'] = results_5.params
f_test_5 = results_5.f_test(joint_hypothesis)
print(f_test_5)

# Save coefficients from regressions
ols_results.reset_index(inplace = True)
ols_results.to_pickle('Results/results_lfp_ols')