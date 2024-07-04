import random

import streamlit as st
from modules import web_unit

username = st.text_input("username")
email = st.text_input("email")
password = st.text_input("password")

if st.button("Create account"):
    uid = str(random.randint(1000,1000000))
    web_unit.create_user(username,email,password,uid)
