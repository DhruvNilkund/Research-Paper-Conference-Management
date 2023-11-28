import streamlit as st
import mysql.connector
from mysql.connector import Error
import bcrypt

st.session_state["logged_in"]=False
# Create a connection to the MySQL database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='rpms'
        )
    except Error as e:
        st.error(f"Error: {e}")
    return connection

# Create a table for user information (you may need to adapt this to your specific needs)
def create_users_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            type ENUM("ADMIN", "STUDENT", "REVIEWER", "VIEWER")
        )
    """)
    connection.commit()
    cursor.close()

# Function to register a new user
def register_user(username, password,email ,type, connection):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password,email,type) VALUES (%s, %s,%s,%s)", (username, password_hash,email,type))
    connection.commit()
    cursor.close()
    

def get_user_type(username, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT type FROM users WHERE USERNAME = %s", (username,))
    user_type = cursor.fetchone()
    cursor.close()
    print(user_type[0])
    return user_type[0] if user_type else None

# Function to check if a user with the given credentials exists
# Function to check if a user with the given credentials exists
def is_valid_user(username, password, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()  # Fetch the result
    user_type = get_user_type(username,connection)
    st.session_state["type"]= user_type
    if result:
        stored_password = result[0]
        cursor.close()  # Close the cursor here
        return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    else:
        cursor.close()  # Close the cursor if no result is found
        return False


# Streamlit app
def main():
    st.title("Login and Registration App")
    
    # Create a connection to the database and users table
    connection = create_connection()
    if connection is not None:
        print("Connected to mysql")
        st.session_state["connection"]=connection
    if connection is not None:
        create_users_table(connection)

    st.subheader("Register")
    new_username = st.text_input("Enter a new username:", key="register_username")
    new_password = st.text_input("Enter a new password:", type="password", key="register_password")
    new_email = st.text_input("Enter your email id :",key="register_email" )
    new_type = st.selectbox("User Type", ["ADMIN", "STUDENT", "REVIEWER", "VIEWER"])


    if st.button("Register"):
        if new_username and new_password:
            register_user(new_username, new_password, new_email,new_type,connection)
            st.success("Registration successful! You can now log in.")

    st.subheader("Login")
    username = st.text_input("Enter your username:", key="login_username")
    password = st.text_input("Enter your password:", type="password", key="login_password")

    if st.button("Login"):
        if is_valid_user(username, password,connection):
            st.session_state["logged_in"]=True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")
    st.sidebar.header("Navigation")
    st.sidebar.success("Select a page above.")


if __name__ == '__main__':
    main()
