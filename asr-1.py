from ASR import input
from ASR import manipulation
from ASR import plot
import matplotlib.pyplot as plt
import pandas as pd
import gc
import os

#=========== general settings ============================#
plt.rcParams["figure.figsize"] = [30, 20]
plt.rcParams["figure.subplot.wspace"] = 0.4
plt.rcParams["figure.subplot.hspace"] = 0.6

plt.rcParams['font.family'] ='sans-serif'#使用するフォント
plt.rcParams['font.sans-serif'] ='Arial'#使用するフォント
plt.rcParams["font.size"] = 30
plt.rcParams['mathtext.rm'] ='sans'#使用するフォント
plt.rcParams['mathtext.default'] ='rm'#使用するフォント

plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
plt.rcParams["xtick.major.pad"] = 19.0
plt.rcParams["ytick.major.pad"] = 16.0
plt.rcParams["xtick.major.size"] = 10
plt.rcParams["ytick.major.size"] = 10

plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ
plt.rcParams["axes.labelpad"] = 10

plt.rcParams["lines.linewidth"] = 3.0
#==================================================================#

os.makedirs("./output", exist_ok=True)

# input file names
raw_data_csv = "./InputFiles/normal_strain.csv"
setting_csv= "./InputFiles/input.csv"
dummy_ch_csv = "./InputFiles/dummy_ch.csv"


# load data from csv
setting_data, dummy_ch = input.csv(setting_csv=setting_csv, dummy_ch_csv=dummy_ch_csv)
print(setting_data)
print("")


# each sample

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

