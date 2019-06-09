# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:01:34 2019

@author: Alex
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('D:/Users/Alex/Git_Repositories/Thesis')

# Education summary statistics
df = pd.read_pickle('SIPP_Dataset_3')
df.sort_values(['unique_id','ref_date'])
education_counts = df.groupby('unique_id').last()['eeducate'].value_counts(sort = False)
fig, ax = plt.subplots()
ax.bar(education_counts.index, education_counts)
ax.set_xticks(education_counts.index)
ax.set_title('Sample Distribution of Education Level')
ax.set_ylabel('Counts')
plt.show()

print('''
31  Less Than 1st Grade
32  1st, 2nd, 3rd or 4th grade
33  5th Or 6th Grade
34  7th Or 8th Grade
35  9th Grade
36  10th Grade
37  11th Grade
38  12th grade, no diploma
39  High School Graduate - (diploma or GED or equivalent)
40  Some college, but no degree
41  Diploma or certificate from a vocational, technical, trade or business school beyond high
43  Associate (2-yr) college degree (include academic/occupational degree)
44  Bachelor's degree (for example: BA, AB, BS)
45  Master's degree (For example: MA, MS, MEng, MEd, MSW, MBA)
46  Professional School degree (for example: MD(doctor),DDS(dentist),JD(lawyer)
47  Doctorate degree (for example: Ph.D., Ed.D)''')

