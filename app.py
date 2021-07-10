import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('data.db')
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')



def dropUserTable():
    c.execute('DROP TABLE userstable')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE password ="' + password + '" AND username ="' + username + '"')
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data





def main():
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Home':
        st.subheader("Home Page")
    elif(choice == "Login"):
        st.subheader("Login")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input(
            "Password", type="password")
        if st.sidebar.checkbox("Login/Logout"):
            create_usertable()
            data = login_user(username,password)
            if data:
                data = data[0]
                st.success("Logged In as {}".format(username))
                logged_in_user = data[0]
                if(logged_in_user == "admin"):
                    st.subheader("Welcome to the Admin Portal")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=[
                                            "Username", "Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Invalid Credentials!")
    else:
        st.subheader("SignUp")
        new_user = st.text_input("Username")
        new_password = st.text_input(
            "Password", type="password")

        if st.button("SignUp"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("registered")
            st.info("go to login")

if __name__ == '__main__':
    main()
