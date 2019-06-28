# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:49:41 2019

@author: Alex
"""

# Import packages
import pandas as pd
import numpy as np
import os

os.chdir('D:/Users/Alex/Git_Repositories/Thesis/Stata_Regressions')
df = pd.read_pickle('SIPP_Dataset')

# Convert missing values
df['eeducate'].mask(df['eeducate'] == -1, np.nan, inplace = True)
df['rmesr'].mask(df['rmesr'] == -1, np.nan, inplace = True)

# Generate unique person id
def make_identifier(df):
    str_id = df.apply(lambda x: '_'.join(map(str, x)), axis=1)
    return pd.factorize(str_id)[0]

df['unique_id'] = make_identifier(df[['spanel','ssuid','epppnum']])

# Create date column
df['ref_date'] = pd.to_datetime(dict(year = df['rhcalyr'], month = df['rhcalmn'], day = 1), format = '%Y%m%d')

# Create variable to encode months passed since giving birth
df['months_since_birth'] = (df['ref_date'].dt.year - df['birth_month'].dt.year) * 12 + \
    (df['ref_date'].dt.month - df['birth_month'].dt.month)            

# Create occupation group variable
# TJBOCC1 : Occupation classification code


# Occupation grouping 2004 & 2008 (Uses Standard Occupational Classification System)
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

# Occupation grouping 1996 and 2001
## 003-022 : 11 Executive, Administrative, and Managerial Occupations
## 023-037 : 13 Management Related Occupations
## 043-063 : 17 Architects and Engineers
## 064-068 : 15 Mathematical and Computer Scientists
## 069-083 : 19 Natural Scientists
## 084-106 : 29 Health Diagnosing Occupations & Health Assesement and Treating Occupations & Therapists
## 113-165 : 25 Teachers, Postsecondary & Teachers, Except Postsecondary & Librarians, Archivists, and Curators
## 166-173 : 19 Social Scientists and Urban Planners
## 174-177 : 21 Social, Recreation, and Religious Workers
## 178-179 : 23 Layers and Judges
## 183-199 : 27 Writers, Artists, Entertainers, and Athletes
## 203-208 : 29 Health Technologists and Technicians
## 213-218 : 17 Engineering and Related Technologists and Technicians
## 223-225 : 19 Science Technicians
## 226-235 : other_1 Technicians, Except Health, Engineering, and Science
## 243-290 : 41 Sales and Related Occupations
## 303-391 : 43 Administrative Support Occupations, Including Clerical
## 403-408 : other_2 Private Household Occupations
## 413-427 : 33 Protective Service Occupations
## 433-444 : 35 Food Preparation and Service Occupations
## 445-447 : 31 Health Service Occupations
## 448-455 : 37 Cleaning and Building Service Occupations, Except Household
## 456-469 : 39 Personal Service Occupations
## 473-499 : 45 Farming, Forestry, and Fishing Occupations
## 503-549 : 49 Precision Product, Craft, and Repair Occupations
## 553-617 : 47 Construction Trades & Extractive Occupations
## 628-799 : 51 Precision Production Occupations & Operators, Fabricators, and Laborers
## 803-865 : 53 Transportation and Material Moving Occupations
## 866-874 : 47 Helpers, Construction and Extractive Occupations
## 875-909 : 0 Freight, Stock, and Material Handlers & Military Occupations 
##             & Experienced Unemployed Not Classified by Occupation

bins_1996_2001 = [0, 22, 40, 63, 68, 83, 106, 165, 173, 177, 179, 200, 210, 220,
                  225, 240, 300, 400, 410, 430, 444, 447, 455, 470, 500, 550, 620,
                  800, 865, 874, np.inf]
# Strange names are because the pandas cut does not allow duplicate names
names_1996_2001 = ['11', '13', '17', '15', '19', '29', '25', 'change_to_19',
                   '21', '23', '27', 'change_to_29', 'change_to_17', 'also_to_19',
                   'other_1', '41', '43', 'other_2', '33', '35', '31', '37', '39',
                   '45', '49', '47', '51', '53', 'change_to_47', '0']

bins_2004_2008 = [0, 450, 970, 1250, 1570, 1970, 2070, 2170, 2570, 2970, 3550, 3670,
        3970, 4170, 4270, 4670, 4970, 5950, 6150, 6950, 7630, 8970, 9770, np.inf]
names_2004_2008 = ['11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31',
         '33', '35', '37', '39', '41', '43', '45', '47', '49', '51', '53', '0']


conditional_1996_2001 = np.logical_or(df['spanel'] == 1996, df['spanel'] == 2001)
conditional_2004_2008 = np.logical_or(df['spanel'] == 2004, df['spanel'] == 2008)
df['industry'] = np.nan
df.loc[conditional_1996_2001, 'industry'] = pd.cut(df.loc[conditional_1996_2001, 'TJBOCC1'], bins_1996_2001,
  labels = names_1996_2001)
df.loc[conditional_2004_2008, 'industry'] = pd.cut(df.loc[conditional_2004_2008, 'TJBOCC1'], bins_2004_2008,
  labels = names_2004_2008)
 
# Reassign
df['industry'].mask(df['industry'] == 'change_to_19', '19', inplace = True)
df['industry'].mask(df['industry'] == 'also_to_19', '19', inplace = True)
df['industry'].mask(df['industry'] == 'change_to_29', '29', inplace = True)
df['industry'].mask(df['industry'] == 'change_to_17', '17', inplace = True)
df['industry'].mask(df['industry'] == 'change_to_47', '47', inplace = True)
 
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

# Code birthmonth as stata time type and write as stata file
datetime_dict = {'birth_month': 'tm'}
df.to_stata('SIPP_Stata_Dataset.dta', convert_dates = datetime_dict)