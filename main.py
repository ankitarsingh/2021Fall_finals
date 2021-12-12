# Final Project For Analysis on Depression disorders.
# Group members: Ankita Singh(arsingh3), Brijesh Taunk(btaunk2), Supriya Jayadev Hiremath(sjh6)
# Distribution of work:
# Ankita Singh: Analysis 1
# Supriya Jayadev Hiremath: Analysis 2
# Brijesh Taunk: Analysis 3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets
from ipywidgets import interactive
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as go


################################ ANALYSIS 1 ############################
def read_file(file_name):
    """
    Reads the csv
    :param file_name: csv to be read
    :return: file
    """
    return pd.read_csv(file_name)


# Interactive plot
def plot_scatter(continent):
    """
    Reads the csv file from 2 data sources and merges them to craete a scatter plot that can be further
    customized according to country using drop down.
    """
    df1 = read_file("prevalence_male_females.csv")
    df_continents = read_file("continents2.csv")
    df1.dropna()
    # Renaming the columns
    df1 = df1.rename(columns={'Prevalence - Depressive disorders - Sex: Male - Age: Age-standardized (Percent)': 'Male',
                              'Prevalence - Depressive disorders - Sex: Female - Age: Age-standardized (Percent)': 'Female'})
    # Filtering the data for one year as mentioned in the article
    df_2017 = df1[df1["Year"] == 2017]

    # Merging df_2017 with df_continents for continents correspinding to country code
    result = pd.merge(df_2017, df_continents, how="left")
    result['region'] = result['region'].replace(np.nan, 'Others')
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
    plt.show()

    # Creating an interactive plot using 'interactive' function with all the necessary dropdowns
    plot1 = interactive(plot_scatter,
                        continent=ipywidgets.Dropdown(
                            value='All',
                            options=['All', 'Asia', 'Others', 'Europe', 'Africa', 'Oceania', 'Americas'],
                            description='Continent'
                        ))
    plot1


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

    df2['location_name'].unique()  # This returns global so no scope of country wise analysis

    # Bar plot
    plt.bar(val1.index, height=val1.values, color='red', width=0.5)
    plt.title("Depression based on gender")
    plt.show()

    # Grouped bar plot for multiple years
    to_plot = pd.pivot_table(df2_2017, index=['year'], values=['val'], columns=['sex'])
    plots = to_plot.plot(kind='bar', figsize=(20, 10), title='Prevalence in gender')


################################ ANALYSIS 2 ############################
def age(row: pd.Series) -> str:
    """ Using the below mentioned source:
    https://www.statcan.gc.ca/en/concepts/definitions/age2 as our standard to define a certain range of
    age as youth or adults or seniors.
    Function 'age' defined below is used to categorize age ranges present in original data set
    into a particular age group as follows:-
    1) youth:'15 to 19', '20 to 24'
    2) adults: '25 to 29', '30 to 34', '35 to 39','40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64'
    3) Seniors: '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89','90 to 94', '95 plus'
    We get a row from source data frame as input which is a pd.Series datatype and
    if else statements in this function checks for all three conditions youth, adults and seniors and assigns
    repective age category to the age_categories column of the source dataframe.
        :param row: pd.Series: a pandas series from source dataframe df_main.
        :return: str: a value of string datatype which defines age category of
        the number present in age column of input series.
        >>> a = pd.Series(['Global','Both','80 to 84','Major depressive disorder','1990','4.013462'])
        >>> a.index = ['location', 'sex', 'age', 'cause', 'year','val']
        >>> age_category = age(a)
        >>> print(age_category)
        seniors
        >>> a1 = pd.Series(['Asia','Both','15 to 19','Major depressive disorder','1990','4.013462'])
        >>> a1.index = ['location', 'sex', 'age', 'cause', 'year','val']
        >>> age_category1 = age(a1)
        >>> print(age_category1)
        youth
        >>> a2 = pd.Series(['Africa','Both','30 to 34','Major depressive disorder','1990','4.013462'])
        >>> a2.index = ['location','sex', 'age', 'cause', 'year','val']
        >>> age_category2 = age(a2)
        >>> print(age_category2)
        adults
        >>> a3 = pd.Series(['Europe','Both','32 to 31','Major depressive disorder','1990','4.013462'])
        >>> a3.index = ['location', 'sex', 'age', 'cause', 'year','val']
        >>> age_category3 = age(a3)
        Traceback (most recent call last):
        UnboundLocalError: local variable 'category' referenced before assignment
        """
    try:
        if row['age'] in ('15 to 19', '20 to 24'):
            category = 'youth'
        elif row['age'] in ('25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59',
                            '60 to 64'):
            category = 'adults'
        elif row['age'] in ('65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90 to 94', '95 plus'):
            category = 'seniors'
    except UnboundLocalError:
        print('Data set has age group that is not required for computation, please re-check the dataset.')
    return category


