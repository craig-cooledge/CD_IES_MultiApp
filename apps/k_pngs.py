import streamlit as st
import os

def app():
    #Get nodal index info
    num_Layers = 37
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
        
    in_desc = open(os.path.join('ModelFiles', 'LayerDescriptions.txt'), 'r')
    descr_list = in_desc.readlines()
    
    # st.title('Hydraulic Conductivity Distributions')
    row1_1, row1_2 = st.columns((1,1))
    with row1_1:
        layer_select = st.sidebar.selectbox('Select a Layer:', layers_list)

    with row1_2:
        stat_select = st.sidebar.selectbox('Select a Statistic:', ('Average', 'Standard Deviation'))
    
    st.title(descr_list[layer_select-1])
    row2_1, row2_2 = st.columns((3,3))
    calib_png_name = os.path.join('ModelResults', 'K_PNGs', 'kh_L{0:0=3d}_Calibration.png'.format(layer_select))
    with row2_1:
        st.image(calib_png_name)
    
    if stat_select == 'Average':
        ies_png_name = os.path.join('ModelResults', 'K_PNGs', 'kh_L{0:0=3d}_IESAvg.png'.format(layer_select))
    elif stat_select == 'Standard Deviation':
        ies_png_name = os.path.join('ModelResults', 'K_PNGs', 'kh_L{0:0=3d}_IESStdDev.png'.format(layer_select))
       
    with row2_2:
        st.image(ies_png_name)