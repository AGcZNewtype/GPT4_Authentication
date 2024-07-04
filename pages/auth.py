import streamlit as st
from modules import authenticate




#检测用户是否登录
if st.session_state["uid"] == 0:
    ##未登录跳转到登录界面
    st.subheader("please login first")
    st.switch_page("pages/login.py")


#登陆成功则显示上产界面
else:
    authenticate.upload()


