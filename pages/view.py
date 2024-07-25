import streamlit as st
from modules import web_unit

# Check if the user is logged in
if 'uid' not in st.session_state:
    st.switch_page("pages/home.py")

elif st.session_state['uid'] == 0:
    st.write("Please login first!")

# User is logged in
else:
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    # Query the database to determine if the user is an admin
    query = "SELECT username, is_teacher FROM userInfo WHERE userid='%s'" % st.session_state.uid
    df = conn.query(query)

    # Check if the user is an admin
    if df.iloc[0]['is_teacher'] == 1:
        username = df.iloc[0]['username']
        st.title("Welcome, " + username)
        web_unit.check_uploads("all")

    else:
        st.write("Sorry, you don't have the permission to do that!")
