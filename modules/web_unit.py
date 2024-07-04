import streamlit as st
import streamlit as st
import mysql.connector
from mysql.connector import Error


def check_user_info(email, password):
    # 建立数据库连接
    conn = st.connection(
        "local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    # 查询数据库
    query = "SELECT password, userid, username FROM userInfo WHERE email='%s'" % email
    df = conn.query(query)

    # 检查查询结果是否为空
    if df.empty:
        st.write("No user found with this email.")
        return

    # 获取 password 和 userId
    password_db = df.iloc[0]['password']
    uid = df.iloc[0]['userid']
    username = df.iloc[0]['username']

    # 验证密码
    if password_db == password:
        st.write("ok!")
        st.session_state.uid = uid
        st.session_state.username = username
        st.switch_page("app.py")
    else:
        st.write("wrong password!!")



def create_user(username, email, password, userid):
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
                INSERT INTO userInfo (username, email, password, userid)
                VALUES (%s, %s, %s, %s)
            """
            # 执行查询并提交更改
            cursor.execute(query, (username, email, password, userid))
            conn.commit()
            st.write("用户注册成功！")

    except Error as e:
        st.write(f"Error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def check_uploads():
    conn = st.connection(
        name="local_db",
        type="sql",
        url="mysql://root:root@localhost:3306/streamlitDB"
    )

    query = "SELECT item_id, item_name, uploader, score FROM result WHERE 1"
    df = conn.query(query)

    # 打印查询结果进行调试
    st.write("Query executed successfully")
    st.write(df)


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
