#!/usr/bin/env python
# coding: utf-8

# In[41]:
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[42]:
survey_dir = 'M:\Coding Content\Datasets\Stackoverflow\Survey2020'
survey_file_name = 'survey_results_public.csv'
schema_file_name = 'survey_results_schema.csv'


# In[43]:
df = pd.read_csv(f"{survey_dir}\\{survey_file_name}")


# In[44]:
# "Respondent" has a unique value for each survey so we can use that as index to clean up view a bit.
pd.index_col = 'Respondent'
pd.set_option('display.max_columns', 61)
pd.set_option('display.max_rows', 61)


# In[45]:
# Shows description of column names (the question that was asked for a column).
schema = pd.read_csv(f"{survey_dir}\\{schema_file_name}", index_col='Column')


# In[46]:
# Our key so we can see which columns represent which questions.
schema.sort_index()
print(schema)


# In[47]:
# Individual filters.
income = df['ConvertedComp'].between(40000, 150000)
income_wide = df['ConvertedComp'].between(10000, 150000)
usa = df['Country'] == 'United States'
age = df['Age'].between(25, 45)

ed_options = ['Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
              'Some college/university study without earning a degree',
              'Primary/elementary school',
              'I never completed any formal education']

no_degree = df['EdLevel'].isin(ed_options)

# Can use a str method just with .str, and then the method after.
# NaN entries may throw an error, so we can give them a default value with na="whatever".
python = df['LanguageWorkedWith'].str.contains('Python')

df['YearsCodePro'] = df['YearsCodePro'].replace('Less than 1 year', 0.5)
df['YearsCodePro'] = df['YearsCodePro'].replace('More than 50 years', 100)
df['YearsCodePro'] = df['YearsCodePro'].astype(float)

# Combining filters into one with '&' operator (specific to pandas in this case).
good_money = income & usa & age & python & no_degree

# Columns I want to see.
interesting_columns = ['ConvertedComp', 
                       'Age',
                       'Country',
                       'DevType', 
                       'YearsCodePro',
                       'YearsCode',
                       'WorkWeekHrs', 
                       'LanguageWorkedWith',
                       'EdLevel',
                       ]

# In[48]:
# Average between 40k to 150k a year, age 25 to 45, United States, Python, no degree.
good_money_df = df.loc[good_money, interesting_columns].sort_values('YearsCodePro')
good_money_df['ConvertedComp'].mean()


# In[49]:
# Average income with less than 3 years professional experience.
low_exp = good_money_df['YearsCodePro'] < 3
good_money_df[low_exp]['ConvertedComp'].mean()


# In[50]:
# Less than a year professional experience (brand new job).
low_exp = (good_money_df['YearsCodePro'] < 1)
good_money_df[low_exp]['ConvertedComp'].mean()


# In[51]:
# 40k to 150k a year, age 25 to 45, United States, Python, no degree, less than 1 year working.
print(good_money_df[no_degree & low_exp])


# In[52]:
# Here I'll find the average incomes of each country based on the following:
#    - Countries with 25 or more surveys taken.
#    - Between $10k to $150k annual USD converted income.
#    - Age 25 to 45.
#    - Python mentioned.
#    - No college degree.

# New combined filter.
global_money_filter = income_wide & age & python & no_degree

globe_df = df[global_money_filter]
income_results = {}
countries = globe_df['Country'].unique()
amount_of_surveys = globe_df['Country'].value_counts()

for country in countries:
    if amount_of_surveys[country] >= 25:
        country_filter = globe_df['Country'] == country
        country_df = globe_df[country_filter]
        average_income = country_df['ConvertedComp'].mean()
        # Add result to our new dictionary.
        income_results[country] = average_income

income = pd.Series(income_results, name='Income averages')
income.index.name = 'Country'
income.sort_values(inplace=True, ascending=False)
print(income)


# In[60]:
# Let's use a linear regression graph to see if there's any obvious relationship between
# age and compensation (spoiler, there is).
# Note these are results between 25-45 years old, no college degree, with mentions of Python (globe_df).
sns.set(color_codes=True)
sns.lmplot(x="Age", y="ConvertedComp", data=globe_df, x_estimator=np.mean)


# In[83]:
# Let's cast a wider net for all educations and all language combos, all countries.
# We'll limit to 100k to get rid of some outliers.
income_range = df['ConvertedComp'].between(30000, 100000)
wider_filter = income_range & age
wider_df = df[wider_filter]
sns.lmplot(x="Age", y="ConvertedComp", data=wider_df, x_estimator=np.mean, hue='Hobbyist')
# The global average seems to be between 50k up towards 75k or so as you go up in age, however..


# In[86]:
# In the US, the average is considerably higher!
us_income_range = df['ConvertedComp'].between(30000, 130000)
wider_filter = us_income_range & age & usa
wider_df = df[wider_filter]
sns.lmplot(x="Age", y="ConvertedComp", data=wider_df, hue='Hobbyist', x_estimator=np.mean)


# In[ ]:
# Interesting that people who answered "yes" to "Do you code as a hobby?" seem to earn more as they get older.


# In[87]:
# Convert notebook to .py file for backup.
# get_ipython().system('jupyter nbconvert --to script StackOverflowSurvey2020.ipynb')
