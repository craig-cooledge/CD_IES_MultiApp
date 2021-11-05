import streamlit as st
import os
import pandas as pd
import plotly.express as px
import numpy as np

def app():
    hist_df = pd.read_csv(os.path.join('ModelResults', 'Kh_Histogram_Data.csv'))
    zone_list = hist_df.columns.values.tolist()
    zone_list.pop(0)
    zone_list.pop(-1)
    zone_list = list(set(zone_list))
    zone_list = list(map(float, zone_list))
    zone_list = list(map(int, zone_list))
    zone_list.sort()
    
    st.title('Kh Summary')
    row1_1, row1_2 = st.columns((3,3))
    with row1_1:
        zone_select = int(float(st.selectbox('Select a K Zone:', zone_list)))
        fig = px.histogram(hist_df, 
                           x= hist_df.columns[zone_select],
                           color = 'Series',
                           barmode = 'overlay',
                           title = 'Average Kh Distribution for Zone {0}'.format(str(int(zone_select))))
        fig.update_layout(xaxis = dict(showexponent = 'all', 
                                       exponentformat = 'E',
                                       title = 'Kh (cps)'),
                          bargap = 0.15)
        st.plotly_chart(fig)
    