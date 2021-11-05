import streamlit as st
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import flopy

def getKValArr(curr_stat):
    if curr_stat == 'Calibration':
        stat = 'Calibration'
    elif curr_stat == 'Average':
        stat = 'Avg'
    elif curr_stat == 'Standard Deviation':
        stat = 'StdDev'
    
    file = open(os.path.join('ModelResults', 'kh_{0}.dat'.format(stat)), 'r')
    vals = file.readlines()
    vals_arr = np.array(vals).astype(np.float)
    return vals_arr

def mapKDistribution(mg, strt_ind, end_ind, currParam, k_arr, currLayer, curr_Run):
    if currParam == 'kh':
        bounds = [1.0e-6, 1.0e-5, 5.0e-5, 1.0e-4, 5.0e-4, 1.0e-3, 5.0e-3, 1.0e-2, 5.0e-2, 1.0e-1]
        rgb = [[102,0,0],[204,0,0],[255,128,0],[255,255,102],[128,128,128],[102,255,102],[0,255,255],[0,0,255],[76,0,153]]
        rgb=np.array(rgb)/255.0
        cmap = matplotlib.colors.ListedColormap(rgb,"")
        norm = matplotlib.colors.BoundaryNorm(bounds, 10)
        frmt = '%.2E'
        cbar_label = 'Kh (cm/s)'
        
    if curr_Run == 'Calibration':
        plt_title = '{0} Distribution from Calibration Run in Layer {1}'.format(currParam, currLayer)
        bounds = [1.0e-6, 1.0e-5, 5.0e-5, 1.0e-4, 5.0e-4, 1.0e-3, 5.0e-3, 1.0e-2, 5.0e-2, 1.0e-1]
        rgb = [[102,0,0],[204,0,0],[255,128,0],[255,255,102],[128,128,128],[102,255,102],[0,255,255],[0,0,255],[76,0,153]]
        rgb=np.array(rgb)/255.0
        cmap = matplotlib.colors.ListedColormap(rgb,"")
        norm = matplotlib.colors.BoundaryNorm(bounds, 10)
        frmt = '%.2E'
        cbar_label = 'Kh (cm/s)'
    if curr_Run == 'Average':
        plt_title = '{0} Distribution from Average of All Realizations in Layer {1}'.format(currParam, currLayer)
        bounds = [1.0e-6, 1.0e-5, 5.0e-5, 1.0e-4, 5.0e-4, 1.0e-3, 5.0e-3, 1.0e-2, 5.0e-2, 1.0e-1]
        rgb = [[102,0,0],[204,0,0],[255,128,0],[255,255,102],[128,128,128],[102,255,102],[0,255,255],[0,0,255],[76,0,153]]
        rgb=np.array(rgb)/255.0
        cmap = matplotlib.colors.ListedColormap(rgb,"")
        norm = matplotlib.colors.BoundaryNorm(bounds, 10)
        frmt = '%.2E'
        cbar_label = 'Kh (cm/s)'
    if curr_Run == 'Standard Deviation':
        plt_title = '{0} Distribution from Std Dev of All Realizations in Layer {1}'.format(currParam, currLayer)
        bounds = [0.0, 1.0e-5, 1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1, 1.0e+0, 1.0e+1, 1.0e+2, 1.0e+3]
        rgb = [[102,0,0],[204,0,0],[255,128,0],[255,255,102],[128,128,128],[102,255,102],[0,255,255],[0,0,255],[76,0,153]]
        rgb=np.array(rgb)/255.0
        cmap = matplotlib.colors.ListedColormap(rgb,"")
        norm = matplotlib.colors.BoundaryNorm(bounds, 10)
        frmt = '%.2E'
        cbar_label = 'Kh (cm/s)'
        
    plt_arr = k_arr[strt_ind[currLayer-1]:end_ind[currLayer-1]]
    fig = plt.figure(figsize=(10, 10), constrained_layout = True)
    ax = fig.add_subplot(1, 1, 1, aspect='equal')
    ax.set_title(plt_title)
    mm = flopy.plot.PlotMapView(modelgrid=mg, ax=ax, layer = 0)
    mm.plot_grid(edgecolor='black', linewidths = 0.05)
    arr = mm.plot_array(a=plt_arr, cmap = cmap, norm = norm)
    cbar = fig.colorbar(arr, shrink = 0.55, format = frmt)
    cbar.set_label(cbar_label, rotation = 270, labelpad = 20)
    return plt

def app(): 
    #Binary grid file and nodal info   
    grbFile = 'CD_00.dis.grb'
    num_Layers = 37
    num_Nodes = 257224

    #Get nodal index info
    strt_ind = []
    end_ind = []
    layers_list = []
    n = 0
    index = 0
    while n < num_Layers:
        strt_ind.append(index)
        index += 6952
        end_ind.append(index)
        layers_list.append(n+1)
        n += 1

    #Get layer info 
    n_Years = 10
    years_list = []
    n = 0
    while n < n_Years:
        years_list.append(n+1)
        n += 1

    grbPath = os.path.join('ModelFiles', grbFile)
    grd = flopy.mf6.utils.binarygrid_util.MfGrdFile(grbPath, verbose=False)
    mg = grd.modelgrid

    #Establish sidebar setup
    st.title('Hydraulic Conductivity Distributions')
    
    row1_1, row1_2 = st.columns((3,3))
    with row1_1:
        layer_select = st.selectbox('Select a Layer:', layers_list)

    with row1_2:
        stat_select = st.selectbox('Select a Statistic:', ('Average', 'Standard Deviation'))

    row2_1, row2_2 = st.columns((3,3))

    #Plot Calibration Ks
    k_arr_1 = getKValArr('Calibration')
    calibfig = mapKDistribution(mg, strt_ind, end_ind, 'kh', k_arr_1, layer_select, 'Calibration')
    with row2_1:
        st.pyplot(calibfig)
        
    #Plot Avg Ks
    k_arr_1 = getKValArr(stat_select)
    avg_k_fig = mapKDistribution(mg, strt_ind, end_ind, 'kh', k_arr_1, layer_select, stat_select)
    with row2_2:
        st.pyplot(avg_k_fig)