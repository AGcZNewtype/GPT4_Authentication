import streamlit as st
from modules import web_unit
import time

if st.session_state['uid'] == 0:
    st.title("Please log in here!")
    # input email
    email = st.text_input("email")
    # input password
    password = st.text_input("password",type="password")


    #Query user information
    if st.button("Login", key="login"):
        if web_unit.validate(email, "em")and web_unit.validate(password, "pw"):
            web_unit.check_user_info(email, password)
        else:
            st.warning("input formal error!")


else:
    st.write("You have already logged in")
    time.sleep(3)
    st.switch_page("pages/home.py")

#注册按钮
if st.button("Register",type="primary", key="register"):
    st.switch_page("pages/register.py")
