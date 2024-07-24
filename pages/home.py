import time
import streamlit as st
from modules import web_unit


#determine whether the user is login
if 'uid' not in st.session_state:
    st.title("welcome to GPT4 Authorship Identification, Please login first")

elif st.session_state.uid == 0:
    st.title("welcome to GPT4 Authorship Identification, Please login first")

#search the database for user info
else:
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    query = "SELECT username,is_teacher FROM userInfo WHERE userid='%s'" % st.session_state.uid
    df = conn.query(query)
    #if the query is empty,that means the there no uid in the database
    if df.empty:
        st.write(df.iloc[0]['username'])

    #if the user is teacher
    elif df['is_teacher'][0] == 1:
        username = df.iloc[0]['username']
        st.title("welcome to GPT4 Authorship Identification, " + username)

    #if the user is student, then print the result that they uploaded
    else:
        username = df.iloc[0]['username']
        st.title("welcome to GPT4 Authorship Identification, "+username)
        web_unit.check_uploads(username)