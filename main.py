
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


df = pd.read_csv("prevalence_male_females.csv")
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)

#df.plot()  # plots all columns against index
df.plot(kind='scatter', x='Prevalence - Depressive disorders - Sex: Female - Age: Age-standardized (Percent)', y='Prevalence - Depressive disorders - Sex: Male - Age: Age-standardized (Percent)') # scatter plot
# df.plot(kind='scatter', x='Year', y='Population (historical estimates)') # scatter plot
# df.plot(kind='density')  # estimate density function
# df.plot(kind='hist')  # histogram
plt.show()



#####AGE-WISE POLOTTING#####
df = pd.read_csv('/Users/supriyajayadevhiremath/Downloads/IHME-GBD_2019_DATA_global_age/IHME-GBD_2019_DATA_global_age.csv')

# youth:'15 to 19', '20 to 24' adults: '25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64' Seniors: '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90 to 94', '95 plus'

def age(row):
    if row['age'] in ('15 to 19', '20 to 24'):
        val = 'youth'
    elif row['age'] in ('25 to 29', '30 to 34', '35 to 39','40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64'):
        val = 'adults'
    else:
        val = 'seniors'
    return val

df['age_categories'] = df.apply(age, axis=1)

to_plot = pd.pivot_table(df, index=['year'],values=['val'],columns=['age_categories'])
to_plot.plot(kind = 'line', figsize =(20,10))
