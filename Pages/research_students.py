import streamlit as st
import pandas as pd

if st.session_state["logged_in"]==False:
    st.title("Please Login")
else:
    connection = st.session_state["connection"]

    # Function to add a student to the database
    def add_student(student_id, student_name, mobile, emailid, college_id):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO student (student_id, student_name, mobile, emailid, college_id) VALUES (%s, %s, %s, %s, %s)",
                    (student_id, student_name, mobile, emailid, college_id))
        connection.commit()
        cursor.close()

    def update_student(student_id, student_name, mobile, emailid, college_id):
        cursor = connection.cursor()
        cursor.execute("UPDATE student SET student_name= %s, mobile = %s, emailid = %s, college_id= %s where student_id = %s",
                    (student_name, mobile, emailid, college_id,student_id))
        connection.commit()
        cursor.close()

    def delete_student(student_id):
        cursor = connection.cursor()
        cursor.execute("DELETE from  student where  student_id = %s",
                    (student_id,))
        connection.commit()
        cursor.close()
       
    st.title("Students Page")

    if st.session_state["type"]=="ADMIN":
        # Add Student
        st.subheader("Add Student Over Here")
        student_id = st.text_input("Student ID (int)", key="student_id", placeholder="int")
        student_name = st.text_input("Student Name (varchar)", key="student_name", placeholder="varchar")
        mobile = st.text_input("Mobile (varchar)", key="mobile", placeholder="varchar")
        emailid = st.text_input("Email ID (varchar)", key="emailid", placeholder="varchar")
        college_id = st.text_input("College ID (int)", key="college_id", placeholder="int")

        if st.button("Add Student"):
            if student_id and student_name and mobile and emailid and college_id:
                # Insert the student into the MySQL database
                add_student(int(student_id), student_name, mobile, emailid, int(college_id))
                st.success("Student added successfully!")

        if st.button("Update Student"):
            if student_id and student_name and mobile and emailid and college_id:
                # Update the student into the MySQL database
                update_student(int(student_id), student_name, mobile, emailid, int(college_id))
                st.success("Student updated successfully!")
                
        if st.button("Delete Student"):
            if student_id:
                # Delete the student into the MySQL database
                delete_student(int(student_id))
                st.success("Student deleted successfully!")

    # Fetch Students
    def fetch_students(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student")  # Assuming your table is named "student"
        student_data = cursor.fetchall()
        cursor.close()
        return student_data

    student_data = fetch_students(st.session_state["connection"])

    if student_data:
        # Get the column names from the table
        columns1 = ["Student ID", "Student Name", "Mobile", "Email ID", "College ID"]

        # Create dynamic search bars for each column
        search_terms = {}
        for column in columns1:
            search_terms[column] = st.text_input(f"Search by {column}", key=column)

        # Filter data based on search input
        filtered_data = student_data
        for column, search_term in search_terms.items():
            if search_term:
                filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

        # If all search bars are empty, display all rows
        if all(not search_term for search_term in search_terms.values()):
            filtered_data = student_data

        # Display the filtered data in a table
        df=pd.DataFrame(filtered_data,columns=(columns1))
        st.table(df)
    else:
        st.write("No students found.")
