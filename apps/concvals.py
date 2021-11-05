import streamlit as st
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import flopy

def getConcArr(year_select, stat_option):
    if stat_option == 'Average':
        curr_stat = 'Avg'
    elif stat_option == 'Standard Deviation':
        curr_stat = 'StdDev'
    file = open(os.path.join('ModelResults', 'Year_{0}_{1}_Concentration.dat'.format(year_select, curr_stat)), 'r')
    vals = file.readlines()
    vals_arr = np.array(vals).astype(float)
    return vals_arr

def mapConcentrations(mg, strt_ind, end_ind, concArr, currYear, stat_option, currLayer):
    if stat_option == 'Average':
        plot_stat = 'Avg'
        bounds = [0.0, 5.0, 50.0, 100.0, 250.0, 750.0, 1000.0, 1500.0, 2500.0]
        rgb = [[128,128,128],[0,0,153],[0,0,255],[0,128,255],[255,204,153],[255,128,0],[255,0,0],[153,0,0]]
        rgb=np.array(rgb)/255.0
        cmap = matplotlib.colors.ListedColormap(rgb,"")
        norm = matplotlib.colors.BoundaryNorm(bounds, 9)
        frmt = '%.0f'
        cbar_label = 'Avg Concentration (ug/L)'
    elif stat_option == 'Standard Deviation':
        plot_stat = 'StdDev'
        bounds = [0.0, 0.01, 0.1, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0]
        rgb = [[128,128,128],[0,0,153],[0,0,255],[0,128,255],[255,204,153],[255,128,0],[255,0,0],[153,0,0]]
        rgb=np.array(rgb)/255.0
        cmap = matplotlib.colors.ListedColormap(rgb,"")
        norm = matplotlib.colors.BoundaryNorm(bounds, 9)
        frmt = '%.2f'
        cbar_label = 'Concentration Std Dev (ug/L)'

    plt_arr = concArr[strt_ind[currLayer-1]:end_ind[currLayer-1]]
    fig = plt.figure(figsize=(10, 10), constrained_layout = True)
    ax = fig.add_subplot(1, 1, 1, aspect='equal')
    ax.set_title('{1} of Concentration for Year {0} in Layer {2}'.format(currYear, stat_option, currLayer))
    mm = flopy.plot.PlotMapView(modelgrid=mg, ax=ax, layer = 0)
    mm.plot_grid(edgecolor='black', linewidths = 0.50)
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

    st.title('Transport Modeling Results')
                      
    row1_1, row1_2 = st.columns((3,3))
    with row1_1:
        year_select = st.slider('Select a Year:', 1, 10)
        
    with row1_2:
        layer_select = st.selectbox('Select a Layer:', layers_list)

    row2_1, row2_2 = st.columns((3,3))
    #Plot avg concentrations
    # avgconcArr = getConcArr(year_select, 'Average')
    # avgfig = mapConcentrations(mg, strt_ind, end_ind, avgconcArr, year_select, 'Average', layer_select)
    avg_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'AvgConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))
    with row2_1:
        st.image(avg_png_name)
        # st.pyplot(avgfig, clear_figure = True)

    #Plot Concentration Standard Deviation
    # stdconcArr = getConcArr(year_select, 'Standard Deviation')
    # stdfig = mapConcentrations(mg, strt_ind, end_ind, stdconcArr, year_select, 'Standard Deviation', layer_select)
    stdv_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'StdDevConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))
    with row2_2:
        st.image(stdv_png_name)
        # st.pyplot(stdfig, clear_figure = True)