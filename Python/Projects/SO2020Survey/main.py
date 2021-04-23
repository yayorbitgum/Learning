# Jupyter Notebook reference for "StackOverflowSurvey2020.ipynb".
#
# Breaking down a StackOverflow 2020 survey database to find information on
# average compensation depending on location, experience, education, etc.
# Most interested in compensation with little professional experience, with no degree, working in US.
# Very interesting answers once outliers and possibly fake data are excluded.
#
# So far, I'm checking for:
#   - 40k-150k converted annual compensation,
#   - age 25-45,
#   - United States,
#   - include Python experience,
#   - no college degree.
#
# I can have pycharm build this page automatically if I pay for pro and get
# jupyter built in support apparently lol. Sounds great but how expensive? Ah the real question.

import pandas as pd

survey_dir = 'M:\Coding Content\Datasets\Stackoverflow\Survey2020'
survey_file_name = 'survey_results_public.csv'
schema_file_name = 'survey_results_schema.csv'

df = pd.read_csv(f"{survey_dir}\\{survey_file_name}")

# "Respondent" has a unique value for each survey so we can use that as index to clean up view a bit.
pd.index_col = 'Respondent'
pd.set_option('display.max_columns', 61)
pd.set_option('display.max_rows', 61)

# Schema shows description of column names (the question that was asked for a column).
schema = pd.read_csv(f"{survey_dir}\\{schema_file_name}", index_col='Column')

# Clean up ---------------------------------------------------------------------
# Mixed data types meant I couldn't sort. I can represent the far ends like this.
df['YearsCodePro'] = df['YearsCodePro'].replace('Less than 1 year', 0.5)
df['YearsCodePro'] = df['YearsCodePro'].replace('More than 50 years', 100)
# Everything else was integers, but I wanna represent less than 1 year as 0.5.
# Pandas/numpy won't compare int to float, so I'll make everything a float in this column.
df['YearsCodePro'] = df['YearsCodePro'].astype(float)

# Filters ----------------------------------------------------------------------
income = df['ConvertedComp'].between(40000, 150000)
usa = df['Country'] == 'United States'
age = df['Age'].between(25, 45)
python = df['LanguageWorkedWith'].str.contains('Python')

ed_options = ['Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
              'Some college/university study without earning a degree',
              'Primary/elementary school',
              'I never completed any formal education']

no_degree = df['EdLevel'].isin(ed_options)

combined_filters = income & usa & age & python & no_degree

interesting_columns = ['ConvertedComp',
                       'Age',
                       'DevType',
                       'YearsCodePro',
                       'YearsCode',
                       'WorkWeekHrs',
                       'LanguageWorkedWith',
                       'EdLevel',
                       ]

# Checking results -------------------------------------------------------------
# Average between 40k to 150k a year, age 25 to 45, United States, include Python, no degree.
good_money_df = df.loc[combined_filters, interesting_columns].sort_values('YearsCodePro')
print(good_money_df['ConvertedComp'].mean())

# Less than 3 years professional experience.
low_exp = good_money_df['YearsCodePro'] < 3
print(good_money_df[low_exp]['ConvertedComp'].mean())

# Less than a year professional experience.
low_exp = (good_money_df['YearsCodePro'] < 1)
print(good_money_df[low_exp]['ConvertedComp'].mean())

print(good_money_df[low_exp])