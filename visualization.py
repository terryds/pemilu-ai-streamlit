import streamlit as st

import duckdb
import pandas as pd

# Get all provinsi
def get_list_of_provinsi(conn):
    query = "SELECT nama FROM provinsi_data"
    result = conn.execute(query).fetchall()
    return [row[0] for row in result]

def show_visualization(conn):
    st.header('Visualization', divider='rainbow')

    # Dropdowns for filters
    provinsi = st.selectbox('Select Provinsi', ['All'] + get_list_of_provinsi(conn))