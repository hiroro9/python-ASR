import numpy as np
import pandas as pd

pi=np.pi

def MPinv(list_of_ch,direction, angle, azimuth):
    """ caluculating the Moore-Penrose Inverse Matrix for Strain tensor calculation """


    """~~~~~~~~~~~ Input conditions ~~~~~~~~~~~~~~"""
    ch_list = list_of_ch
    direction_deg = float(direction) #inclined direction of wellbore from North
    angle_deg = float(angle) # inclined angle of well 
    azimuth_deg = float(azimuth) # core orientation from North or inclined direction 
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

    azimuth_deg = azimuth_deg - 45

    """~~~~~~~~~~~ Allocate numbers to each direction (for example, xx => 0, xy => 3 etc...) ~~~~~~~~~~~~~~"""
    ch_col = ch_list.columns.values

    if "xx" in ch_col: ch_list.at["ch_no","xx"] =0
    if "yy" in ch_col: ch_list.at["ch_no","yy"] =1
    if "zz" in ch_col: ch_list.at["ch_no","zz"] =2
    if "xy" in ch_col: ch_list.at["ch_no","xy"] =3
    if "yx" in ch_col: ch_list.at["ch_no","yx"] =4
    if "yz" in ch_col: ch_list.at["ch_no","yz"] =5
    if "zy" in ch_col: ch_list.at["ch_no","zy"] =6
    if "zx" in ch_col: ch_list.at["ch_no","zx"] =7
    if "xz" in ch_col: ch_list.at["ch_no","xz"] =8

    ch = ch_list.loc["ch_no",:].values
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

    Number_of_vector = len(ch)
    No_v = Number_of_vector
    direction_rad = direction_deg*pi*180**(-1)  
    angle_rad = angle_deg*pi*180**(-1)  
    azimuth_rad = azimuth_deg*pi*180**(-1)  


    """~~~~~~~~ Create matrix of Direction Cosine vectors~~~~~~~~~~~~~~~~~~~~~~~ """
    c=np.cos(0.25*pi)
    s=np.sin(0.25*pi)
    n = np.zeros((3,9))

    n[:,0] = np.array([1,0,0])
    n[:,1] = np.array([0,1,0])
    n[:,2] = np.array([0,0,1])
    n[:,3] = np.array([c,s,0])
    n[:,4] = np.array([c,-s,0])
    n[:,5] = np.array([0,c,s])
    n[:,6] = np.array([0,c,-s])
    n[:,7] = np.array([c,0,s])
    n[:,8] = np.array([-c,0,s])


    """~~~~~~~~~~~~~~ coordinate transformation from 'ASR local co-ordinate' to 'Geological co-ordinate' ~~~~~~~~~~~~~~~~~"""
    cdr = np.cos(direction_rad)
    sdr = np.sin(direction_rad)

    caz = np.cos(azimuth_rad)
    saz = np.sin(azimuth_rad)

    can = np.cos(angle_rad)
    san = np.sin(angle_rad)

    Rdr = np.array([[cdr, sdr, 0],[-sdr, cdr, 0],[0, 0, 1]]) #counter_clockwise
    Ran = np.array([[1, 0, 0],[0, can, san],[0, -san, can]])
    Raz = np.array([[caz, -saz, 0],[saz, caz, 0],[0, 0, 1]])

    R1 = Ran.dot(Rdr)
    R2 = Raz.dot(R1)

    for i in range(0,9):
        n[:,i] = R2.dot(n[:,i])
    n= np.round(n,6)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """





    """~~~~~~~~ Create matrix A (b = Ax: b;Observed normal strain data, x;strain tensor component which we have to determine) ~~~~~~~~~~~~~~~~~~~~~~~ """
    X = np.empty((No_v,6))

    for i in range(0,No_v):
       cc = ch[i]
       X[i,:] = np.array([n[0,cc]**2, n[1,cc]**2, n[2,cc]**2, 2*n[0,cc]*n[1,cc], 2*n[1,cc]*n[2,cc], 2*n[2,cc]*n[0,cc]])
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


    X_inv = np.linalg.pinv(X) # Calculate Moore-Penrose inverse matrix

    return X_inv








def strain_tensor(list_of_combinations, Moore_Penrose_inv_mat, raw_data, time_step=1):
    """ calculate strain tensor """

    """~~~~~~~~~~~~~ Input data ~~~~~~~~~~~~~~"""
    mp = Moore_Penrose_inv_mat
    dt = time_step
    loc = list_of_combinations
    time = raw_data.loc[:,"Elapsed Time"].values     
    ch_list = loc.loc["ch",:].values
    strain = raw_data.loc[:, ch_list]
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


    """~~~~~~~~~~~~~ Calculate strain tensor ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    strain_l = pd.DataFrame({"Elapsed Time":[0],"xx":[0],"yy":[0],"zz":[0],"xy":[0],"yz":[0],"zx":[0]})
    for i in range(0, len(time),dt):
        strain2 = strain.loc[i,:].values
        strain3 = mp.dot(strain2)

        t = time[i]
        s = np.hstack((t,strain3)) 
        r = pd.DataFrame(s,index = ["Elapsed Time","xx","yy","zz","xy","yz","zx"])
       
        strain_l = pd.concat([strain_l,r.T]).reset_index(drop=True)
    strain_ll = strain_l.drop(0)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    return strain_ll


