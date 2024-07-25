import streamlit as st
from modules import authenticate
import time


#Check if the user is logged in
if st.session_state["uid"] == 0:
    ##If you are not logged in, jump to the login interface
    st.subheader("please login first")
    time.sleep(3)
    st.switch_page("pages/login.py")


#If the login is successful, the authentication interface will be displayed.
else:
    authenticate.upload()


