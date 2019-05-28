# -*- coding: utf-8 -*-
"""
Created on Sun May 19 14:42:44 2019

@author: Alex
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')

df = pd.read_csv('SIPP_CSV_Dataset.csv')

# Create value counts of employment status
rmesr_value_counts = df['rmesr'].value_counts()

# Plot employment status
fig, ax = plt.subplots()
ax.bar(rmesr_value_counts.index, rmesr_value_counts)
ax.set_ylabel('Counts')
ax.set_title('Employment Status Counts of Sample')
plt.show()

print('1  With a job entire month, worked all weeks.')
print('2  With a job entire month, absent from work without pay 1+ weeks, absence not due to layoff')
print('3  With a job entire month, absent from work without pay 1+ weeks, absence due to layoff')
print('4  With a job at least 1 but not all weeks, no time on layoff and no time looking for work')
print('5  With a job at least 1 but not all weeks, remaining weeks on layoff or looking for work')
print('6  No job all month, on layoff or looking for work all weeks.')
print('7  No job all month, at least one but not all weeks on layoff or looking for work')
print('8  No job all month, at least one but not all weeks on layoff or looking for work')

df2 = pd.read_stata('US_Paid_leave_analysis_altered.dta')

df2.groupby(['spanel', 'swave', 'srefmon'])

# To do: 
#   groupby 
#   plot distributions of time invariant variables:
#       education (eeducate)
#       top 20 industry bins (TJBOCC1)
#       