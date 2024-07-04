import streamlit as st

if 'uid' not in st.session_state:
    st.session_state.uid = 0
    st.title("welcome to GPT4 Authorship Identification, Please login first")

elif st.session_state.uid == 0:
    st.title("welcome to GPT4 Authorship Identification, Please login first")

else:
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    query = "SELECT username FROM userInfo WHERE userid='%s'" % st.session_state.uid
    df = conn.query(query)

    if df.empty:
        st.write("please login!!!.")
        st.switch_page("login.py")

    else:
        username = df.iloc[0]['username']
        st.title("welcome to GPT4 Authorship Identification, "+username)

