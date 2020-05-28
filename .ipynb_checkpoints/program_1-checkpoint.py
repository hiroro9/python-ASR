from ASR import input
import pandas as pd
from multiprocessing import Pool
import multiprocessing as mlt


raw_data_file = "normal_strain.csv"
condition_file = "input.csv"
dummy_ch_file = "dummy_ch.csv"
sma_window = 5000


"""~~~~~~~~~~~~~~~ Input from data files ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
input_condition = pd.read_csv(condition_file, index_col=0)
ic = input_condition

input_dum_ch = pd.read_csv(dummy_ch_file,index_col=0)
dum=input_dum_ch.values
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""



"""~~~~~~~~~~~~~~~ Print input conditons ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
print("""
""")
print("~~~~~~~~~~~~~~~~~~~~Input Conditions~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("")
print(ic)
print("")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print("""
""")
print("~~~~~~~~~~~~~~~~~~~~~~~Dummy Channels~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("")
print(input_dum_ch)
print("")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("""
""")
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""



"""~~~~~~~~~~~~~~~ apply the function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def d_form_2(i): 
    input.d_form(ic.columns[i], raw_data_file, condition_file, dummy_ch_file, sma_window)

def multi():
    p = Pool(mlt.cpu_count())
    p.map(d_form_2, range(len(ic.columns)))
    p.close()

if __name__ == "__main__":
    multi()
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


