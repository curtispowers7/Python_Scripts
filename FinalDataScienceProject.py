#Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import random as rd
import math
import statistics as stat
import scipy
from sklearn.linear_model import LinearRegression as lm
import seaborn as sns
import re
from datetime import datetime
from datetime import timedelta
%matplotlib inline



#Import Data
data = pd.read_csv('./Cyber Security Breaches.csv', sep=',')
data.head()


#Tally Null Values
data.isnull().sum()


#Pull only the columns I want
data2 = data[['Number', 'State', 'Individuals_Affected', 'Date_of_Breach', 'Type_of_Breach', 'Location_of_Breached_Information', 'Date_Posted_or_Updated', 'year']].copy()
data2


#List data types in the rows
columns = list(data2)
typedict = {}
for column in columns:
    types = []
    for row in data2[column]:
        types.append(type(row))
    uniquetypes = set(types)
    typedict[column] = uniquetypes

for key in typedict.keys():
    print("Column Name: {0} --------- Data types in rows: {1}".format(key, typedict[key]))
    
    
    
    
#Change Date_of_Breach to a date data type
dates = []
match = re.compile('.*\-.*')
for date in data2['Date_of_Breach']:
    if re.match(match, date): 
        date = date.split('-')[0].strip()
    dates.append(date)

data2['Date_of_Breach'] = pd.to_datetime(dates, format="%m/%d/%Y")





#List data types in the rows
columns = list(data2)
typedict = {}
for column in columns:
    types = []
    for row in data2[column]:
        types.append(type(row))
    uniquetypes = set(types)
    typedict[column] = uniquetypes

for key in typedict.keys():
    print("Column Name: {0} --------- Data types in rows: {1}".format(key, typedict[key]))
    
    
    
plt.figure(figsize=(15, 5))
plt.scatter(data2['Location_of_Breached_Information'], data2['Type_of_Breach'])
plt.show()


plt.figure(figsize=(15, 5))
plt.scatter(data2['Individuals_Affected'], data2['Type_of_Breach'])
plt.show()


plt.figure(figsize=(15, 5))
plt.scatter(data2['Individuals_Affected'], data2['Location_of_Breached_Information'])
plt.show()



plt.figure(figsize=(15, 5))
plt.scatter(data2['year'], data2['Location_of_Breached_Information'])
plt.show()



plt.figure(figsize=(15, 5))
plt.scatter(data2['year'], data2['Type_of_Breach'])
plt.show()



plt.figure(figsize=(15, 5))
plt.scatter(data2['year'], data2['Individuals_Affected'])
plt.show()



#Change Type_of_Breach to numbers for categorizing and regressions
mapping = {}

counter = 0
for category in data2['Type_of_Breach']:
    if category not in mapping.keys():
        mapping[category] = counter
        counter+=1
    else:
        continue
mapping

intType_of_Breach = []
for row in data2['Type_of_Breach']:
    intType_of_Breach.append(mapping[row])

data2['intType_of_Breach'] = intType_of_Breach
data2.head()



#Change Location_of_Breached_Information to numbers for categorizing and regressions
mapping = {}

counter = 0
for category in data2['Location_of_Breached_Information']:
    if category not in mapping.keys():
        mapping[category] = counter
        counter+=1
    else:
        continue
mapping

intLocation_of_Breached_Information = []
for row in data2['Location_of_Breached_Information']:
    intLocation_of_Breached_Information.append(mapping[row])

data2['intLocation_of_Breached_Information'] = intLocation_of_Breached_Information
data2.head()




#Run a regression of Individuals_Affected vs intType_of_Breach
Type_of_Breach = ols('Individuals_Affected ~ intType_of_Breach', data=data2).fit()
Type_of_Breach.summary()



#Run a regression of Individuals_Affected vs intLocation_of_Breached_Information
Location_of_Breached_Information = ols('Individuals_Affected ~ intLocation_of_Breached_Information', data=data2).fit()
Location_of_Breached_Information.summary()



#Run a regression of Individuals_Affected vs year
year = ols('Individuals_Affected ~ year', data=data2).fit()
year.summary()



