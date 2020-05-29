#!/usr/bin/env python
# coding: utf-8

# In[8]:


from ASR import input
from ASR import manipulation
from ASR import plot
import pandas as pd
from memory_profiler import profile


# In[9]:


# input file names
raw_data_csv = "./InputFiles/normal_strain.csv"
condition_csv= "./InputFiles/input.csv"
dummy_ch_csv = "./InputFiles/dummy_ch.csv"


# In[10]:


# load data from csv
raw_data, condition_data, dummy_ch = input.csv(raw_data_csv=raw_data_csv, condition_csv=condition_csv, dummy_ch_csv=dummy_ch_csv)


# ## each sample

# In[ ]:


for i in condition_data.columns:
    sample_ID = i
    
    ud = int(condition_data.loc["Using Dummy", i])
    
    strain = input.strain(sample_ID=i, raw_data=raw_data, condition=condition_data)
    dummy = input.dummy(sample_ID=i, raw_data=raw_data, condition=condition_data, dummy_ch=dummy_ch)
    temperature = input.temperature(sample_ID=i, raw_data=raw_data, condition=condition_data)
    date = input.date(sample_ID=i, raw_data=raw_data, condition=condition_data)
    
    # offset strain data
    strain_offset = manipulation.offset(strain)
    dummy_offset = manipulation.offset(dummy)
    
    if ud == 1:
        dum_ch = condition_data.loc["Which Dummy", i]
        strain_offset_dum = manipulation.dummy_sub(strain_offset, dummy_offset[dum_ch])
    elif ud == 0:
        strain_offset_dum = strain_offset
    else:
        print("invalid value for Using Dummy during " + i)
        
    
    # concatinate time & strain
    time_strain = pd.concat([date["Elapsed Time"], strain_offset_dum, temperature], axis=1)
    
    # plot strain
    plot.strain(time_strain, i)
    plot.each_dirc(time_strain, i, condition_data)

    # make csv file
    data = pd.concat([date, strain_offset_dum, temperature], axis=1)
    data.to_csv("./output/" + i + ".csv", mode="w")


# In[ ]:




