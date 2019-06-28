# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:14:57 2019

@author: Alex
"""

unique_persons = df['unique_id'].unique()

### Iterate through each unique person
for person in unique_persons:
    # Create dataframe for each unique person
    person_df = df[df['unique_id'] == person].loc[:,['unique_id', 'ref_date', 'birth_month', 'TBJOCC1']]
    # Create array of employer values for month of and after birth of child
    post_birth_occs = person_df[person_df['ref_date'] >= person_df['birth_month']]['TJBOCC1'].values
    # Drop null values
    post_birth_occs = post_birth_occs[~pd.isnull(post_birth_employers)]
    # True if array contains multiple values
    post_birth_occs_binary = int(len(set(post_birth_employers)) > 1)
    # Assign result back to original dataframe
    df.loc[df['unique_id'] == person, 'ever_occs_change'] = post_birth_occs_binary

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
#group_models_results = [smf.ols(formula = 
#    'LFP ~ C(rhcalyr) + C(tfipsst) + C(birth_recode) * policy',
#    data = df[df['industry_pre_birth'] == i]).fit(cov_type = 'cluster',
#    cov_kwds={'groups': df[df['industry_pre_birth'] == i]['ssuid']}) for i in occ_dict]

# Summary of management regression
#print(group_models_results[2].summary())




df = pd.read_pickle('SIPP_Dataset_2')

# Generate constant within panel weights
df['end_date'] = df.groupby('unique_id').ref_date.transform('max')

df['end_weight'] = np.nan
df['end_weight'].mask(df['ref_date'] == df['end_date'], df['wpfinwgt'], inplace = True)
df['end_weight'] = df.groupby('unique_id')['end_weight'].transform('max')



