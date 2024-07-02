import streamlit as st

def check_user_info(email, password):
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )
    df = conn.query("select password,userId from userInfo WHERE email='%s'" % email)
    array = st.dataframe(df)
    st.write(array)


