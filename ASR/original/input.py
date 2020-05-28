import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.size"]=25




def d_form(sample_ID, raw_data_file, condition_file, dummy_ch_file, sma_window):

    """convert the row data of normal ASR to off-set data"""


    """~~~~~ Input from data files ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    input_raw_data = pd.read_csv(raw_data_file,index_col=1, skiprows=[1],usecols=lambda x: x not in ['Time.','Channel No.','---.1'],dtype={"---":"int"})
    
    input_condition = pd.read_csv(condition_file, index_col=0)
    ic = input_condition
    
    input_dum_ch = pd.read_csv(dummy_ch_file,index_col=0)
    dum=input_dum_ch.values

    nn = int(sma_window)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    a = int(ic.at["Initial Time", sample_ID])
    b = int(ic.at["Final Time", sample_ID])
    c = int(ic.at["Using Dummy", sample_ID])
    d = ic.at["Which Dummy", sample_ID]


    input_ch = ic.loc["xx":"xz", sample_ID].dropna(how="all")
    ip = input_ch.values

    input_ch_ind = input_ch.index
    frame = pd.DataFrame(input_ch_ind)
    frame1 = frame[~frame.duplicated()]
    frame2 = frame1.reset_index(drop=True)


    """~~~~~ Input the data of a sample ~~~~~~~~~"""
    data1 = input_raw_data.loc[a:b,["Elapsed Time"]]
    data2 = input_raw_data.loc[a:b,ip]
    data3 = input_raw_data.loc[a:b,dum[0,:]]
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """~~~~~~ SMA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    data2 = data2.rolling(window = nn, min_periods = 1).mean()
    data3 = data3.rolling(window = nn, min_periods = 1).mean()
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """~~~~~ Form the dummy data for the sample ~~~~~~~~~~"""
    data33=pd.concat([data1, data3],axis=1)
    data3_offset = data33 - data33.values[0,:]
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """~~~~~~ Form the data of the sample ~~~~~~~~~~~~~"""
    data_conbine = pd.concat([data1,data2],axis=1)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    """~~~~~~ Off set for the sample data ~~~~~~~~~~~~~~"""
    data_offset = data_conbine - data_conbine.values[0,:]
    data1_offset = data1 - data1.values[0,:]
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""



    """~~~~~~ Subtracting Dummy strain data ~~~~~~~~~~~~~~~~~~~~~~~~~"""
    if c == 0:
        pass

    elif c == 1:
        dd = data3_offset.loc[a:b,[d]]

        chs = data_offset.columns[1:]
        chn = len(chs)
        for i in range(0, chn):
            cn = chs[i]
            data_offset[cn] = data_offset[cn].sub(dd[d], axis=0)


        dchs = data3_offset.columns[1:]
        dchn = len(dchs)
        for i in range(0, dchn):
            dcn=dchs[i]
            data3_offset[dcn] = data3_offset[dcn].sub(dd[d], axis=0)
   
    else:
        print("Invalid Value for 'using dummy'. Please input 0 or 1!") 

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""



    """~~~~~~ Input Tempareture data ~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    data_t = input_raw_data.loc[a:b,["CH000","CH001"]]
    data_t1 = pd.concat([data1_offset,data_t],axis=1)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """~~~~~~ Combine Temperature data to starain data ~~~~~~~~~"""
    data = pd.concat([data_offset,data_t], axis=1)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    """~~~~~~ Output the strain data to csv ~~~~~~"""
    data.to_csv(sample_ID+".csv")
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    """~~~~~~ Plot the strain data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    fig, ax = plt.subplots(1,1,figsize=(40,20))
    data_offset.plot(x="Elapsed Time",ax=ax) 
    ax.set_xlabel("Elapsed Time[h]", fontsize="large", fontweight="bold")

    #ax_t = ax.twinx()
    #data_t1.plot(x="Elapsed Time",ax = ax_t,marker = "o")
    #ax_t.set_ylabel("Temperature[$^\circ$C]", fontsize="large",fontweight="bold")

    ax.set_ylabel("Strain[$\mu$strain]", fontsize="large",fontweight="bold")
    ax.legend(bbox_to_anchor=(1.2,1))
    plt.subplots_adjust(left=0.1, right=0.8)
    fig.suptitle(sample_ID, fontsize="large",fontweight="bold")
    fig.savefig(sample_ID+".png")
    plt.close(fig)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    

    """~~~~~~ Plot each strain data set of the same direction ~~~~~~~~~~~~~~"""
    fig1 = plt.figure(figsize=(35,35))
    for i in range(0,len(frame2.index)):
        k=input_ch.at[frame2.at[i,"#"]]
        axi = fig1.add_subplot(3,3,i+1)
        data.plot(x=0,y=k,ax=axi)
        axi.set_xlabel("Elapsed Time[h]", fontsize="large", fontweight="bold")
        axi.set_ylabel("Strain[$\mu$strain]", fontsize="large",fontweight="bold")
        axi.set_title(frame2.at[i,"#"])
    fig1.suptitle(sample_ID+"_each_Gage",fontsize="large", fontweight="bold")
    fig1.savefig(sample_ID+"_each.png")
    plt.close(fig1)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    """~~~~~~ Plot the dummy data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    fig_d, ax_d = plt.subplots(1,1,figsize=(30,30))
    data3_offset.plot(x="Elapsed Time",ax=ax_d) 
    ax_d.set(xlabel="Elapsed Time[h]",ylabel="Strain[$\mu$strain]")
    ax_d.legend(bbox_to_anchor=(1.2,1))
    plt.subplots_adjust(left=0.1, right=0.8)
    fig_d.suptitle(sample_ID+"_Dummy gages",fontsize="large", fontweight="bold")
    fig_d.savefig(sample_ID+"_dummy.png")
    plt.close(fig_d)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    """~~~~~~ Plot the dummy data sets ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    fig_d2 = plt.figure(figsize=(30,30))
    for i in range(0,len(input_dum_ch.columns),2):
        axi = fig_d2.add_subplot(2,2,0.5*(i+2))
        data3_offset.plot(x="Elapsed Time",y=input_dum_ch.iat[0,i],ax=axi)
        data3_offset.plot(x=0,y=input_dum_ch.iat[0,i+1],ax=axi)
        axi.set(xlabel="Elapsed Time[h]",ylabel="Strain[$\mu$strain]")
    fig_d2.suptitle(sample_ID+"_Dummy_each",fontsize="large", fontweight="bold")
    fig_d2.savefig(sample_ID+"_dummy_each.png")
    plt.close(fig_d2)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
