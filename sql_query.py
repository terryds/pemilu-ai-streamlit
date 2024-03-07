import streamlit as st

import duckdb
import pandas as pd

# Function to run a query
def run_query(conn, query):
    rows = conn.execute(query).fetchall()
    return rows

def show_sql_query(conn):
    st.header('SQL Query', divider='rainbow')

    query = st.text_area("Enter your query", "SELECT * FROM provinsi_data")
    if st.button("Run"):
        rows = run_query(conn, query)
        # Display results
        if rows:
            df = pd.DataFrame(rows)
            st.write(df)
        else:
            st.write("Query returned no results")