import streamlit as st
from modules import web_unit

if st.session_state['uid'] == 0:
    # 输入邮箱
    email = st.text_input("email")
    # 输入密码
    password = st.text_input("password")


    if st.button("登录",type="primary", key="login"):
        web_unit.check_user_info(email, password)


else:
    st.write("You have already logged in")

#注册按钮
if st.button("注册", key="register"):
    st.switch_page("pages/create.py")
