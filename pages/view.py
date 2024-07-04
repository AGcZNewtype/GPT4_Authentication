import streamlit as st
from modules import web_unit

if 'uid' not in st.session_state:
    st.switch_page("app.py")

elif st.session_state['uid'] == 0:
    st.write("Please login first!")

else:
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    query = "SELECT username,is_teacher FROM userInfo WHERE userid='%s'" % st.session_state.uid
    df = conn.query(query)

    if df.iloc[0]['is_teacher'] == 1:
        username = df.iloc[0]['username']
        st.title("welcome, " + username)
        web_unit.check_uploads()

    else:
        st.write("Sorry, you don't have the permission to do that!")


