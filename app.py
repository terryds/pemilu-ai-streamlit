import streamlit as st
import duckdb

from visualization import show_visualization
from sql_query import show_sql_query
from ask_ai import show_ask_ai

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return duckdb.connect(database='pemilu2024-kpu.duckdb', read_only=True)

conn = init_connection()


# Function to run a query
def run_query(query):
    rows = conn.execute(query).fetchall()
    return rows



# Streamlit widgets to take user input.

st.title('2024 Indonesian Presidential Election Visualization')


st.sidebar.title('Navigation')
page = st.sidebar.radio('Select a Page:', ['Data Visualization', 'SQL Query', 'Ask AI'])

if page == 'Data Visualization':
    show_visualization(conn)
elif page == 'SQL Query':
    show_sql_query(conn)
elif page == 'Ask AI':
    show_ask_ai(conn)