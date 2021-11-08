import streamlit as st
import os
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def app():
    #Get nodal index info
    num_Layers = 37
    layers_list = []
    n = 0
    while n < num_Layers:
        layers_list.append(n+1)
        n += 1 
    
    hist_df = pd.read_csv(os.path.join('ModelResults', 'Kh_Histogram_Data_Geomean.csv'))
    zone_list = hist_df.columns.values.tolist()
    zone_list.pop(0)
    zone_list.pop(-1)
    zone_list = list(set(zone_list))
    # zone_list = list(map(float, zone_list))
    # zone_list = list(map(int, zone_list))
    zone_list.sort()
    
    st.title('Kh Summary')
    # layer_select = st.sidebar.selectbox('Select a Layer:', layers_list) 
    zone_select = st.sidebar.selectbox('Select a K Zone:', zone_list)
    # zone_idx = zone_list.index(zone_select)
    
    # row1_1 = st.columns(3)
    
    # with row1_1:
    fig = px.histogram(hist_df, 
                       x= hist_df[zone_select],
                       color = 'Series',
                       barmode = 'overlay',
                       title = 'Average Kh Distribution for {0}'.format(zone_select))
    fig.update_layout(xaxis = dict(showexponent = 'all', 
                                   exponentformat = 'E',
                                   title = 'Kh (cm/s)'),
                      bargap = 0.15)
    st.plotly_chart(fig, use_container_width = True)
    
    in_csv = './ModelResults/IES_Kvals.csv'
    df = pd.read_csv(in_csv)
    row2_1, row2_2 = st.columns((3,3))
    with row2_1:
        zone_num = int(zone_select.split('Zone')[1])
        # box_df = df.loc[df['Layer'] == layer_select]
        box_df = df.loc[df['Zone'] == zone_num]
        # box_df = df.loc[(df['Zone'] == zone_num) & (df['Layer']==layer_select)]
        box_fig = go.Figure()
        y0 = box_df['kh_cps_Calibration']
        y1 = box_df['kh_cps_Base']
        y2 = box_df['Kh_ies_avg']
        points = False
        box_fig.add_trace(go.Box(y = y0, boxpoints = points, name = 'Calibration'))
        box_fig.add_trace(go.Box(y = y1, boxpoints = points, name = 'IES Base'))
        box_fig.add_trace(go.Box(y = y2, boxpoints = points, name = 'IES Average'))
        box_fig.update_layout(title = 'K Value Distribution', yaxis = dict(showexponent = 'all', exponentformat = 'E', title = 'Kh (cm/s)'))
        st.plotly_chart(box_fig, use_container_width = True)
    
    stat_df = box_df[['kh_cps_Calibration', 'kh_cps_Base', 'Kh_ies_avg']]
    pd.set_option('display.float_format', lambda x: '%g' % x)
    with row2_2:
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.table(stat_df.describe().style.format('{:7,.3E}'))