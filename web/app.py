import streamlit as st
from modules import login


st.write("输入邮箱：")
st.text_input("email")
st.write("输入密码：")
st.text_input("password")
login.check_user_info()