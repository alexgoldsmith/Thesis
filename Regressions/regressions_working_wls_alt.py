# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:34:41 2019

@author: Alex
"""

import pandas as pd
import statsmodels.api as sm
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_2')

# Initialize dataframe to store regression results
headers = ['model_1', 'model_2', 'model_3', 'model_4', 'model_5']
ols_results = pd.DataFrame(columns = headers)

# List of specifications
spec_options = ['working ~ C(l_birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(rhcalyr) + C(tfipsst) + C(l_birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(rhcalyr) : C(tfipsst) + C(l_birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(rhcalyr) * C(tfipsst) + C(l_birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(unique_id) + C(rhcalyr) : C(tfipsst) + C(l_birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)']

# Choose specification
specification = spec_options[4]

# Drop missing values
df.dropna(subset = ['working', 'rhcalyr', 'tfipsst', 'l_birth_recode', 'policy'],
          inplace = True)

# Full sample regression
model_1 = sm.WLS.from_formula(formula = specification, data = df, weights = df['end_weight'])
results_1 = model_1.fit(cov_type='cluster', cov_kwds={'groups': df['unique_id']})
#print(results_1.summary())
ols_results['model_1'] = results_1.params


# College educated regression
model_2 = sm.WLS.from_formula(formula = specification, data = df[df['college'] == 1], weights = df[df['college'] == 1]['end_weight'])
results_2 = model_2.fit(cov_type='cluster', cov_kwds={'groups': df[df['college'] == 1]['unique_id']})
#print(results_2.summary())
ols_results['model_2'] = results_2.params


# Less than college educated regression
model_3 = sm.WLS.from_formula(formula = specification, data = df[df['college'] == 0], weights = df[df['college'] == 0]['end_weight'])
results_3 = model_3.fit(cov_type='cluster', cov_kwds={'groups': df[df['college'] == 0]['unique_id']})
#print(results_3.summary())
ols_results['model_3'] = results_3.params


# Blue collar regression
model_4 = sm.WLS.from_formula(formula = specification, data = df[df['blue_collar'] == 1], weights = df[df['blue_collar'] == 1]['end_weight'])
results_4 = model_4.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 1]['unique_id']})
#print(results_4.summary())
ols_results['model_4'] = results_4.params


# White collar regression
model_5 = sm.WLS.from_formula(formula = specification, data = df[df['blue_collar'] == 0], weights = df[df['blue_collar'] == 0]['end_weight'])
results_5= model_5.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 0]['unique_id']})
#print(results_5.summary())
ols_results['model_5'] = results_5.params


# Construct joint hypothesis
joint_hypothesis = str()
for i in range(25, 25+7): #Input range of months here (birth occurs in month 25)
    joint_hypothesis += 'C(l_birth_recode)[' + str(i) + '.0]:policy = 0,'
joint_hypothesis = joint_hypothesis[:-1] # Delete trailing comma

# F-tests
f_test_1 = results_1.f_test(joint_hypothesis)
print(f_test_1)

f_test_2 = results_2.f_test(joint_hypothesis)
print(f_test_2)

f_test_3 = results_3.f_test(joint_hypothesis)
print(f_test_3)

f_test_4 = results_4.f_test(joint_hypothesis)
print(f_test_4)

f_test_5 = results_5.f_test(joint_hypothesis)
print(f_test_5)

# Save coefficients from regressions
ols_results.reset_index(inplace = True)
ols_results.to_pickle('Results/results_working_wls_FE_end_weights_alt')