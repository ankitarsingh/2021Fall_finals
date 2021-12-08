import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_csv("prevalence_male_females.csv")
df2 = pd.read_csv("IHME-GBD_2019_DATA.csv")

df1.head()
df2.head()

df1.plot(kind='scatter', x='Prevalence - Depressive disorders - Sex: Female - Age: Age-standardized (Percent)',
        y='Prevalence - Depressive disorders - Sex: Male - Age: Age-standardized (Percent)',
        xlabel="Prevalence in Female", ylabel="Prevalence in Male", ylim=(0,8), xlim=(0,8)) # scatter plot

# ####AGE-WISE POLOTTING#####
df_all_age = pd.read_csv('/Users/supriyajayadevhiremath/Downloads/IHME-GBD_2019_DATA_allregion_allage/IHME-GBD_2019_DATA_allregion_allage.csv')
# youth:'15 to 19', '20 to 24' adults: '25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64' Seniors: '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90 to 94', '95 plus'


def age(row):
    if row['age'] in ('15 to 19', '20 to 24'):
        val = 'youth'
    elif row['age'] in ('25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64'):
        val = 'adults'
    else:
        val = 'seniors'
    return val

df_all_age['age_categories'] = df_all_age.apply(age, axis=1)

list_of_countries = ['Europe', 'Oceania', 'Africa', 'Asia', 'United States of America']
list_of_condition = ['Major depressive disorder', 'Dysthymia', 'Bipolar disorder', 'Anxiety disorders']


def country_wise_plot(df, country: str, identifier: str):
    if identifier == 'Major depressive disorder':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Major depressive disorder')]
        to_plot = pd.pivot_table(country_df, index=['year'], values=['val'], columns=['age_categories'])
        plots = to_plot.plot(kind='line', figsize=(20, 10))
    elif identifier == 'Bipolar disorder':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Bipolar disorder')]
        to_plot = pd.pivot_table(country_df, index=['year'], values=['val'], columns=['age_categories'])
        plots = to_plot.plot(kind='line', figsize=(20, 10))
    elif identifier == 'Dysthymia':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Dysthymia')]
        to_plot = pd.pivot_table(country_df, index=['year'], values=['val'], columns=['age_categories'])
        plots = to_plot.plot(kind='line', figsize=(20, 10))
    elif identifier == 'Anxiety disorders':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Anxiety disorders')]
        to_plot = pd.pivot_table(country_df, index=['year'], values=['val'], columns=['age_categories'])
        plots = to_plot.plot(kind='line', figsize=(20, 10))
    else:
        print('Wrong input from dataframe, please check it!')


for each_country in list_of_countries:
    country_wise_plot(df_all_age, each_country, 'Major depressive disorder')

for each_country in list_of_countries:
    for each_condition in list_of_condition:
        country_wise_plot(df_all_age, each_country, each_condition)


def max_val(df_max, country, identifier):
    if identifier == 'Major depressive disorder':
        country_df = df_max[(df_max['location'] == country) & (df_max['cause'] == identifier)]
    elif identifier == 'Bipolar disorder':
        country_df = df_max[(df_max['location'] == country) & (df_max['cause'] == identifier)]
    elif identifier == 'Dysthymia':
        country_df = df_max[(df_max['location'] == country) & (df_max['cause'] == identifier)]
    elif identifier == 'Anxiety disorders':
        country_df = df_max[(df_max['location'] == country) & (df_max['cause'] == identifier)]

    values = country_df[country_df.val == country_df.val.max()]

    return values

# Plotting trend for substance use in different age groups
df2 = pd.read_csv('/Users/supriyajayadevhiremath/Downloads/IHME-GBD_2019_DATA-d3aa7862-1/IHME-GBD_2019_DATA_sub_use_drug_use_all_regions.csv')
df2['age_categories'] = df2.apply(age, axis=1)
#df2.val *= 100


def categorical_plot_drug_substance_use(df, country: str, identifier: str):
    if identifier == 'Substance use disorders':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Substance use disorders')]
        to_plot = pd.pivot_table(country_df, index=['year'], values=['val'], columns=['age_categories'])
        plots = to_plot.plot(kind='line', figsize =(20, 10), title='Prevalence of Substance use disorders in ' + country)
    elif identifier == 'Drug use disorders':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Drug use disorders')]
        to_plot = pd.pivot_table(country_df, index=['year'], values=['val'], columns=['age_categories'])
        plots = to_plot.plot(kind='line', figsize=(20, 10), title='Prevalence of Drug use disorders in ' + country)


categorical_plot_drug_substance_use(df2, 'Africa', 'Substance use disorders')
# In africa and asia substance use disorder is more prevalent in adults than in youth
# In Europe substance use disorder there is close trend of observation in youth and adults
# In USA and Oceania more prevalent in youth than in adults

categorical_plot_drug_substance_use(df2, 'United States of America', 'Drug use disorders')
# in all Regions drug use disorder is more prevalent in youth than in adults or seniors


# #Anxiety disorder and suicide rate of countries from 1990 to 2017 comparison and plotting

def read_file(file_name):
    return pd.read_csv(file_name)


def merge_data(data1, data2, join_col_name, country_code):
    data = pd.merge(data1[data1['Code'] == country_code], data2[data2['Code'] == country_code], left_on=join_col_name, right_on=join_col_name, how='left')
    return data


def plot_graph(merge_file_data, country):
    final_data = pd.DataFrame({
        'year': merge_file_data['Year'],
        'suicide_rate': merge_file_data['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)'],
        'anxiety_rate': merge_file_data['Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)']
    })
    ax = plt.gca()
    final_data.plot(x='year', y='anxiety_rate', ax=ax)
    final_data.plot(x='year', y='suicide_rate', ax=ax)
    plt.xlabel('Year')
    plt.ylabel('Percent %')
    plt.title('country: '+country)
    plt.show()


def __main__():
    anxiety_disorder_data = read_file('share-with-anxiety-disorders.csv')
    suicide_data = read_file('share-deaths-suicide.csv')

    for x in ['USA', 'AFG']:
        merge_file_data = merge_data(anxiety_disorder_data, suicide_data, 'Year', x)
        print(suicide_data)
        print(anxiety_disorder_data)
        plot_graph(merge_file_data, x)


__main__()
