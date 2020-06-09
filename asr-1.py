#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ASR import input
from ASR import manipulation
from ASR import plot
import pandas as pd
import gc
import os


# In[2]:

os.makedirs("./output", exist_ok=True)

# input file names
raw_data_csv = "./InputFiles/normal_strain.csv"
setting_csv= "./InputFiles/input.csv"
dummy_ch_csv = "./InputFiles/dummy_ch.csv"


# In[3]:


# load data from csv
setting_data, dummy_ch = input.csv(setting_csv=setting_csv, dummy_ch_csv=dummy_ch_csv)
print(setting_data)
print("")


# ## each sample

# In[5]:


for i in setting_data.columns:
    sample_ID = i
    
    ud = int(setting_data.loc["Using Dummy", i])
    sma_window = int(setting_data.loc["SMA Window", i])
    
    strain = input.strain(sample_ID=i, raw_data_csv=raw_data_csv, setting=setting_data)
    dummy = input.dummy(sample_ID=i, raw_data_csv=raw_data_csv, setting=setting_data, dummy_ch=dummy_ch)
    temperature = input.temperature(sample_ID=i, raw_data_csv=raw_data_csv, setting=setting_data)
    date = input.date(sample_ID=i, raw_data_csv=raw_data_csv, setting=setting_data)
    
    # offset strain data
    strain = manipulation.offset(strain)
    dummy = manipulation.offset(dummy)
    
    if ud == 1:
        dum_ch = setting_data.loc["Which Dummy", i]
        strain = manipulation.dummy_sub(strain, dummy, dum_ch)
    elif ud == 0:
        pass
    else:
        print("invalid value for Using Dummy during " + i)
    
    strain = manipulation.sma(strain, sma_window)
    
    # make csv file
    data = pd.concat([date, strain, temperature], axis=1)
#    data.to_csv("./output/" + i + ".csv", mode="w")
    data.to_csv("./output/{}.csv".format(i), mode="w")
    del data
    gc.collect()
    
    # plot strain
    time_strain = pd.concat([date["Elapsed Time"], strain], axis=1)
    time_dummy = pd.concat([date["Elapsed Time"], dummy], axis=1)
    time_temperature = pd.concat([date["Elapsed Time"], temperature], axis=1)

    plot.strain(time_strain,time_temperature, i)
    plot.each_dirc(time_strain, i, setting_data)
    plot.dummy(time_dummy,time_temperature, i)


# In[ ]:




