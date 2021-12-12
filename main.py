
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets
from ipywidgets import interactive


def read_file(file_name):
    """
    Reads the csv
    :param file_name: csv to be read
    :return: file
    """
    return pd.read_csv(file_name)


def gender_depression_original_data():
    """
    Reads csv file from the article's source and another one from global health data. We replicate the scatter
    plot in the article which shows that depression is more prevalent in females compared to males in year 2017.
    We check the same for the second dataset using a bar plot
    """

    df1 = read_file("prevalence_male_females.csv")
    df_continents = read_file("continents2.csv")
    df1.dropna()
    # Renaming the columns
    df1 = df1.rename(columns={'Prevalence - Depressive disorders - Sex: Male - Age: Age-standardized (Percent)':'Male',
                              'Prevalence - Depressive disorders - Sex: Female - Age: Age-standardized (Percent)':'Female'})
    # Filtering the data for one year as mentioned in the article
    df_2017 = df1[df1["Year"] == 2017]

    #Merging df_2017 with df_continents for continents correspinding to country code
    result = pd.merge(df_2017, df_continents, how="left")
    result['region'] = result['region'].replace(np.nan, 'Others')

    # Interactive plot
    def plot_scatter(continent):
        if continent == 'All':
            result.plot(kind='scatter', x='Female', y='Male', ylim=(0, 8), xlim=(0, 8),
                        figsize=(20, 10))  # scatter plot
        else:
            df_temp = result[result['region'] == continent]
            df_temp.plot(kind='scatter', x='Female', y='Male', ylim=(0, 8), xlim=(0, 8),
                         figsize=(20, 10))  # scatter plot
        plt.xlabel('Prevelance in Female')
        plt.ylabel('Prevelance in Male')
        plt.title('Prevalence in gender')
        #plt.show()

    # Creating an interactive plot using 'interactive' function with all the necessary dropdowns
    plot1 = interactive(plot_scatter,
                        continent=ipywidgets.Dropdown(
                            value='All',
                            options=['All', 'Asia', 'Others', 'Europe', 'Africa', 'Oceania', 'Americas'],
                            description='Continent'
                        ))


def gender_depression_global_data():
    """
    Reads csv from the global health data and then checks the depression score for male vs females by aggregating them
    and also plotting a bar chart for the same.
    """
    df2 = read_file("GHD_male_female.csv")
    df2.dropna()
    # Creates a pivot table dataframe
    table = pd.pivot_table(df2, values='val', columns=['sex_name'], aggfunc=np.sum)
    print(table)

    df2_2017 = df2[df2["year"] == 2017]
    val1 = df2_2017.groupby(['sex_name'])['val'].mean()

    df2['location_name'].unique() # This returns global so no scope of country wise analysis

    # Bar plot
    plt.bar(val1.index, height=val1.values, color='red', width=0.5)
    plt.title("Depression based on gender")
    plt.show()

    # Grouped bar plot for multiple years
    to_plot = pd.pivot_table(df2_2017, index=['year'], values=['val'], columns=['sex'])
    plots = to_plot.plot(kind='bar', figsize=(20, 10), title='Prevalence in gender')


def __main__():
    gender_depression_original_data()
    gender_depression_global_data()
