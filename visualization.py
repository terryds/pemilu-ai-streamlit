import streamlit as st
import duckdb
import pandas as pd

# Function to fetch options for dropdowns from the database and add "All" option
def fetch_options(conn, table_name, column_id=None, selected_id=None):
    if column_id and selected_id:
        query = f"SELECT id, nama FROM {table_name} WHERE {column_id} = {selected_id};"
    else:
        query = f"SELECT id, nama FROM {table_name};"
    data = pd.read_sql_query(query, conn)
    options = {'All': 'All'}
    options.update(data.set_index('id').to_dict()['nama'])
    return options


def show_visualization(conn):
    st.header('Regional Vote Data Visualization', divider='rainbow')

    st.info('Database retrieved from https://github.com/terryds/pemilu-2024-scraper/releases (Last update is on March, 5th)')
    st.info('Please note that KPU (General Election Committee) said there might be some invalid data, related to OCR issues and some data may not have been inputted yet. Source: https://www.cnnindonesia.com/nasional/20240304163444-617-1070317/kpu-sebut-suara-psi-janggal-akibat-teknologi-ocr-sirekap-tidak-akurat')

    # Dropdown for Provinsi
    provinsi_options = fetch_options(conn, 'provinsi_data')
    selected_provinsi = st.selectbox('Select Provinsi', options=list(provinsi_options.keys()), format_func=lambda x: provinsi_options[x], index=0)

    # Dropdown for Kota
    kota_options = fetch_options(conn, 'kota_data', 'provinsi_id', selected_provinsi) if selected_provinsi != 'All' else {'All': 'All'}
    selected_kota = st.selectbox('Select Kota', options=list(kota_options.keys()), format_func=lambda x: kota_options[x], index=0)

    # Dropdown for Kecamatan
    kecamatan_options = fetch_options(conn, 'kecamatan_data', 'kota_id', selected_kota) if selected_kota != 'All' else {'All': 'All'}
    selected_kecamatan = st.selectbox('Select Kecamatan', options=list(kecamatan_options.keys()), format_func=lambda x: kecamatan_options[x], index=0)

    # Dropdown for Kelurahan
    kelurahan_options = fetch_options(conn, 'kelurahan_data', 'kecamatan_id', selected_kecamatan) if selected_kecamatan != 'All' else {'All': 'All'}
    selected_kelurahan = st.selectbox('Select Kelurahan', options=list(kelurahan_options.keys()), format_func=lambda x: kelurahan_options[x], index=0)

    # Dropdown for TPS
    tps_options = fetch_options(conn, 'tps_data', 'kelurahan_id', selected_kelurahan) if selected_kelurahan != 'All' else {'All': 'All'}
    selected_tps = st.selectbox('Select TPS', options=list(tps_options.keys()), format_func=lambda x: tps_options[x], index=0)

    # Building the WHERE clause based on selections
    where_clauses = []
    if selected_provinsi != 'All':
        where_clauses.append(f"provinsi_id = {selected_provinsi}")
    if selected_kota != 'All':
        where_clauses.append(f"kota_id = {selected_kota}")
    if selected_kecamatan != 'All':
        where_clauses.append(f"kecamatan_id = {selected_kecamatan}")
    if selected_kelurahan != 'All':
        where_clauses.append(f"kelurahan_id = {selected_kelurahan}")
    if selected_tps != 'All':
        where_clauses.append(f"tps_id = {selected_tps}")

    where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    # Query based on selections
    query = f"""
    SELECT 
        SUM(jumlah_suara_pasangan01_anies_imin) AS jumlah_suara_pasangan_01,
        SUM(jumlah_suara_pasangan02_prabowo_gibran) AS jumlah_suara_pasangan_02,
        SUM(jumlah_suara_pasangan03_ganjar_mahfud) AS jumlah_suara_pasangan_03,

        SUM(suara_sah) AS total_suara_sah,
        SUM(suara_tidak_sah) AS total_suara_tidak_sah,
        SUM(suara_total) AS total_suara,
        SUM(pemilih_dpt_total) AS pemilih_dpt_total,
        SUM(pengguna_dpt_total) AS pengguna_dpt_total
    FROM suara_detailed_view
    {where_clause};
    """
    
    df = pd.read_sql_query(query, conn)

    # Display Results
    if not df.empty:
        st.header("Hasil")
        total_valid_votes = df['jumlah_suara_pasangan_01'].sum() + df['jumlah_suara_pasangan_02'].sum() + df['jumlah_suara_pasangan_03'].sum()
        for col in ['jumlah_suara_pasangan_01', 'jumlah_suara_pasangan_02', 'jumlah_suara_pasangan_03']:
            votes = df[col].sum()
            percentage = (votes / total_valid_votes * 100) if total_valid_votes > 0 else 0
            st.metric(label=f"{col} (Percentage)", value=f"{votes:,} ({percentage:.2f}%)")
        for col in df.columns:
            if col not in ['jumlah_suara_pasangan_01', 'jumlah_suara_pasangan_02', 'jumlah_suara_pasangan_03']:
                st.metric(label=col, value=f"{df[col].sum():,}")
    else:
        st.write("No data available for the selected criteria.")