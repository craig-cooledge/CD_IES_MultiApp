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
    
    #Get layer info 
    n_Years = 10
    years_list = []
    n = 0
    while n < n_Years:
        years_list.append(n+1)
        n += 1
    
    st.title('Plume Animation by Layer')
    
    layer_select = st.sidebar.selectbox('Select a Layer:', layers_list)
    
    avg_gif = os.path.join('ModelResults','Conc_GIFs','L{0:0=3d}_AvgConc_Plume.gif'.format(layer_select))
    stddev_gif = os.path.join('ModelResults','Conc_GIFs','L{0:0=3d}_StdDevConc_Plume.gif'.format(layer_select))
    
    row1_1, row1_2 = st.columns((3,3))
    with row1_1:
        st.image(avg_gif)
        
    with row1_2:
        st.image(stddev_gif)
    
    
    

    