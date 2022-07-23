#!/usr/bin/env python
# coding: utf-8

# In[1]:


#IMPORTS
#For offline plotting
from plotly.offline import plot,iplot, init_notebook_mode

#Basics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

#hide warnings
import warnings
warnings.filterwarnings('ignore')


# In[2]:


total_data = pd.read_csv('../Data/Cleaned_Final_Global_Data.csv',parse_dates=['Date'])
# total_data.head()
# total_data.sample(6)
# total_data.info()
# Dates converted to date time object


# In[3]:


total_data['Active'] = total_data['Confirmed']-total_data['Recovered']-total_data['Deaths']


# In[4]:


# total_data.isna().sum()
#Fill missing values
total_data['Province/State'] = total_data['Province/State'].fillna('')
# print(total_data.isna().sum())


# In[5]:


full_grouped = total_data.groupby(['Date','Country/Region'])['Confirmed','Deaths','Recovered','Active'].sum().reset_index()
# full_grouped
temp = full_grouped.groupby(['Country/Region','Date'])['Confirmed','Deaths','Recovered'].sum().diff().reset_index()
# temp
incon = (temp['Country/Region'] != temp['Country/Region'].shift(1))
temp.loc[incon,'Confirmed'] = np.nan
temp.loc[incon,'Deaths'] = np.nan
temp.loc[incon,'Recovered'] = np.nan
#This sets the values of differences of the first day to nan
#Now set the new columns
# temp
temp.columns = ['Country/Region','Date','New Confirmed','New Deaths','New Recovered']
# temp
full_grouped = pd.merge(full_grouped,temp,on=['Country/Region','Date'])
# print(full_grouped)
# as visible, for the first date, all new cases are Nan. Fill with 0
full_grouped = full_grouped.fillna(0)
# full_grouped.info()
#They are coming as float. Make int
full_grouped[['New Confirmed','New Deaths','New Recovered']] = full_grouped[['New Confirmed','New Deaths','New Recovered']].astype('int')
# If difference goes negative, we make it 0
full_grouped['New Confirmed'] = full_grouped['New Confirmed'].apply(lambda x: 0 if x<0 else x)
# full_grouped


# In[6]:


# Now we create new data frames for different kinds of analysis
# DAY_WISE
day_wise = full_grouped.groupby('Date')['Confirmed','Deaths','Recovered','New Confirmed','New Deaths','New Recovered'].sum().reset_index()
# day_wise
# NUM COUNTRIES
day_wise['No. of countries'] = full_grouped[full_grouped['Confirmed']!=0].groupby('Date')['Country/Region'].unique().apply(len).values
# day_wise
# We see how the number of countries have increased with time
#Number cases per 100 cases
day_wise['Deaths / 100 Cases'] = round((day_wise['Deaths']/day_wise['Confirmed'])*100, 2)
day_wise['Deaths / 100 Cases'] = round((day_wise['Recovered']/day_wise['Confirmed'])*100, 2)
day_wise['Deaths / 100 Recovered'] = round((day_wise['Deaths']/day_wise['Recovered'])*100, 2)
# day_wise
day_wise[['Deaths / 100 Cases','Deaths / 100 Cases','Deaths / 100 Recovered']] = day_wise[['Deaths / 100 Cases','Deaths / 100 Cases','Deaths / 100 Recovered']].fillna(0)
# day_wise.isna().sum() Perfect
# day_wise


# In[7]:


#Country Wise
country_wise = full_grouped[full_grouped['Date']==max(full_grouped['Date'])].reset_index(drop=True).drop('Date', axis=1)
# country_wise


# In[8]:


country_wise = country_wise.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active', 'New Confirmed', 'New Recovered','New Deaths'].sum().reset_index()
# country_wise
country_wise['Deaths / 100 Cases'] = round((country_wise['Deaths']/country_wise['Confirmed'])*100, 2)
country_wise['Recovered / 100 Cases'] = round((country_wise['Recovered']/country_wise['Confirmed'])*100, 2)
country_wise['Deaths / 100 Recovered'] = round((country_wise['Deaths']/country_wise['Recovered'])*100, 2)
# country_wise
country_wise[['Deaths / 100 Cases','Recovered / 100 Cases','Deaths / 100 Recovered']] = country_wise[['Deaths / 100 Cases','Recovered / 100 Cases','Deaths / 100 Recovered']].fillna(0)
# country_wise.isna().sum() Perfect
# country_wise.head()


# In[9]:


population = pd.read_csv('../Static/population_by_country_2020.csv')
population = population.iloc[:,:2]
population.columns = ['Country/Region','Population']
# country_wise[country_wise['Country/Region']=='China']
country_wise = pd.merge(country_wise,population,on='Country/Region',how='left')


# In[10]:


# country_wise[country_wise['Population'].isna()]
# 15 values for which population not known. Updated from other sources.
cols = ['Burma', 'Congo (Brazzaville)', 'Congo (Kinshasa)', "Cote d'Ivoire", 'Czechia', 
        'Kosovo', 'Saint Kitts and Nevis', 'Saint Vincent and the Grenadines', 
        'Taiwan*', 'US', 'West Bank and Gaza']
pops = [54409800, 89561403, 5518087, 26378274, 10708981, 1793000, 
        53109, 110854, 23806638, 330541757, 4543126]
for c, p in zip(cols, pops):
    country_wise.loc[country_wise['Country/Region']== c, 'Population'] = p
# country_wise[country_wise['Population'].isna()]
# Not getting values for other 4 countries


# In[11]:


country_wise['Cases / Million People'] = round((country_wise['Confirmed'] / country_wise['Population']) * 1000000)
# country_wise.head()


# In[12]:


# FInding immediate values
today = full_grouped[full_grouped['Date']==max(full_grouped['Date'])].reset_index(drop=True).drop('Date', axis=1)[['Country/Region', 'Confirmed']]
last_week = full_grouped[full_grouped['Date']==max(full_grouped['Date'])-timedelta(days=7)].reset_index(drop=True).drop('Date', axis=1)[['Country/Region', 'Confirmed']]

temp = pd.merge(today, last_week, on='Country/Region', suffixes=(' today', ' last week'))
# temp
temp['1 week change'] = temp['Confirmed today'] - temp['Confirmed last week']
# temp
country_wise = pd.merge(country_wise, temp, on='Country/Region')
# country_wise['1 week % increase'] = round(country_wise['1 week change']/country_wise['Confirmed last week']*100, 2)


# In[13]:


country_wise['1 week % increase'] = round(country_wise['1 week change']/country_wise['Confirmed last week']*100, 2)
# country_wise


# In[14]:



# """
# End of preprocessing:
# Frames to save:
# country_wise, day_wise, total_data, full_grouped
# """


# In[15]:


total_data.to_csv('../Data/Cleaned_Final_Global_Data.csv',index=False)
country_wise.to_csv('../Data/Country_Wise_Data.csv',index=False)
day_wise.to_csv('../Data/Day_Wise_Data.csv',index=False)
full_grouped.to_csv('../Data/Full_Grouped_Data.csv',index=False)

