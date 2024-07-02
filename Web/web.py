import streamlit as st
import streamlit_authenticator as stauth


st.write("Hello world")

conn = st.connection(
    "local_db",
    type="sql",
    url="mysql://root:root@localhost:3306/streamlitDB"
)
df = conn.query("select * from userInfo")
array = st.dataframe(df)

st.write(type[array])