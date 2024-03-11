import streamlit as st

import pandas as pd

def show_about():
    st.header('About', divider='rainbow')

    st.subheader('Author')
    st.markdown('## Terry Djony')
    st.markdown('[LinkedIn](https://linkedin.com/terry-djony)')
    st.markdown('[Website](https://terrydjony.com)')
    st.markdown('[Github](https://github.com/terryds)')

    st.subheader('Contact')
    st.write('If you want to contact me, feel free to reach out to my LinkedIn, or email to terrydjony[at]gmail.com')