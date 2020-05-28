import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ASR import generate_combination as gc
from ASR import leastsquare as ls
from ASR import principal_strain as ps
from multiprocessing import Pool
import multiprocessing as mlt


"""~~~~~~~~~~~~~~~ input conditions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
sample_ID = "FDB-13"
initial_step = 100
time_step = 10

input_file = "input.csv"
""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


""" ~~~~~~~~~~~~~~~~~~ print conditions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """
print("")
#sample_ID = input("""Please input sample ID!!
#: """)
print("Sample_ID:",sample_ID)

#initial_step_str = input("""Please input Initial Step!!
#: """)
#initial_step = int(initial_step_str)
print("Initial Step:",initial_step)

#time_step_str = input("""Please input Time Step!!
#: """)
#time_step = int(time_step_str)
print("Time Step:",time_step)
print("")
print("Combination number:",len(list_of_comb))
""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


input_cond = pd.read_csv(input_file, index_col=0,usecols=["#",sample_ID])
input_raw_data = pd.read_csv(sample_ID+".csv",usecols=lambda x: x not in ['---', 'CH000','CH001'])

channels = input_cond.loc["xx":"xz", sample_ID].dropna(how="all")
direction = input_cond.at["Inclined direction",sample_ID]
angle = input_cond.at["Angle(degree)",sample_ID]
azimuth = input_cond.at["Azimuth(degree)", sample_ID]



"""~~~~~~~~~~~~~~~~~~~ Choose combination of 9 strain gauges ~~~~~~~~~~~~~~~~~~~"""
list_of_comb = gc.gen_comb(sample_ID, input_file)
""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


def main(i):
    a = ls.MPinv(list_of_comb[i], direction, angle, azimuth)
    b = ls.strain_tensor(list_of_comb[i], a, input_raw_data, time_step) 
    w,v = ps.principal_strain(b,i,sample_ID, initial_step, list_of_comb[i])
 
def multi():
    p = Pool(mlt.cpu_count())
    p.map_async(main, range(len(list_of_comb))).get(99999)
    p.close()

if __name__ == "__main__":
    multi()

#k = 0
#for i in list_of_comb:
#    k += 1
#    a = ls.MPinv(i, direction, angle, azimuth)
#    b = ls.strain_tensor(i, a, input_raw_data, time_step) 
#    w,v = ps.principal_strain(b,k,sample_ID, initial_step, i)
#    c = check_criteria(w,v)
#     if c == 1:
#         e += 1
#     elif c == 0:
#         pass


