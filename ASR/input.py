#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np


# In[4]:


def condition(raw_data_csv, condition_csv, dummy_ch_csv):
    raw_data = pd.read_csv(raw_data_csv, index_col=0)
    condition = pd.read_csv(condition_csv, index_col=0)
    dummy_ch = pd.read_csv(dummy_ch_csv, index_col=0)
    
    return raw_data , condition , dummy_ch 


# In[17]:


def strain(sample_ID, raw_data_file, condition_file):
    sample_ID=a


# In[18]:


def dummy(sample_ID, raw_data_file, dummy_ch_file):
    l


# In[19]:


def temperature(sample_ID, raw_data_file):
    a


# In[ ]:




