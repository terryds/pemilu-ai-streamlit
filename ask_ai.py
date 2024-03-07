import streamlit as st
# from langchain.llms import OpenAI
# import duckdb

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.chat_models import ChatOpenAI

def generate_response(query, openai_api_key):
    placeholder = st.empty()
    placeholder.info('Thinking... Please wait for a few minutes. Do not change your input or click the submit button again before the answer pops up')
    prefix = """You are an agent designed to interact with a SQL database.
This is the details of the SQL database you're going to query:
CREATE TABLE IF NOT EXISTS provinsi_data (
                id INTEGER PRIMARY KEY NOT NULL,
                nama TEXT NOT NULL,
                kode TEXT NOT NULL,
                tingkat INTEGER NOT NULL,
                lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS kota_data (
                id INTEGER PRIMARY KEY NOT NULL,
                nama TEXT NOT NULL,
                kode TEXT NOT NULL,
                tingkat INTEGER NOT NULL,
                provinsi_id INTEGER REFERENCES provinsi_data(id),
                lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS kecamatan_data (
                id INTEGER PRIMARY KEY NOT NULL,
                nama TEXT NOT NULL,
                kode TEXT NOT NULL,
                tingkat INTEGER NOT NULL,
                kota_id INTEGER REFERENCES kota_data(id),
                lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS kelurahan_data (
                id INTEGER PRIMARY KEY NOT NULL,
                nama TEXT NOT NULL,
                kode TEXT NOT NULL,
                tingkat INTEGER NOT NULL,
                kecamatan_id INTEGER REFERENCES kecamatan_data(id),
                lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS tps_data (
                id INTEGER PRIMARY KEY NOT NULL,
                nama TEXT NOT NULL,
                kode TEXT NOT NULL,
                tingkat INTEGER NOT NULL,
                kelurahan_id INTEGER REFERENCES kelurahan_data(id),
                lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS suara_data (
                id VARCHAR(36) PRIMARY KEY NOT NULL,
                origin_url TEXT NOT NULL,
                jumlah_suara_pasangan01_anies_imin INTEGER,
                jumlah_suara_pasangan02_prabowo_gibran INTEGER,
                jumlah_suara_pasangan03_ganjar_mahfud INTEGER,
                image_urls TEXT,
                suara_sah INTEGER,
                suara_tidak_sah INTEGER,
                suara_total INTEGER,
                pemilih_dpt_total INTEGER,
                pemilih_dpt_lelaki INTEGER,
                pemilih_dpt_perempuan INTEGER,
                pengguna_dpt_total INTEGER,
                pengguna_dpt_lelaki INTEGER,
                pengguna_dpt_perempuan INTEGER,
                pengguna_dptb_total INTEGER,
                pengguna_dptb_lelaki INTEGER,
                pengguna_dptb_perempuan INTEGER,
                pengguna_total INTEGER,
                pengguna_total_lelaki INTEGER,
                pengguna_total_perempuan INTEGER,
                pengguna_non_dpt_total INTEGER,
                pengguna_non_dpt_lelaki INTEGER,
                pengguna_non_dpt_perempuan INTEGER,
                psu TEXT,
                status_suara BOOLEAN,
                status_adm BOOLEAN,
                ts TIMESTAMP,
                tps_id INTEGER REFERENCES tps_data(id),
                lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            );
            CREATE VIEW IF NOT EXISTS suara_detailed_view AS
                SELECT 
                    sd.id,
                    sd.origin_url,
                    sd.jumlah_suara_pasangan01_anies_imin,
                    sd.jumlah_suara_pasangan02_prabowo_gibran,
                    sd.jumlah_suara_pasangan03_ganjar_mahfud,
                    sd.image_urls,
                    sd.suara_sah,
                    sd.suara_tidak_sah,
                    sd.suara_total,
                    sd.pemilih_dpt_total,
                    sd.pemilih_dpt_lelaki,
                    sd.pemilih_dpt_perempuan,
                    sd.pengguna_dpt_total,
                    sd.pengguna_dpt_lelaki,
                    sd.pengguna_dpt_perempuan,
                    sd.pengguna_dptb_total,
                    sd.pengguna_dptb_lelaki,
                    sd.pengguna_dptb_perempuan,
                    sd.pengguna_total,
                    sd.pengguna_total_lelaki,
                    sd.pengguna_total_perempuan,
                    sd.pengguna_non_dpt_total,
                    sd.pengguna_non_dpt_lelaki,
                    sd.pengguna_non_dpt_perempuan,
                    sd.psu,
                    sd.status_suara,
                    sd.status_adm,
                    sd.ts,
                    sd.lastupdated,
                    tps.nama AS nama_tps,
                    kel.nama AS nama_kelurahan,
                    kec.nama AS nama_kecamatan,
                    kot.nama AS nama_kota,
                    prov.nama AS nama_provinsi
                FROM 
                    suara_data sd
                    JOIN tps_data tps ON sd.tps_id = tps.id
                    JOIN kelurahan_data kel ON tps.kelurahan_id = kel.id
                    JOIN kecamatan_data kec ON kel.kecamatan_id = kec.id
                    JOIN kota_data kot ON kec.kota_id = kot.id
                    JOIN provinsi_data prov ON kot.provinsi_id = prov.id;

Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.
"""

    suffix = """If there is information about the question on the database schema on my system prompt, then I should use that information to see what I can query. If there is no information about the question on the database schema and I don't know what to query, I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables."""

    db = SQLDatabase.from_uri("duckdb:///pemilu2024-kpu.duckdb", {'connect_args': { 'read_only': True}})
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, openai_api_key=openai_api_key)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", prefix=prefix, suffix=suffix, verbose=True)
    result = agent_executor.invoke(query)
    st.success(result["output"])
    placeholder.empty()

def show_ask_ai(conn):
    st.header('Ask AI', divider="rainbow")

    if 'is_submitting' not in st.session_state:
        st.session_state.is_submitting = False

    openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=st.session_state.is_submitting)

    st.warning('Please note that there are still missing data in some of regions. For example, (as of March 6th, 2024), the data in https://pemilu2024.kpu.go.id/pilpres/hitung-suara/11/1118/111806/1118062041/1118062041001 (which API can be hit at https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/11/1118/111806/1118062041/1118062041001.json ) has not yet been inputted. Only some candidates get inputted', icon="⚠️")

    with st.form('my_form'):
        query = st.text_area('Ask something here', disabled=st.session_state.is_submitting)
        submitted = st.form_submit_button('Submit', disabled=st.session_state.is_submitting)
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            st.session_state.is_submitting = True
            generate_response(query, openai_api_key)
            st.session_state.is_submitting = False