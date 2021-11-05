import streamlit as st
from multiapp import MultiApp
from apps import (
    k_pngs,
    kvals_summary,
    concvals_pngs,
    conc_gifs,
)

st.set_page_config(layout="wide")

apps = MultiApp()

# Add all your application here

apps.add_app("Kh Maps", k_pngs.app)
apps.add_app("Kh Summary", kvals_summary.app)
apps.add_app("Transport Results", concvals_pngs.app)
apps.add_app("Plume Animations", conc_gifs.app)

# The main app
apps.run()
