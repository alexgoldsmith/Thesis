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