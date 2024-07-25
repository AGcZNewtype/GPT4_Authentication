import streamlit as st


#create navigator constraction
pages = {
    "Your account" : [
        st.Page("pages/home.py", title="Home Page"),
        st.Page("pages/login.py", title="Log In"),
st.Page("pages/register.py", title="Register"),
        st.Page("pages/logout.py", title="Log Out")
    ],
    "Authenticator" : [
        st.Page("pages/auth.py", title="authenticate Document"),
        st.Page("pages/view.py", title="View Result")
    ]
}


#initilize session key.
if 'uid' not in st.session_state:
    st.session_state.uid = 0

#run the navigation
pg = st.navigation(pages)
pg.run()

