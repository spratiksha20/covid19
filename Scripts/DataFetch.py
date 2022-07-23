#!/usr/bin/env python
# coding: utf-8

# In[2]:


#imports
#----------------

import pandas as pd
import wget


# In[5]:


get_ipython().system(' rm -rf ../Data/*.csv # removes the existing csv files')


# In[8]:


# Now we assign the urls of the csv files that we want to access
urls = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', 
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']
# Credits:

# get_ipython().system('cd ../Data/')
for url in urls:
    wget.download(url,'../Data/')
    
# this downloads and stores the .csv files from the urls in the Data folder


# In[ ]:




