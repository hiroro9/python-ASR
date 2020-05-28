import numpy as np
import pandas as pd


def gen_comb(sample_ID, input_file):
    """ Generate all combinations of strain channels """

    """~~~~~~~~~~~~~~~~ Input from a condition file ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    ch = pd.read_csv(input_file,index_col = 0, usecols = ["#",sample_ID]).loc["xx":"xz"].dropna(how = "all")
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    frame = pd.DataFrame(ch.index)
    frame1 = frame[~frame.duplicated()].reset_index(drop=True)

    if "xx" in ch.index: 
        xx = ch.loc["xx"].reset_index(drop=True).values 
    else:
        xx = np.array([0])

    if "yy" in ch.index: 
        yy = ch.loc["yy"].reset_index(drop=True).values 
    else:
        yy = np.array([0])

    if "zz" in ch.index: 
        zz = ch.loc["zz"].reset_index(drop=True).values 
    else:
        zz = np.array([0])

    if "xy" in ch.index: 
        xy = ch.loc["xy"].reset_index(drop=True).values 
    else:
        xy = np.array([0])

    if "yx" in ch.index: 
        yx = ch.loc["yx"].reset_index(drop=True).values 
    else:
        yx = np.array([0])

    if "yz" in ch.index: 
        yz = ch.loc["yz"].reset_index(drop=True).values 
    else:
        yz = np.array([0])

    if "zy" in ch.index: 
        zy = ch.loc["zy"].reset_index(drop=True).values 
    else:
        zy = np.array([0])

    if "zx" in ch.index: 
        zx = ch.loc["zx"].reset_index(drop=True).values 
    else:
        zx = np.array([0])

    if "xz" in ch.index: 
        xz = ch.loc["xz"].reset_index(drop=True).values 
    else:
        xz = np.array([0])
    

    ch_list = ["q"]
    
    k = 0
    for i1 in range(0, len(xx)):
        for i2 in range(0, len(yy)):
            for i3 in range(0, len(zz)):
                for i4 in range(0, len(xy)):
                    for i5 in range(0, len(yx)):
                        for i6 in range(0, len(yz)):
                            for i7 in range(0, len(zy)):
                                for i8 in range(0, len(zx)):
                                    for i9 in range(0, len(xz)):

                                        #d = {"xx":{"ch":xx[i1]},"yy":{"ch":yy[i2]},"zz":{"ch":zz[i3]},"xy":{"ch":xy[i4]},"yx":{"ch":yx[i5]},"yz":{"ch":yz[i6]},"zy":{"ch":zy[i7]},"zx":{"ch":zx[i8]}, "xz":{"ch":xz[i9]}}
                                        #ch_comb = pd.DataFrame(d)

                                        d = {"xx":xx[i1],"yy":yy[i2],"zz":zz[i3],"xy":xy[i4],"yx":yx[i5],"yz":yz[i6],"zy":zy[i7],"zx":zx[i8], "xz":xz[i9]}
                                        ch_comb = pd.DataFrame(d, index= ["ch"])

                                        ch_comb = ch_comb[ch_comb!=0]
                                        ch_comb = ch_comb.dropna(how ="all", axis=1)
                                        ch_list = ch_list+[ch_comb]
                                        k +=1


    ch_list = ch_list[1:]

    return ch_list
    
