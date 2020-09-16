#!/usr/bin/env python
# coding: utf-8

# offset.py 本体

import pandas as pd


# 1. offset

def offset(data):
    data = data - data.values[0,:]
    
    return data


# ## 2. dummy_sub

def dummy_sub(data, dummy, dum_ch):
    data = data.add(-dummy[dum_ch].values[:], axis=0)

    return data


# ## 3. sma

def sma(data, sma_window):
    data = data.rolling(window=sma_window, min_periods=1).mean()
    
    return data
