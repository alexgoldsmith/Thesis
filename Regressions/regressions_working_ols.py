# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:34:41 2019

@author: Alex
"""

import pandas as pd
import statsmodels.formula.api as smf
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset_2')

# Initialize dataframe to store regression results
headers = ['model_1', 'model_2', 'model_3', 'model_4', 'model_5']
ols_results = pd.DataFrame(columns = headers)

# List of specifications
spec_options = ['working ~ C(birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(rhcalyr) + C(tfipsst) + C(birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(rhcalyr) : C(tfipsst) + C(birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)',
                'working ~ C(rhcalyr) * C(tfipsst) + C(birth_recode) : (C(tfipsst) + C(rhcalyr) + policy)']

# Choose specification
specification = spec_options[3]

# Drop missing values
df.dropna(subset = ['working', 'rhcalyr', 'tfipsst', 'birth_recode', 'policy'],
          inplace = True)

# Full sample regression
model_1 = smf.ols(formula = specification, data = df)
results_1 = model_1.fit(cov_type='cluster', cov_kwds={'groups': df['ssuid']})
#print(results_1.summary())
ols_results['model_1'] = results_1.params


# College educated regression
model_2 = smf.ols(formula = specification, data = df[df['eeducate'] >= 44])
results_2 = model_2.fit(cov_type='cluster', cov_kwds={'groups': df[df['eeducate'] >= 44]['ssuid']})
#print(results_2.summary())
ols_results['model_2'] = results_2.params


# Less than college educated regression
model_3 = smf.ols(formula = specification, data = df[df['college'] == 0])
results_3 = model_3.fit(cov_type='cluster', cov_kwds={'groups': df[df['college'] == 0]['ssuid']})
#print(results_3.summary())
ols_results['model_3'] = results_3.params


# Blue collar regression
model_4 = smf.ols(formula = specification, data = df[df['blue_collar'] == 1])
results_4 = model_4.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 1]['ssuid']})
#print(results_4.summary())
ols_results['model_4'] = results_4.params


# White collar regression
model_5 = smf.ols(formula = specification, data = df[df['blue_collar'] == 0])
results_5= model_5.fit(cov_type='cluster', cov_kwds={'groups': df[df['blue_collar'] == 0]['ssuid']})
#print(results_5.summary())
ols_results['model_5'] = results_5.params


# Construct joint hypothesis
joint_hypothesis = str()
for i in range(25+3, 25+10): #Input range of months here (birth occurs in month 25)
    joint_hypothesis += 'C(birth_recode)[' + str(i) + '.0]:policy = 0,'
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
ols_results.to_pickle('Results/results_working_ols')