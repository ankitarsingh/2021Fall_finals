
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("prevalence_male_females.csv")
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)

#df.plot()  # plots all columns against index
df.plot(kind='scatter', x='Prevalence - Depressive disorders - Sex: Female - Age: Age-standardized (Percent)', y='Prevalence - Depressive disorders - Sex: Male - Age: Age-standardized (Percent)') # scatter plot
# df.plot(kind='scatter', x='Year', y='Population (historical estimates)') # scatter plot
# df.plot(kind='density')  # estimate density function
# df.plot(kind='hist')  # histogram
plt.show()
