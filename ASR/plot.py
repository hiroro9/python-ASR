#!/usr/bin/env python
# coding: utf-8

# # plot.py

import matplotlib.pyplot as plt
import pandas as pd

# ## 1. strain

def strain(data, temp, sample_ID):
    fig, ax = plt.subplots(1,1)
    data.plot(x="Elapsed Time", ax=ax)
    ax.set_xlabel("Elapsed Time [h]", fontsize="large")
    
    ax_t = ax.twinx()
    temp.loc[:,["Elapsed Time", "CH000"]].plot(x="Elapsed Time",ax = ax_t, marker = "o", legend="Water Temp")
    temp.loc[:,["Elapsed Time", "CH001"]].plot(x="Elapsed Time",ax = ax_t, marker = "o", legend="Room Temp")
    ax_t.set_ylabel("Temperature [$^\circ$C]", fontsize="large")
    ax_t.set_ylim([-20,110])
    ax_t.legend()
    
    ax.set_ylabel("$\mu$ strain", fontsize="large")
    ax.legend(bbox_to_anchor=(1.2,1))
    plt.subplots_adjust(left=0.1, right=0.8)
    fig.suptitle(sample_ID, fontsize="large",fontweight="bold")
    
    fig.savefig("./output/{}.png".format(sample_ID), pad_inches=0.05)
    plt.close(fig)


# ## 2. each_dirc

def each_dirc(data, sample_ID, condition):
    fig = plt.figure()
    ch = condition.loc["xx":"xz", sample_ID].dropna(how="all")
    ech = pd.DataFrame(ch.index)
    ech2 = ech[~ech.duplicated()].reset_index(drop=True)
    
    for i in range(0,len(ech2.index)):
        k = ch.at[ech2.at[i,"#"]]
        axi = fig.add_subplot(3,3,i+1)
        data.plot(x=0,y=k,ax=axi)
        axi.set_xlabel("Elapsed Time [h]", fontsize="large")
        axi.set_ylabel("$\mu$ strain", fontsize="large")
        axi.set_title(ech2.at[i,"#"])
    fig.suptitle(sample_ID + "_each_Gage",fontsize="large", fontweight="bold")
    
    fig.savefig("./output/{}_each.png".format(sample_ID), pad_inches=0.05)
    plt.close(fig)


# ## 3. dummy

def dummy(data, temp, sample_ID):
    fig, ax = plt.subplots(1,1)
    data.plot(x="Elapsed Time", ax=ax)
    ax.set_xlabel("Elapsed Time [h]", fontsize="large")
    
    ax_t = ax.twinx()
    temp.plot(x="Elapsed Time",ax = ax_t,marker = "o")
    ax_t.set_ylabel("Temperature [$^\circ$C]", fontsize="large")
    
    ax.set_ylabel("$\mu$ strain", fontsize="large")
    ax.legend(bbox_to_anchor=(1.2,1))
    plt.subplots_adjust(left=0.1, right=0.8)
    fig.suptitle(sample_ID + " dummy samples", fontsize="large",fontweight="bold")
    
    fig.savefig("./output/{}_dummy.png".format(sample_ID), pad_inches=0.05)
    plt.close(fig)
