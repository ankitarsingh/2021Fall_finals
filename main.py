
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


df1 = pd.read_csv("prevalence_male_females.csv")
df2 = pd.read_csv("IHME-GBD_2019_DATA.csv")

df1.head()
df2.head()

df1.plot(kind='scatter', x='Prevalence - Depressive disorders - Sex: Female - Age: Age-standardized (Percent)',
        y='Prevalence - Depressive disorders - Sex: Male - Age: Age-standardized (Percent)',
        xlabel="Prevalence in Female", ylabel="Prevalence in Male", ylim=(0,8), xlim=(0,8)) # scatter plot




#####AGE-WISE POLOTTING#####
df_all_age = pd.read_csv('/Users/supriyajayadevhiremath/Downloads/IHME-GBD_2019_DATA_allregion_allage/IHME-GBD_2019_DATA_allregion_allage.csv')
# youth:'15 to 19', '20 to 24' adults: '25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64' Seniors: '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90 to 94', '95 plus'

def age(row):
    if row['age'] in ('15 to 19', '20 to 24'):
        val = 'youth'
    elif row['age'] in ('25 to 29', '30 to 34', '35 to 39','40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64'):
        val = 'adults'
    else:
        val = 'seniors'
    return val

df_all_age['age_categories'] = df_all_age.apply(age, axis=1)

list_of_countries = ['Europe', 'Oceania', 'Africa', 'Asia', 'United States of America']
countries_list = np.array(list_of_countries)
countries_list.sort()

def country_wise_plot(df, country: str, identifier: str):
    if identifier == 'Major depressive disorder':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Major depressive disorder')]
        to_plot = pd.pivot_table(country_df, index=['year'],values=['val'],columns=['age_categories'])
        plots = to_plot.plot(kind = 'line', figsize =(20,10))
    elif identifie == 'Bipolar disorder':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Bipolar disorder')]
        to_plot = pd.pivot_table(country_df, index=['year'],values=['val'],columns=['age_categories'])
        plots = to_plot.plot(kind = 'line', figsize =(20,10))
    elif identifier == 'Dysthymia':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Dysthymia')]
        to_plot = pd.pivot_table(country_df, index=['year'],values=['val'],columns=['age_categories'])
        plots = to_plot.plot(kind = 'line', figsize =(20,10))
    elif identifier == 'Anxiety disorders':
        country_df = df[(df['location'] == country) & (df['cause'] == 'Anxiety disorders')]
        to_plot = pd.pivot_table(country_df, index=['year'],values=['val'],columns=['age_categories'])
        plots = to_plot.plot(kind = 'line', figsize =(20,10))
    return plots


country_wise_plot(df_all_age, 'Europe','Major depressive disorder')


##Anxiety disorder and suicide rate of countries from 1990 to 2017 comparison and plotting

def read_file(file_name):
    return pd.read_csv(file_name)


def merge_data(data1, data2, join_col_name, country_code):
    data = pd.merge(data1[data1['Code'] == country_code], data2[data2['Code'] == country_code], left_on=join_col_name, right_on=join_col_name, how='left')
    return data
