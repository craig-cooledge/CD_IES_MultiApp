import streamlit as st
import os

def app():    
    num_Layers = 37
    num_Nodes = 257224

    #Get nodal index info
    layers_list = []
    n = 0
    index = 0
    while n < num_Layers:
        layers_list.append(n+1)
        n += 1

    #Get layer info 
    n_Years = 10
    years_list = []
    n = 0
    while n < n_Years:
        years_list.append(n+1)
        n += 1

    st.title('Transport Modeling Results')
                      
    row1_1, row1_2 = st.columns((3,3))
    with row1_1:
        year_select = st.sidebar.slider('Select a Year:', 1, 10)
        
    with row1_2:
        layer_select = st.sidebar.selectbox('Select a Layer:', layers_list)

    row2_1, row2_2 = st.columns((3,3))
    avg_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'AvgConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))
    with row2_1:
        st.image(avg_png_name)

    #Plot Concentration Standard Deviation
    stdv_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'StdDevConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))
    with row2_2:
        st.image(stdv_png_name)