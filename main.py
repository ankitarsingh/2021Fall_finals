import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ipywidgets
from ipywidgets import interactive
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as go


def read_file(file_name):
    """
    Reads the csv
    :param file_name: csv to be read
    :return: file
    """
    return pd.read_csv(file_name)


# Interactive plot
def plot_scatter(continent):
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

    df2['location_name'].unique() # This returns global so no scope of country wise analysis

    # Bar plot
    plt.bar(val1.index, height=val1.values, color='red', width=0.5)
    plt.title("Depression based on gender")
    plt.show()

    # Grouped bar plot for multiple years
    to_plot = pd.pivot_table(df2_2017, index=['year'], values=['val'], columns=['sex'])
    plots = to_plot.plot(kind='bar', figsize=(20, 10), title='Prevalence in gender')

#############################

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
def interactive_graph(maindf: pd.DataFrame, list_to_display: list, cause_to_plot: str, region_or_category: str) -> go.Figure:
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


def __main__():
    plot_scatter()
    gender_depression_global_data()
