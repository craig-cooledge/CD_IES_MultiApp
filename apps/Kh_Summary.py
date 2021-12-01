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
        
    #Get Zone Descriptions
    in_descr = open(os.path.join('ModelFiles', 'KZoneDescriptions.txt'), 'r')
    zone_descr = in_descr.readlines()
    zone_list = []
    for item in zone_descr:
        list_val = item.split(' ')[0] + ' - ' + item.split(' ')[1]
        zone_list.append(list_val.strip('\n'))
    
    hist_df = pd.read_csv(os.path.join('ModelResults', 'Kh_Histogram_Data.csv'))

    zone_select = st.sidebar.selectbox('Select a K Zone:', zone_list)
    plot_zone = 'Zone {0:0=3d}'.format(int(zone_select[0:3]))
    
    st.title('Kh summary for K Zone: {0}'.format(zone_select))
    
    fig = px.histogram(hist_df, 
                       x= hist_df[plot_zone],
                       color = 'Series',
                       barmode = 'overlay',
                       title = 'Average Kh Distribution for {0}'.format(plot_zone))
    fig.update_layout(xaxis = dict(showexponent = 'all', 
                                   exponentformat = 'E',
                                   title = 'Kh (cm/s)'),
                      bargap = 0.15)
    st.plotly_chart(fig, use_container_width = True)
    
    in_csv = './ModelResults/IES_Nodal_KVals.csv'
    df = pd.read_csv(in_csv)
    row2_1, row2_2 = st.columns((3,3))
    with row2_1:
        zone_num = int(zone_select[0:3])
        box_df = df.loc[df['Zone'] == zone_num]
        box_fig = go.Figure()
        y0 = box_df['Kh_cps_fromMS']
        y1 = box_df['Kh_cps_Calibration']
        y2 = box_df['Kh_cps_Base']
        y3 = box_df['Kh_cps_IES_Avg']
        points = False
        box_fig.add_trace(go.Box(y = y0, boxpoints = points, name = 'Matrix Solutions'))
        box_fig.add_trace(go.Box(y = y1, boxpoints = points, name = 'Calibration'))
        box_fig.add_trace(go.Box(y = y2, boxpoints = points, name = 'IES Realization Base'))
        box_fig.add_trace(go.Box(y = y3, boxpoints = points, name = 'IES Realization Average'))
        box_fig.update_layout(title = 'Nodal Kh Distribution', yaxis = dict(showexponent = 'all', exponentformat = 'E', title = 'Kh (cm/s)'))
        st.plotly_chart(box_fig, use_container_width = True)
    
    stat_df = box_df[['Kh_cps_fromMS','Kh_cps_Calibration', 'Kh_cps_Base', 'Kh_cps_IES_Avg']]
    pd.set_option('display.float_format', lambda x: '%g' % x)
    with row2_2:
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.table(stat_df.describe().style.format('{:7,.3E}'))