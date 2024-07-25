import time
import streamlit as st
import mysql.connector
import random
from mysql.connector import Error
import hashlib
import re

# Generate a hash from a given input string
def generate_hash(input_string):
    input_bytes = input_string.encode('utf-8')
    hash_object = hashlib.sha256(input_bytes)
    hash_hex = hash_object.hexdigest()
    return hash_hex[:20]

# Function to check user information for login
def check_user_info(email, password):
    # Establish database connection
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    # Query the database
    query = "SELECT username, password, salt, userid FROM userInfo WHERE email='%s'" % email
    df = conn.query(query)

    # Check if the query result is empty
    if df.empty:
        st.write("No user found with this email.")
        return

    # Get password and userId from the query result
    password_db = df.iloc[0]['password']
    uid = df.iloc[0]['userid']
    salt = df.iloc[0]['salt']
    username = df.iloc[0]['username']
    password_salt = generate_hash(str(password) + str(salt))
    # print("this is login:", salt, password_salt, password_db)

    # Verify the password
    if password_db == password_salt:
        st.write("ok!")
        st.session_state.uid = uid
        st.session_state.username = username
        st.switch_page("pages/home.py")
    else:
        st.warning("Wrong password!!")

# Function to create a new user
def create_user(username, email, password, salt, userid):
    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host='localhost',
            database='streamlitDB',
            user='root',
            password='root'
        )

        if conn.is_connected():
            cursor = conn.cursor()
            # Generate SQL insert query
            query = """
                INSERT INTO userInfo (username, email, password, salt, userid)
                VALUES (%s, %s, %s, %s, %s)
            """
            # Execute the query and commit the changes
            cursor.execute(query, (username, email, password, salt, userid))
            conn.commit()
            # print(st.session_state.uid)
            st.write("Registered successfully!")

    except Error as e:
        # st.write(f"Error: {e}")
        st.warning("Already registered!")
        time.sleep(3)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Check uploads
def check_uploads(username):
    if username == "all":
        query = "SELECT item_id, item_name, uploader, score FROM result WHERE 1"
    else:
        query = "SELECT item_id, item_name, uploader, score FROM result WHERE uploader='%s'" % username
    conn = st.connection(
        name="local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    df = conn.query(query)

    if df.empty:
        st.write("It's empty! Waiting for upload!!!")
    else:
        # Use st.dataframe to create a scrollable data frame
        st.dataframe(df, width=800, height=440, hide_index=True)
        # Print the query results for debugging

# Add a result to the database
def add_result(item_id, item_name, uploader, score):
    try:
        # Establish database connection
        conn = mysql.connector.connect(
            host='localhost',
            database='streamlitDB',
            user='root',
            password='root'
        )

        if conn.is_connected():
            cursor = conn.cursor()
            # Generate SQL insert query
            query = """
                INSERT INTO result (item_id, item_name, uploader, score)
                VALUES (%s, %s, %s, %s)
            """
            # Execute the query and commit the changes
            cursor.execute(query, (item_id, item_name, uploader, score))
            conn.commit()
            st.write("Submitted successfully!")

    except Error as e:
        st.write(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to validate input text based on type
def validate(text, type):
    # Detect validation text type
    if type == "pw":
        # Password regex pattern
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if re.match(password_regex, text):
            return True
        else:
            return False
    # Detect email regex
    elif type == "em":
        # Email regex pattern
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, text):
            return True
        else:
            return False
    else:
        # Username regex pattern
        special_char_regex = r'[^a-zA-Z0-9]'
        if re.search(special_char_regex, text):
            return False
        else:
            return True
