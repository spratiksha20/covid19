#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


confirmed_df = pd.read_csv('../Data/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('../Data/time_series_covid19_recovered_global.csv')
deaths_df = pd.read_csv('../Data/time_series_covid19_deaths_global.csv')


# In[18]:


#confirmed_df.head()
#recovered_df.head()
deaths_df.head()


# In[13]:


#confirmed_df.describe()
#confirmed_df.columns
#recovered_df.describe()
#recovered_df.columns
#deaths_df.describe()
#deaths_df.columns


# In[48]:


#We need the dates as identifiers and not as columns
date_cols = confirmed_df.columns[4:]
confirmed_df_temp = confirmed_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'], value_vars= date_cols ,var_name='Date',value_name='Confirmed')
# confirmed_df_temp
deaths_df_temp = deaths_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'], value_vars= date_cols, var_name='Date',value_name='Deaths')
# deaths_df_temp[deaths_df_temp['Deaths']!=0]
# deaths_df_temp
recovered_df_temp = recovered_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'], value_vars= date_cols, var_name='Date',value_name='Recovered')
# recovered_df_temp
# print(recovered_df_temp.shape)
# print(deaths_df_temp.shape)
# print(confirmed_df_temp.shape)
# We see that the number of rows in recovered is different. *****(Check why?)


# In[43]:


#concatenation gives error due to different labels in death. Merge used instead
total_data = pd.merge(left=confirmed_df_temp, right=deaths_df_temp, how='left',on=['Province/State','Country/Region','Date','Lat','Long'])
# print(total_data.head(10))
total_data = pd.merge(left=total_data, right=recovered_df_temp, how='left', on=['Province/State','Country/Region','Date','Lat','Long'])
# print(total_data.head(10))
# total_data.shape
# shape same as deaths_df_temp


# In[54]:


# print(total_data)
# We see a lot of province and states to be null. Lets check how many.
# total_data.isna().sum()


# In[53]:


#For data points where the recovered cases is not available, let us initialise them to 0.
total_data['Recovered'] = total_data['Recovered'].fillna(0)
# Was giving some string exceptions occasionally. Fixed:
total_data['Recovered'] = total_data['Recovered'].astype(int)
# print(total_data.isna().sum())
#Recovered Nan fixed.


# In[61]:


#Lets glance at the State/Province and Country feature for the whole data frame
# with pd.option_context('display.max.rows',None,'display.max.columns',None):
#     print(total_data[['Province/State','Country/Region']])
# Too large - Let us assume the rest of the data is intact. (Fixes made if future errors found)


# In[63]:


# Let us save this data finally.
total_data.to_csv('../Data/Cleaned_Final_Global_Data.csv',index=False)

