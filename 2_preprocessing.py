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

# Create variable to encode months passed since giving birth
df['months_since_birth'] = (df['ref_date'] - df['birth_month']).astype('timedelta64[M]')

# Create variable with month = -24 as reference
df['birth_recode'] = np.nan
df['birth_recode'] = df['birth_recode'].mask(df['months_since_birth'] >= -24,
                                             df['months_since_birth'] + 25)
df['birth_recode'] = df['birth_recode'].mask(df['months_since_birth'] < -24, 50)
df['birth_recode'] = df['birth_recode'].mask(df['months_since_birth'] > 24, 51)


# Create industry sector variable
# TJBOCC1 : Occupation classification code

# Recode missing values to pandas 'NaN'
df['TJBOCC1'].mask(df['TJBOCC1'] == -1, inplace = True)

# Fix difference in coding between 1996/2001 panels and 2004/2008 panels
mask = np.logical_or(df.spanel == 1996, df.spanel == 2001)
df.loc[mask, 'TJBOCC1'] = df.loc[mask, 'TJBOCC1'] * 10

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
## 3700-3950    : 33 Personal Care and Service Occupations
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
## 9840         : O Unemployed Veterans


bins = [0, 450, 970, 1250, 1570, 1970, 2070, 2170, 2570, 2970, 3550, 3670,
        3970, 4170, 4270, 4670, 4970, 5950, 6150, 6950, 7630, 8970, 9770, np.inf]
names = ['11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31',
         '33', '35', '37', '39', '41', '43', '45', '47', '49', '51', '53', 'other']

df['industry'] = pd.cut(df['TJBOCC1'], bins, labels = names)

# Encode change of employer

#df.shift

## Recode missing values to pandas 'NaN'
df['EENO1'].where(df['EENO1'] != -1, inplace = True)
 
## For each unique person extract employer codes before birth and after birth
### Create numpy array of unique person ids
unique_persons = df['unique_id'].unique()

# Save dataframe to pickle
df.to_pickle('SIPP_Dataset_2')

# Save dataset as stata datafile
datetime_dict = {'birth_month': 'tm',
                 'ref_date' : 'tm'}

df.to_stata('SIPP_Stata_Dataset_2.dta', convert_dates = datetime_dict)

