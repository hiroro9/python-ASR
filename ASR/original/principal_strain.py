import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import numpy.linalg as LA
import mplstereonet as sn
plt.rcParams["font.size"]=30

pi=np.pi

def principal_strain(strain_tensor_data, k, sample_ID, initial_step, ch_list):
    """ calculate magnitudes and directions of principal strains """


    k = str(k)
    it = int(initial_step)
    dir = ["xx","yy","zz","xy","yz","zx"]
    ch = ch_list.loc["ch",:]



    """ ~~~~~~~~~~input from data file~~~~~~~~~~~~~~~~~ """

    sdata = strain_tensor_data
    time_p = sdata.loc[:,"Elapsed Time"]     

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


    time_n = time_p.values
    t = len(sdata.index)


    """ ~~~~~~~~~~Create strain tensor ~~~~~~~~~~~~~~~~~ """

    stensor = np.empty((t,3,3))
    for i in range(0,t):
        strain = sdata.loc[i+1, dir]

        s1 = strain.at["xx"]
        s2 = strain.at["xy"]
        s3 = strain.at["zx"]
        s4 = strain.at["yy"]
        s5 = strain.at["yz"]
        s6 = strain.at["zz"]

        stensor[i,:,:] = np.array([[s1,s2,s3],
                                   [s2,s4,s5],
                                   [s3,s5,s6]])

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


    w,v = LA.eigh(stensor) #calculate eigen vectors & eigenvalues


    """ ~~~~~~~~~~ Output data ~~~~~~~~~~~~~~~~~~~~~~~ """
    time = time_n[it:]

    w = w[it:,:]
    v = v[it:,:,:]


    v1 = v[:,:,2]
    v2 = v[:,:,1]
    v3 = v[:,:,0]


    w_ave = np.mean(w, axis=0)
    v_ave = np.mean(v, axis=0)

    v1_ave = v_ave[:,2]
    v2_ave = v_ave[:,1]
    v3_ave = v_ave[:,0]
    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """



    def plunge_trend(n):
    
        norm = np.linalg.norm(n)
        n = n/norm
        
        x = n[0]
        y = n[1]
        z = n[2]
    
        plunge = np.arcsin(z) 
    
        if x == 0 and y > 0:
            trend = pi*0.5
        elif x == 0 and y < 0:
            trend = pi*1.5
        elif x > 0 and y == 0:
            trend = 0
        elif x < 0 and y == 0:
            trend = pi
        elif x == 0 and y == 0:
            trend = 0
        else:
            trend = np.arctan(abs(y/x))
    
        if x > 0 and y>0:
            trend = trend 
        elif x > 0 and y< 0:
            trend = 2*pi - trend
        elif x <0 and y <0:
            trend = 1.5*pi - trend
        elif x <0 and y >0:
            trend = trend + 0.5*pi
    
        plunge = np.rad2deg(plunge)
        trend = np.rad2deg(trend)
        return plunge, trend


    def plot_schmidt(ax, plunge, trend, style, label = "", markersize = 30, alpha = 1):
        if plunge >= 0:
            ax.line(plunge, trend, style,label = label, markersize = markersize, alpha = alpha)
        elif plunge < 0:
            ax.line(-plunge, trend, style,label = label, markerfacecolor = "#ffffff", markersize = markersize, alpha = alpha)


    fig = plt.figure(figsize=(30,30))
    ax = fig.add_subplot(3,1,1,projection="stereonet")
    ax.set_azimuth_ticklabels(["N","","E","","S","","W"])
    ax.grid(which="both")
    """ ~~~~~~~~~~ Lower-himisphere Schmidt net plot of principal strain directions ~~~~~~~~~~~~~~~~~~~~~~~ """

    for i in range(1, len(time)):
        plunge111, trend111 = plunge_trend(v1[i,:])
        plot_schmidt(ax,plunge111,trend111, "ro", markersize=5)

        plunge112, trend112 = plunge_trend(v2[i,:])
        plot_schmidt(ax,plunge112,trend112, "go", markersize=5)

        plunge113, trend113 = plunge_trend(v3[i,:])
        plot_schmidt(ax,plunge113,trend113, "bo", markersize=5)


    plunge1, trend1 = plunge_trend(v1[0,:])
    plot_schmidt(ax,plunge1,trend1, "r^",markersize =20)

    plunge2, trend2 = plunge_trend(v2[0,:])
    plot_schmidt(ax,plunge2,trend2, "g^",markersize =20)

    plunge3, trend3 = plunge_trend(v3[0,:])
    plot_schmidt(ax,plunge3,trend3, "b^",markersize =20)


    plunge1, trend1 = plunge_trend(v1[-1,:])
    plot_schmidt(ax,plunge1,trend1, "ro",markersize =20)

    plunge2, trend2 = plunge_trend(v2[-1,:])
    plot_schmidt(ax,plunge2,trend2, "go",markersize =20)

    plunge3, trend3 = plunge_trend(v3[-1,:])
    plot_schmidt(ax,plunge3,trend3, "bo",markersize =20)

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


    """ ~~~~~~~~~~ Lower-himisphere Schmidt net plot of averaged principal strain directions ~~~~~~~~~~~~~~~~~~~~~~~ """

    plunge1, trend1 = plunge_trend(v1_ave)
    plot_schmidt(ax,plunge1,trend1, "r*",markersize =20, label = "$\sigma_1$")

    plunge2, trend2 = plunge_trend(v2_ave)
    plot_schmidt(ax,plunge2,trend2, "g*",markersize =20,label = "$\sigma_2$")

    plunge3, trend3 = plunge_trend(v3_ave)
    plot_schmidt(ax,plunge3,trend3, "b*", markersize =20,label = "$\sigma_3$")

    ax.legend(bbox_to_anchor = (1.2, 1), loc="upper left")
    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

    
    fig.text(0.15,0.7,ch)


    """ ~~~~~~~~~~ Plot of max & min horizontal strain directions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """
 
    zr = np.empty((360,1))
    for i in range(0,360):
        th_deg = i
        th = th_deg*pi*180**(-1)  

        vector = np.array([[np.cos(th)],[np.sin(th)],[0]])
        sstensor = stensor[-1,:,:]
        z = sstensor.dot(vector)
        zz = vector.T.dot(z)
        zr[i] = zz

    th_max = zr.argmax()
    th_min = zr.argmin()

    #th_max = th_max*pi*180**(-1)  
    #th_min = th_min*pi*180**(-1)  

    #n_max_1 = np.array([[np.cos(th_max)],[np.sin(th_max)],[0]])
    #n_max_2 = np.array([[np.cos(th_max+pi)],[np.sin(th_max+pi)],[0]])

    #n_min_1 = np.array([[np.cos(th_min)],[np.sin(th_min)],[0]])
    #n_min_2 = np.array([[np.cos(th_min+pi)],[np.sin(th_min+pi)],[0]])

    plunge11, trend11 = 0, th_max
    plunge12, trend12 = 0, th_max+180
    #plunge11, trend11 = plunge_trend(n_max_1)
    #plunge12, trend12 = plunge_trend(n_max_2)
    plot_schmidt(ax,plunge11,trend11, "rD",markersize =30)
    plot_schmidt(ax,plunge12,trend12, "rD",markersize =30)

    plunge22, trend22 = 0, th_min
    plunge23, trend23 = 0, th_min + 180
    #plunge22, trend22 = plunge_trend(n_min_1)
    #plunge23, trend23 = plunge_trend(n_min_2)
    plot_schmidt(ax,plunge22,trend22, "bD",markersize =30)
    plot_schmidt(ax,plunge23,trend23, "bD",markersize =30)

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """



    """ ~~~~~~~~~~ Plot of time change of principal strain magnitudes ~~~~~~~~~~~~~~~~~~~ """

    ax1 = fig.add_subplot(3,1,2)
    w1 = w[:,2]-w[0,2]
    w2 = w[:,1]-w[0,1]
    w3 = w[:,0]-w[0,0]
    time = time[:]-time[0]


    ax1.plot(time,w1,label="$\epsilon_1$")
    ax1.plot(time,w2,label="$\epsilon_2$")
    ax1.plot(time,w3,label="$\epsilon_3$")
    ax1.set(xlabel="Elapsed Time[h]",ylabel="Strain[$\mu$strain]")
    ax1.legend()

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """



    """ ~~~~~~~~~~ Plot of time change of principal strain magnitudes ratios ~~~~~~~~~~~~~~~~~~~ """

    ax2 = fig.add_subplot(3,1,3)
    w1 = w1[1:]
    w2 = w2[1:]
    w3 = w3[1:]
    time1 = time[1:]
    
    w21 = w2/w1
    w31 = w3/w1

    ax2.plot(time1,w21,label="$\epsilon_2$/$\epsilon_1$")
    ax2.plot(time1,w31,label="$\epsilon_3$/$\epsilon_1$")
    ax2.set(xlabel="Elapsed Time[h]")
    ax2.legend()

    """ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


    fig.suptitle(sample_ID+"_"+k,fontsize="large", fontweight="bold")
    fig.savefig("result_"+sample_ID+"_"+k+".png")
    plt.close(fig)

    return w, v