# Reference from DATAPANE site https://docs.datapane.com/examples-and-tutorials/interactive-filters#plotly-1
def interactive_graph(maindf: pd.DataFrame, list_to_display: list, cause_to_plot: str,
                      region_or_category: str) -> go.Figure:
    """
    This function takes in dataframe which has mean values for each age category
    corresponding to every mental health and for all regions present in our source dataframe
    and plots graph displaying prevalence of mental health condition in every region over the time
    in particular age group.
    :param maindf:pd.DataFrame: main_df dataframe
    :param list_to_display:list: list of regions/age_groups to plot.
    :param cause_to_plot: string input of mental health condition to be plotted.
    :param region_or_category: string input of region/age group.
    :return: go.Figure: (interactive graph)
    >>> vals = [['Asia', 'Major depressive disorder', '2001', '3.8','adults'],\
                  ['Africa', 'Major depressive disorder', '2001', '5','seniors'],\
                  ['United States of America', 'Major depressive disorder', '2001', '1.2','youth'],\
                  ['Europe', 'Major depressive disorder', '2016', '4','seniors']]
    >>> df_test = pd.DataFrame(vals, columns = ['location', 'cause','year','val','age_categories'])
    >>> region_list = ['Asia', 'Africa','Europe','United States of America']
    >>> a = 'Major depressive disorder'
    >>> b = 'seniors'
    >>> result = interactive_graph(df_test, region_list, a, b)
    >>> result # doctest: +ELLIPSIS
    Figure({
        'data': [{'name': 'Africa',...
                   'yaxis': {'title': {'text': 'PREVALENCE'}}}
    })
    """
    final_plot = go.Figure()
    list_of_countries = ['Asia', 'Europe', 'Africa']
    list_of_countries.sort()
    list_to_display.sort()

    if list_of_countries == list_to_display:
        for country in list_to_display:
            df_to_plot = maindf[(maindf['location'] == country) & (maindf['cause'] == cause_to_plot)
                                & (maindf['age_categories'] == region_or_category)]
            final_plot.add_trace(
                go.Scatter(
                    x=df_to_plot['year'][df_to_plot['location'] == country],
                    y=df_to_plot['val'][df_to_plot['location'] == country],
                    name=country, visible=True
                )
            )
    else:
        for group in list_to_display:
            df_to_plot = maindf[(maindf['location'] == region_or_category) & (maindf['cause'] == cause_to_plot)
                                & (maindf['age_categories'] == group)]
            final_plot.add_trace(
                go.Scatter(
                    x=df_to_plot['year'][df_to_plot['age_categories'] == group],
                    y=df_to_plot['val'][df_to_plot['age_categories'] == group],
                    name=group, visible=True
                )
            )

    buttons = []

    for i, each_val in enumerate(list_to_display):
        args = [False] * len(list_to_display)
        args[i] = True

        button = dict(label=each_val,
                      method="restyle",
                      args=[{"visible": args}])

        buttons.append(button)

        final_plot.update_layout(
            updatemenus=[dict(
                active=0,
                type="dropdown",
                buttons=buttons,
                x=0.0,
                y=1.0,
                xanchor='right',
                yanchor='top'
            )],
            title="PREVELANCE OF " + cause_to_plot.upper() + " IN " + region_or_category.upper(),
            title_x=0.6,
            xaxis_title="YEAR",
            yaxis_title="PREVALENCE",
            autosize=False,
            width=1000,
            height=800,
            xaxis1_rangeslider_visible=True
        )

    return final_plot


