#!/usr/bin/env python
# coding: utf-8

# # offset.py 本体

# In[12]:


import pandas as pd


# ## 1. offset

# In[15]:


def offset(data):
    offset = data - data.values[0,:]
    
    return offset


# ## 2. dummy_sub

# In[31]:


def dummy_sub(data, dummy):
    sub_data = data - dummy
    
    return sub_data


# ## 3. sma

# In[18]:


def sma(data, sma_window):
    sma_data = data.rolling(window=sma_window, min_periods=1).mean()
    
    return sma_data