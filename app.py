import streamlit as st
from multiapp import MultiApp
from apps import (
    Kh_pngs,
    Kh_Summary,
    KhKv_pngs,
    KhKv_Summary,
    concvals_pngs,
    conc_gifs,
)

st.set_page_config(layout="wide")

apps = MultiApp()

# Add all your application here

apps.add_app("Kh Maps", Kh_pngs.app)
apps.add_app("Kh Summary", Kh_Summary.app)
apps.add_app("KhKv Maps", KhKv_pngs.app)
apps.add_app("KhKv Summary", KhKv_Summary.app)
apps.add_app("Transport Results", concvals_pngs.app)
apps.add_app("Plume Animations", conc_gifs.app)

# The main app
apps.run()
