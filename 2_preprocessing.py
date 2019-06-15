# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:49:41 2019

@author: Alex
"""

# Import packages
import pandas as pd
import numpy as np
import os

os.chdir('C:/Users/Alex/Git_Repositories/Thesis')
df = pd.read_pickle('SIPP_Dataset')

# Convert missing values
df['eeducate'].mask(df['eeducate'] == -1, np.nan, inplace = True)
df['rmesr'].mask(df['rmesr'] == -1, np.nan, inplace = True)

# Generate unique person id
def make_identifier(df):
    str_id = df.apply(lambda x: '_'.join(map(str, x)), axis=1)
    return pd.factorize(str_id)[0]

df['unique_id'] = make_identifier(df[['spanel','ssuid','epppnum']])

# Confirm unique id generation
#print(df.groupby(['uniqueid', 'swave', 'srefmon']).size().max())

# Create date column
df['ref_date'] = pd.to_datetime(dict(year = df['rhcalyr'], month = df['rhcalmn'], day = 1), format = '%Y%m%d')

# Create datetime objects
df['CA_law'] = pd.to_datetime('7/1/2004')
df['NJ_law'] = pd.to_datetime('7/1/2009')

# Create binary variable to signify Paid Family Leave policy is in effect
## New Jersey is coded as 34 while California is coded as 6
df['policy'] = 0
filter_1 = np.logical_and(df['tfipsst'] == 34, df['birth_month'] >= df['NJ_law'])
df.loc[filter_1, 'policy'] = 1
filter_2 = np.logical_and(df['tfipsst'] == 6, df['birth_month'] >= df['CA_law'])
df.loc[filter_2, 'policy'] = 1

# Create LFP variable
df['LFP'] = np.nan
df['LFP'].mask(df['rmesr'] <= 7, 1, inplace = True)
df['LFP'].where(df['rmesr'] <= 7, 0, inplace = True)

# Create working variable (includes being on paid leave)
df['working'] = np.nan
df['working'].mask(df['rmesr'] == 1, 1, inplace = True)
df['working'].where(df['rmesr'] == 1, 0, inplace = True)

# Create looking for work variable
df['looking'] = np.nan
looking_codes = [5, 6, 7]
not_looking_codes = [1, 2, 3, 4, 8]
df['looking'].mask(df['rmesr'].isin(looking_codes), 1, inplace = True)
df['looking'].mask(df['rmesr'].isin(not_looking_codes), 0, inplace = True)

# Create variable to encode months passed since giving birth
df['months_since_birth'] = (df['ref_date'].dt.year - df['birth_month'].dt.year) * 12 + \
    (df['ref_date'].dt.month - df['birth_month'].dt.month)

# Create variable with month = -24 as reference
df['birth_recode'] = np.nan
df['birth_recode'] = df['birth_recode'].mask(df['months_since_birth'] >= -24,
                                             df['months_since_birth'] + 25)
df['birth_recode'] = df['birth_recode'].mask(df['months_since_birth'] < -24, 50)
df['birth_recode'] = df['birth_recode'].mask(df['months_since_birth'] > 24, 51)


# Create occupation group variable
# TJBOCC1 : Occupation classification code


# Sector codebook (Uses Standard Occupational Classification System)
## 10-430       : 11 Management Occupations
## 500-950      : 13 Business and Financtial Operations Occupations
## 1000-1240    : 15 Computer and Mathematical Occupations
## 1300-1560    : 17 Architecture and Engineering Occupations
## 1600-1960    : 19 Life, Physical, and Social Science Occupations
## 2000-2060    : 21 Community and Social Service Occupations
## 2100-2150    : 23 Legal Occupations
## 2200-2550    : 25 Education, Training, and Library Occupations
## 2600-2960    : 27 Arts, Design, Entertainment, Sports, and Media Occupations
## 3000-3540    : 29 Healthcare Practitioners and Technical Occupations
## 3600-3650    : 31 Healthcare Support Occupations
## 3700-3950    : 33 Protective Service Occupations
## 4000-4160    : 35 Food Preparation and Serving Related Occupations
## 4200-4250    : 37 Building and Grounds Cleaning and Maintenance Occupations
## 4300-4650    : 39 Personal Care and Service Occupations
## 4700-4960    : 41 Sales and Related Occupations
## 5000-5930    : 43 Office and Administrative Support Occupations
## 6000-6130    : 45 Farming, Fishing, and Forestry Occupations
## 6200-6940    : 47 Construction and Extraction Occupations
## 7000-7620    : 49 Installation, Maintenance, and Repair Occupations
## 7700-8960    : 51 Production Occuptions
## 9000-9750    : 53 Transportation and Material Moving Occupations
## 9840         : 0 Unemployed Veterans


bins = [0, 450, 970, 1250, 1570, 1970, 2070, 2170, 2570, 2970, 3550, 3670,
        3970, 4170, 4270, 4670, 4970, 5950, 6150, 6950, 7630, 8970, 9770, np.inf]
names = ['11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31',
         '33', '35', '37', '39', '41', '43', '45', '47', '49', '51', '53', '0']

df['industry'] = pd.cut(df['TJBOCC1'], bins, labels = names)
 
# Generate variable for mode, pre-birth, and post-birth occupation group
unique_persons = df['unique_id'].unique()
df['industry_mode'] = np.nan
df['industry_post_birth'] = np.nan
df['industry_pre_birth'] = np.nan
for person in unique_persons:
    # Create dataframe for each unique person
    person_df = df[df['unique_id'] == person].loc[:,['unique_id', 'months_since_birth', 'industry']]
    # If array of occupations contains at least one non-null value
    if person_df['industry'].notnull().values.any() == True:
        # Get mode occupation group and assign it to df variable
        mode_occ = person_df['industry'].mode().values[0]
        df['industry_mode'].mask(df['unique_id'] == person, mode_occ, inplace = True)
    # If array of occupations since birth contains at least one non-null value    
    if person_df[person_df['months_since_birth'] >= 0]['industry'].notnull().values.any() == True:
        # Get array of all occupations (group) held post birth
        post_birth_occs = person_df[person_df['months_since_birth'] >= 0]['industry']
        # Drop null values
        post_birth_occs = post_birth_occs[~pd.isnull(post_birth_occs)]
        # Get first value in array and assign it to df varible
        post_birth_occ = post_birth_occs.values[0]
        df['industry_post_birth'].mask(df['unique_id'] == person, post_birth_occ, inplace = True)
    # If array of occupations before birth contains at least one non-null value    
    if person_df[person_df['months_since_birth'] < 0]['industry'].notnull().values.any() == True:
        # Get array of all occupations (group) held before birth
        pre_birth_occs = person_df[person_df['months_since_birth'] < 0]['industry']
        # Drop null values
        pre_birth_occs = pre_birth_occs[~pd.isnull(pre_birth_occs)]
        # Get last value in array and assign it to df varible
        pre_birth_occ = pre_birth_occs.values[-1]
        df['industry_pre_birth'].mask(df['unique_id'] == person, pre_birth_occ, inplace = True)

# Generate dummy for blue collar occupation
blue_collar_groups = ['33', '35', '37', '39', '45', '47', '49', '51', '53']
white_collar_groups = ['11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '41', '43']
df['blue_collar'] = np.nan
df['blue_collar'].mask(df['industry_pre_birth'].isin(blue_collar_groups), 1, inplace = True)
df['blue_collar'].mask(df['industry_pre_birth'].isin(white_collar_groups), 0, inplace = True)

# Save dataframe to pickle
df.to_pickle('SIPP_Dataset_2')

# Code birthmonth as stata time type and write as stata file
#datetime_dict = {'birth_month': 'tm'}
#df.to_stata('SIPP_Stata_Dataset.dta', convert_dates = datetime_dict)