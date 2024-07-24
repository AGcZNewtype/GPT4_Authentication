import time
import streamlit as st
import mysql.connector
import random
from mysql.connector import Error
import hashlib

def generate_hash(input_string):
    input_bytes = input_string.encode('utf-8')
    hash_object = hashlib.sha256(input_bytes)
    hash_hex = hash_object.hexdigest()
    return hash_hex[:20]


def check_user_info(email, password):
    # 建立数据库连接
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    # 查询数据库
    query = "SELECT username, password, salt, userid FROM userInfo WHERE email='%s'" % email
    df = conn.query(query)

    # 检查查询结果是否为空
    if df.empty:
        st.write("No user found with this email.")
        return

    # 获取 password 和 userId
    password_db = df.iloc[0]['password']
    uid = df.iloc[0]['userid']
    salt = df.iloc[0]['salt']
    username = df.iloc[0]['username']
    password_salt = generate_hash(str(password)+str(salt))
    # print("this is login:",salt,password_salt,password_db)


    # 验证密码
    if password_db == password_salt:
        st.write("ok!")
        st.session_state.uid = uid
        st.session_state.username = username
        st.switch_page("pages/home.py")
    else:
        st.write("wrong password!!")



def create_user(username, email, password, salt, userid):
    try:
        # 建立数据库连接
        conn = mysql.connector.connect(
            host='localhost',
            database='streamlitDB',
            user='root',
            password='root'
        )

        if conn.is_connected():
            cursor = conn.cursor()
            # 生成 SQL 插入查询
            query = """
                INSERT INTO userInfo (username, email, password, salt, userid)
                VALUES (%s, %s, %s, %s, %s)
            """
            # 执行查询并提交更改
            cursor.execute(query, (username, email, password, salt, userid))
            conn.commit()
            print(st.session_state.uid)
            st.write("Registered successfully！")

    except Error as e:
        # st.write(f"Error: {e}")
        st.write("Already registered!")
        time.sleep(3)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



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
        # 使用st.dataframe来创建可滑动的数据框
        st.dataframe(df, width=800, height=440, hide_index=True)
        # 打印查询结果进行调试



def add_result(item_id,item_name, uploader, score):
    try:
        # 建立数据库连接
        conn = mysql.connector.connect(
            host='localhost',
            database='streamlitDB',
            user='root',
            password='root'
        )

        if conn.is_connected():
            cursor = conn.cursor()
            # 生成 SQL 插入查询
            query = """
                INSERT INTO result (item_id, item_name, uploader, score)
                VALUES (%s, %s, %s, %s)
            """
            # 执行查询并提交更改
            cursor.execute(query, (item_id, item_name, uploader, score))
            conn.commit()
            st.write("提交成功！")

    except Error as e:
        st.write(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

