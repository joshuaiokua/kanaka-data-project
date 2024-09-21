"""
Streamlit Application

Entrypoint file for Streamlit application.
"""
# ruff: noqa: B018

import numpy as np
import pandas as pd
import streamlit as st

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("Choose a datapoint color")
color = st.color_picker("Color", st.get_option("theme.primaryColor"))
st.divider()
st.scatter_chart(st.session_state.df, x="x", y="y", color=color)
