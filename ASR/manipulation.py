#!/usr/bin/env python
# coding: utf-8

# # offset.py 本体

# In[1]:


import pandas as pd


# ## 1. offset

# In[2]:


def offset(data):
    data = data - data.values[0,:]
    
    return data


# ## 2. dummy_sub

# In[18]:


def dummy_sub(data, dummy, dum_ch):
    data = data.add(-dummy[dum_ch].values[:], axis=0)

    return data


# ## 3. sma

# In[4]:


def sma(data, sma_window):
    data = data.rolling(window=sma_window, min_periods=1).mean()
    
    return data