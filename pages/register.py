import random
import streamlit as st
from modules import web_unit

username = st.text_input("username")
email = st.text_input("email")
password = st.text_input("password")

if st.button("Create account"):
    uid = web_unit.generate_hash(str(email)+str(password)+str(username))
    salt = random.randint(10000, 9999999)
    password_salt = web_unit.generate_hash(str(password) + str(salt))
    # print("this is create:", password,salt, password_salt)
    web_unit.create_user(username,email,password_salt,salt,uid)
    st.switch_page("pages/login.py")