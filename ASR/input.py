#!/usr/bin/env python
# coding: utf-8

# # input.py 本体

import pandas as pd
import numpy as np


# ## 0. csv

def csv(setting_csv, dummy_ch_csv):
    """input all csv files"""
    
    setting = pd.read_csv(setting_csv, index_col=0)
    dummy_ch = pd.read_csv(dummy_ch_csv, index_col=0, header = None)
    
    return setting , dummy_ch 


# ## 1. strain

def strain(sample_ID, raw_data_csv, setting):
    ini_time = int(setting.at["Initial Time", sample_ID])
    fin_time = int(setting.at["Final Time", sample_ID])
    ch = setting.loc["xx":"xz", sample_ID].dropna(how="all").values
    
    ls = list(range(ini_time, fin_time+1))
    ls.insert(0,0)
    strain = pd.read_csv(raw_data_csv, skiprows=lambda x: x not in ls, usecols=ch)
    
    return strain


# ## 2. dummy

def dummy(sample_ID, raw_data_csv, setting, dummy_ch):
    ini_time = int(setting.at["Initial Time", sample_ID])
    fin_time = int(setting.at["Final Time", sample_ID])

    if dummy_ch.empty:
      dummy = pd.DataFrame(index = range(0, fin_time - ini_time + 1) , columns = ["CH_None"]).fillna(0)
      
    else:
      dv = dummy_ch.values.tolist()[0]
      
      ls = list(range(ini_time, fin_time+1))
      ls.insert(0,0)
      dummy = pd.read_csv(raw_data_csv, skiprows=lambda x: x not in ls, usecols=dv)
     
    return dummy


# ## 3. temperature

def temperature(sample_ID, raw_data_csv, setting):
    ini_time = int(setting.at["Initial Time", sample_ID])
    fin_time = int(setting.at["Final Time", sample_ID])
    
    ls = list(range(ini_time, fin_time+1))
    ls.insert(0,0)
    temperature = pd.read_csv(raw_data_csv, skiprows=lambda x: x not in ls, usecols=["CH000", "CH001"])
    
    return temperature


# ## 4. date

def date(sample_ID, raw_data_csv, setting):
    ini_time = int(setting.at["Initial Time", sample_ID])
    fin_time = int(setting.at["Final Time", sample_ID])
    
    ls = list(range(ini_time, fin_time+1))
    ls.insert(0,0)
    date = pd.read_csv(raw_data_csv, skiprows=lambda x: x not in ls, usecols=["Elapsed Time","Time.", "Channel No.", "---.1"])
    
    return date
