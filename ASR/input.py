#!/usr/bin/env python
# coding: utf-8

# # input.py 本体

# In[41]:


import pandas as pd
import numpy as np


# ## 0. csv

# In[150]:


def csv(raw_data_csv, condition_csv, dummy_ch_csv):
    """input all csv files"""
    raw_data = pd.read_csv(raw_data_csv, index_col=1, skiprows=[1], converters={"Time.":str, 'Channel No.':str, "---.1":str})
    condition = pd.read_csv(condition_csv, index_col=0)
    dummy_ch = pd.read_csv(dummy_ch_csv, index_col=0)
    
    return raw_data , condition , dummy_ch 


# ## 1. strain

# In[151]:


def strain(sample_ID, raw_data, condition):
    ini_time = int(condition.at["Initial Time", sample_ID])
    fin_time = int(condition.at["Final Time", sample_ID])
    ch = condition.loc["xx":"xz", sample_ID].dropna(how="all").values
    time = raw_data.loc[ini_time:fin_time, ["Elapsed Time","Time.", "Channel No.", "---.1"]]
    strain = raw_data.loc[ini_time:fin_time, ch]
#     if add time columns
#     strain = pd.concat([time, strain], axis=1)
    
    return strain


# ## 2. dummy

# In[152]:


def dummy(sample_ID, raw_data, condition, dummy_ch):
    ini_time = int(condition.at["Initial Time", sample_ID])
    fin_time = int(condition.at["Final Time", sample_ID])
    dummy_ch.values
    dummy = raw_data.loc[ini_time:fin_time, dummy_ch.values[0,:]]
    time = raw_data.loc[ini_time:fin_time, ["Elapsed Time","Time.", "Channel No.", "---.1"]]
#     if add time columns
#     dummy = pd.concat([time, dummy], axis=1)
    
    return dummy


# ## 3. temperature

# In[153]:


def temperature(sample_ID, raw_data, condition):
    ini_time = int(condition.at["Initial Time", sample_ID])
    fin_time = int(condition.at["Final Time", sample_ID])
    temperature = raw_data.loc[ini_time:fin_time, ["CH000", "CH001"]]
    time = raw_data.loc[ini_time:fin_time, ["Elapsed Time","Time.", "Channel No.", "---.1"]]
#     if add time columns
#     temperature = pd.concat([time, temperature], axis=1)
    
    return temperature


# ## 4. date

# In[154]:


def date(sample_ID, raw_data, condition):
    ini_time = int(condition.at["Initial Time", sample_ID])
    fin_time = int(condition.at["Final Time", sample_ID])
    time = raw_data.loc[ini_time:fin_time, ["Elapsed Time","Time.", "Channel No.", "---.1"]]
    
    return time