def max_val(df_max: pd.DataFrame, country: str, identifier: str) -> pd.DataFrame:
    """
     This function takes in source dataframe and prints maximum values
     for every mental health condition for every country
     :param df_max: source dataframe
     :param country: required country string input to excute for that particular country
     :param identifier: Taking in string input Identifier to execute for particular mental health condition
     :return: returns a dataframe of a row showing maximum value for the entered parameters.
     >>> vals = [['Asia', 'Major depressive disorder', '2001', '3.8','adults'],\
                  ['Asia', 'Major depressive disorder', '2001', '5','seniors'],\
                  ['Asia', 'Major depressive disorder', '2001', '1.2','youth'],\
                  ['Africa', 'Major depressive disorder', '2016', '4','seniors']]
     >>> test_df = pd.DataFrame(vals, columns = ['location', 'cause', 'year' , 'val', 'age'])
     >>> c = 'Asia'
     >>> id_test = 'Major depressive disorder'
     >>> max_val(test_df, c,id_test)
       location                      cause  year val      age
     1     Asia  Major depressive disorder  2001   5  seniors
     """
    if identifier in ('Major depressive disorder', 'Bipolar disorder', 'Dysthymia', 'Anxiety disorders'):
        country_df = df_max[(df_max['location'] == country) & (df_max['cause'] == identifier)]
    else:
        print("Function call has country and identifier not used in our data analysis")
    values = country_df[country_df.val == country_df.val.max()]
    return values


def compute(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates new column in source dataframe called 'age_categories' using 'age' function and
    multiplies val coloumn with 100 as the original dataset value got divided by 100 while downloading.

    Since original data set has age groups(ex: 15 to 19), and in source dataframe each group was assigned to
    it's corresponding category either as youth, adults or seniors.
    So there are various values for one age category for every mental health condiiton.
    To perform analysis, this function also calculates mean value of these rows so that every category has
    one average value for every disorder.
    :param df:pd.DataFrame: source dataframe with no age category column.
    :return: Dataframe with age category column and val column divided by 100.
     >>> vals1 = [['Africa', 'Major depressive disorder', 2001, 3.8,'15 to 19'],\
               ['Africa', 'Major depressive disorder', 2001, 5.6,'20 to 24'],\
               ['Africa', 'Major depressive disorder', 2001, 1.23,'60 to 64'],\
               ['Africa', 'Major depressive disorder', 2001, 4.1,'15 to 19']]
     >>> test_df1 = pd.DataFrame(vals1, columns = ['location', 'cause', 'year' , 'val', 'age'])
     >>> compute(test_df1)
        year location                      cause age_categories    val
     0  2001   Africa  Major depressive disorder         adults  123.0
     1  2001   Africa  Major depressive disorder          youth  450.0
     >>> vals2 = 23
     >>> compute(vals2)
     Traceback (most recent call last):
     AttributeError: Input has to be a dataframe.
    """
    if type(df) != pd.DataFrame:
        raise AttributeError('Input has to be a dataframe.')
    elif 'age_categories' not in df.columns:
        df['age_categories'] = df.apply(age, axis=1)
        df.val *= 100
    else:
        print('Computation has already been performed please check or import the data file again')
    df2 = df.groupby(by=['year', 'location', 'cause', 'age_categories']).agg({'val': 'mean'}).reset_index()
    return df2



################################ ANALYSIS 3 ############################

def merge_data(data1, data2, join_col_name, country_code):
    """" Merges 2 datasets using a common column i.e. country_code. Uses left join and returns a merged table """
    data = pd.merge(data1[data1['Code'] == country_code], data2[data2['Code'] == country_code], left_on=join_col_name,
                    right_on=join_col_name, how='left')
    return data


def plot_graph(merge_file_data, country):
    """
     Uses the merged data and builds the line graph and correlation plot of anxiety_rate and suicide_rate of every
     country.
     Uses 2 parameters, merge_file_data and country.
     The function takes values from merged dataset. It gives error from the except block if any string is passed instead
     of integer in anxiety or suicide rate value.

    :param merge_file_data: pd.dataframe: source dataframe with all the countries and their anxiety rates and
    suicide rates.
    :param country: string input to help plot for that one country from the dataset.
    >>> values = [[0.45059409, 4.831408829,'2001']]
    >>> df = pd.DataFrame(values, columns = ['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)','Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)','Year'])
    >>> c = 'AFG'
    >>> plot_graph(df,c)

    >>> values = [['kk', 4.831408829,'2001']]
    >>> df = pd.DataFrame(values, columns = ['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)','Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)','Year'])
    >>> c = 'AFG'
    >>> plot_graph(df,c)
    Getting string data instead of integer

    >>> values = [[0.562432741, 'abc','2007']]
    >>> df = pd.DataFrame(values, columns = ['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)', 'Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)','Year'])
    >>> c = 'AFG'
    >>> plot_graph(df,c)
    Getting string data instead of integer

    >>> values = [[0.751, 2.344,'2009']]
    >>> df = pd.DataFrame(values, columns = ['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)', 'Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)','Year'])
    >>> c = 'AFG'
    >>> plot_graph(df,c)
    """
    try:
        final_data = pd.DataFrame({
            'year': merge_file_data['Year'],
            'suicide_rate': merge_file_data['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)'],
            'anxiety_rate': merge_file_data[
                'Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)']
        })
        ax = plt.gca()
        final_data.plot(x='year', y='anxiety_rate', ax=ax)
        final_data.plot(x='year', y='suicide_rate', ax=ax)
        plt.xlabel('Year')
        plt.ylabel('Percent %')
        plt.title('Country: ' + country)
        plt.show()
        data = {'anxiety_rate': merge_file_data[
            'Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)'],
                'suicide_rate': merge_file_data['Deaths - Self-harm - Sex: Both - Age: All Ages (Percent)']
                }
        df = pd.DataFrame(data, columns=['anxiety_rate', 'suicide_rate'])

        # Correlation plot
        corrplot_matrix = df.corr()
        sn.heatmap(corrplot_matrix, annot=True)
        plt.title('Country: ' + country)
        plt.show()

    except TypeError:
        print('Getting string data instead of integer')


def __main__():
    """ The function reads 2 dataset files and runs a loop in a modifiable list of countries using country codes i.e.
        the country codes can be added and removed from the list and the graphs for the new list will be plotted. """
    plot_scatter()
    gender_depression_global_data()


    anxiety_disorder_data = read_file('share-with-anxiety-disorders.csv')
    suicide_data = read_file('share-deaths-suicide.csv')

    for x in ['USA', 'AFG', 'ALB', 'DZA', 'ASM', 'AND', 'AGO', 'ATG', 'ARG', 'ARM', 'AUS', 'AUT', 'AZE', 'BHS', 'BHR']:
        merge_file_data = merge_data(anxiety_disorder_data, suicide_data, 'Year', x)
        plot_graph(merge_file_data, x)
    print(suicide_data.head())
    print(anxiety_disorder_data.head())
    print(suicide_data)
    print(anxiety_disorder_data)
    df_global = read_file('IHME-GBD_2019_DATA_global.csv')
    df_five_region = read_file('IHME-GBD_2019_DATA_allregion_allage.csv')
    df_SD_use = read_file('IHME-GBD_2019_DATA_sub_use_drug_use_all_regions.csv')
    df_socialmedia = read_file('social media usage.csv')

    print('There are {} missing values in our five region dataframe'.format(df_five_region.isna().sum().sum()))
    print('There are {} missing values in our global dataframe'.format(df_global.isna().sum().sum()))

    to_concat = [df_global, df_five_region]
    df_noagecat = pd.concat(to_concat)
    main_df = compute(df_noagecat)
    df_substance_and_drug_use = compute(df_SD_use)
    df_five_regions = compute(df_five_region)
    list_of_countries = list(main_df['location'].unique())
    list_of_condition = list(main_df['cause'].unique())
    list_of_age_groups = list(main_df['age_categories'].unique())

    df_depression = df_five_regions[(df_five_regions['cause'] == 'Major depressive disorder')]
    main_df_depression = df_depression.groupby(by=['location']).agg({'val': 'mean'}).reset_index()

    fig_depression = px.bar(main_df_depression, x='location', y='val',
                            title="PREVALENCE OF DEPRESSION IN FIVE MAIN REGIONS",
                            labels={"val": "Prevalence(c%)",
                                    "location": "Region",
                                    }
                            )
    fig_depression.show()

    main_df_all = df_five_regions.groupby(by=['location']).agg({'val': 'mean'}).reset_index()

    fig_all_disorders = px.bar(main_df_all, x='location', y='val',
                               title="PREVALENCE OF MENTAL HEALTH DISORDERS IN FIVE MAIN REGIONS",
                               labels={"val": "Prevalence(c%)",
                                       "location": "Region",
                                       }
                               )
    fig_all_disorders.show()

    interactive_graph(main_df, list_of_age_groups, 'Major depressive disorder',
                      'United States of America')
    interactive_graph(main_df, list_of_age_groups, 'Major depressive disorder', 'Oceania')
    interactive_graph(main_df, list_of_age_groups, 'Major depressive disorder', 'Asia')
    interactive_graph(main_df, list_of_age_groups, 'Major depressive disorder', 'Global')

    for each_country in list_of_countries:
        for condition in list_of_condition:
            value_df = max_val(main_df, each_country, condition)
            country = (list(value_df['location']))
            age_group = (list(value_df['age_categories']))
            cause = (list(value_df['cause']))
            max_value = (list(value_df['val']))
            print('{} : Maximum percent of prevalance for {} condition'
                  ' in {} agegroup is {: .2f}'.format(country[0],
                                                      cause[0], age_group[0], max_value[0]), '\n')

    interactive_graph(df_substance_and_drug_use, list_of_age_groups, 'Substance use disorders',
                      'United States of America')
    interactive_graph(df_substance_and_drug_use, list_of_age_groups, 'Drug use disorders', 'United States of America')
    interactive_graph(df_substance_and_drug_use, list_of_age_groups, 'Substance use disorders',
                      'Oceania')
    interactive_graph(df_substance_and_drug_use, list_of_age_groups, 'Drug use disorders', 'Oceania')
    interactive_graph(df_substance_and_drug_use, list_of_countries, 'Substance use disorders', 'youth')
    interactive_graph(df_substance_and_drug_use, list_of_countries, 'Drug use disorders', 'youth')

    df_socialmedia['date'] = pd.to_datetime(df_socialmedia['Unnamed: 0'], format='%m/%d/%y')
    df_socialmedia['year'] = pd.DatetimeIndex(df_socialmedia['date']).year
    df_social_media = df_socialmedia[['year', '18-29', '30-49', '50-64', '65+']]

    # Referenced from https://pandas.pydata.org/docs/reference/api/pandas.melt.html
    df_new = pd.melt(df_social_media, id_vars="year", var_name="age_groups", value_name="percent_usage")
    df_new['percent_usage'] = df_new['percent_usage'].map(lambda x: x.rstrip('%'))
    df_new['percent_usage'] = df_new['percent_usage'].astype(str).astype(int)
    trend_plot = sn.relplot(data=df_new, x="year", y="percent_usage", hue="age_groups", kind="line", height=10,
                             aspect=2)




__main__()