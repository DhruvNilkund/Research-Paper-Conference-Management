import streamlit as st
import pandas as pd 

if st.session_state["logged_in"]==False:
    st.title("Please Login")
else:
    connection = st.session_state["connection"]

    # Function to add a college to the database
    def add_college(college_id, college_name, dean, col_location, emailID, phone):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO college (college_id, college_name, dean, col_location, emailID, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                    (college_id, college_name, dean, col_location, emailID, phone))
        connection.commit()
        cursor.close()

    st.title("Colleges Page")

    def update_college(college_id, college_name, dean, col_location, emailID, phone):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE college SET college_name=%s, dean=%s, col_location=%s, emailID=%s, phone=%s WHERE college_id = %s",
            (college_name, dean, col_location, emailID, phone,college_id)
        )
        connection.commit()
        cursor.close()

    def delete_college(college_id):
        cursor = connection.cursor()
        cursor.execute(
            "delete from  college WHERE college_id = %s",
            (college_id,)
        )
        connection.commit()
        cursor.close()
        
    # Add College
    if st.session_state["type"]=="ADMIN":
        st.subheader("Add College Over Here")
        college_id = st.text_input("College ID (int)", key="college_id", placeholder="int")
        college_name = st.text_input("College Name (varchar)", key="college_name", placeholder="varchar")
        dean = st.text_input("Dean (varchar)", key="dean", placeholder="varchar")
        col_location = st.text_input("College Location (tinytext)", key="col_location", placeholder="tinytext")
        emailID = st.text_input("Email ID (varchar)", key="emailID", placeholder="varchar")
        phone = st.text_input("Phone (varchar)", key="phone", placeholder="varchar")

        if st.button("Add College"):
            if college_id and college_name and dean and col_location and emailID and phone:
                # Insert the college into the MySQL database
                add_college(int(college_id), college_name, dean, col_location, emailID, phone)
                st.success("College added successfully!")
        
        if st.button("Update College"):
            if college_id and college_name and dean and col_location and emailID and phone:
                # Insert the college into the MySQL database
                update_college(int(college_id), college_name, dean, col_location, emailID, phone)
                st.success("College updated successfully!")
                
        if st.button("Delete College"):
            if college_id:
                # Insert the college into the MySQL database
                delete_college(int(college_id))
                st.success("College deleted successfully!")
                
                
    # Fetch Colleges
    def fetch_colleges(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM college")  # Assuming your table is named "college"
        college_data = cursor.fetchall()
        cursor.close()
        return college_data
    
    def get_college_research_papers(college_id):
        cursor=connection.cursor()
        cursor.callproc("get_college_research_papers", (college_id,))
        results = cursor.stored_results()
        results=list(results)
        if results:
            result_set = results[0]
            return result_set.fetchall()
        cursor.close()
        return []
    
    college_data = fetch_colleges(st.session_state["connection"])

    if college_data:
        # Get the column names from the table
        columns1 = ["College ID", "College Name", "Dean", "College Location", "Email ID", "Phone"]

        # Create dynamic search bars for each column
        search_terms = {}
        for column in columns1:
            search_terms[column] = st.text_input(f"Search by {column}", key=column)

        # Filter data based on search input
        filtered_data = college_data
        for column, search_term in search_terms.items():
            if search_term:
                filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

        # If all search bars are empty, display all rows
        if all(not search_term for search_term in search_terms.values()):
            filtered_data = college_data

        # Display the filtered data in a table
        df=pd.DataFrame(filtered_data,columns=(columns1))
        st.table(df)

        collegeid = st.text_input("Enter College ID (int)", key="track_id", placeholder="int")

        if st.button("Search Research Papers"):
            if collegeid:
                collegeid = int(collegeid)
                research_results = get_college_research_papers(collegeid)

                if research_results:
                    columns = ["research_paper_id", "research_paper_name", "student_name","college_id"]
                    df = pd.DataFrame(research_results, columns=columns)
                    st.table(df)
                else:
                    st.write("No research papers found for the specified collegeid.")
        
    else:
        st.write("No colleges found.")

