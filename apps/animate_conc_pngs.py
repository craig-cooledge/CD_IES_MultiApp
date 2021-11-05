import streamlit as st
import os
import time

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
    #Get layer info 
    n_Years = 10
    years_list = []
    n = 0
    while n < n_Years:
        years_list.append(n+1)
        n += 1
    
    st.title('Transport Modeling Results')

    row1_1, row1_2 = st.columns((3,3))
    # year_select = st.slider('Select a Year:', 1, 10, 1, 1)
    
    year_select = 1
    # st.button('Animate Plume', on_click = )
    with row1_1:
        layer_select = st.sidebar.selectbox('Select a Layer:', layers_list)
        
        n = 0
        img_list = []
        while n < n_Years:
            img_list.append(os.path.join('ModelResults', 'Conc_PNGs', 'AvgConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, n+1)))
            n += 1
        
        avg_png_name = img_list[0]
        if st.sidebar.button('Animate Plume'):
            x = 1
            year_select += 1
            while x < n_Years-1:
                avg_png_name = img_list[year_select]
                placeholder = st.image(avg_png_name)
                time.sleep(1.0)
                placeholder.empty()
                x += 1
                year_select += 1
        else:
            placeholder = st.image(avg_png_name)
        
        avg_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'AvgConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))
        placeholder = st.image(avg_png_name)
        # placeholder.empty()

    # with row1_2:
        # layer_select = st.selectbox('Select a Layer:', layers_list)
    
    # avg_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'AvgConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))
    # stdv_png_name = os.path.join('ModelResults', 'Conc_PNGs', 'StdDevConc_L{0:0=3d}_Year{1:0=3d}.png'.format(layer_select, year_select))

    # row2_1, row2_2 = st.columns((3,3))
    # with row2_1:
       # st.image(avg_png_name)
        
    # with row2_2:
       # st.image(stdv_png_name)