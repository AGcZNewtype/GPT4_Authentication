import random
import streamlit as st
from modules import web_unit

# Create user information input fields
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password")

# Start account registration
if st.button("Create account"):
    # Generate UID using hash
    uid = web_unit.generate_hash(str(email) + str(password) + str(username))
    # Generate a random number as salt
    salt = random.randint(10000, 9999999)
    # Use salt to obfuscate and hash the password
    password_salt = web_unit.generate_hash(str(password) + str(salt))

    # Check if user inputs meet regularization criteria
    if web_unit.validate(email, "em") and web_unit.validate(username, "1") and web_unit.validate(password, "pw"):
        # Call the method to create the account
        web_unit.create_user(username, email, password_salt, salt, uid)
        st.switch_page("pages/login.py")
    else:
        st.warning("Input format error!")
