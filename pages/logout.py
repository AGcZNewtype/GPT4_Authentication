import streamlit as st
import time

#Determine if the user is logged in
if "uid" not in st.session_state or st.session_state.uid == 0:
    st.title("Sorry! You haven't log in!")

#if logged in, clear the session key to log out
else:
    st.session_state.uid = 0

    st.title("Successfully logged out!")
    time.sleep(3)
    #switch to main page
    st.switch_page("pages/home.py")