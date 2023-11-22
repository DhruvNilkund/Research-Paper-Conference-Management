import streamlit as st
import pandas as pd
    
if st.session_state["logged_in"]==False:
    st.title("Please Login")
else:
    connection = st.session_state["connection"]

    def add_reviewer(reviewer_id, reviewer_name, affiliation, mobile, emailid):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO reviewer (reviewer_id, reviewer_name, affiliation, Mobile, emailid) VALUES (%s, %s, %s, %s, %s)",
                    (reviewer_id, reviewer_name, affiliation, mobile, emailid))
        connection.commit()
        cursor.close()

    def update_reviewer(reviewer_id, reviewer_name, affiliation, mobile, emailid):
        cursor = connection.cursor()
        cursor.execute("UPDATE reviewer set reviewer_name= %s,affiliation= %s, mobile = %s,emailid = %s where reviewer_id = %s ",
                    (reviewer_name, affiliation, mobile, emailid,reviewer_id))
        connection.commit()
        cursor.close()

    def delete_reviewer(reviewer_id):
        cursor = connection.cursor()
        cursor.execute("delete from reviewer where reviewer_id = %s ",
                    (reviewer_id,))
        connection.commit()
        cursor.close()
             
    st.title("Reviewer Page")

    if st.session_state["type"]=="ADMIN":
        # Add Reviewer
        st.subheader("Add Reviewer Over Here")
        reviewer_id = st.text_input("Reviewer ID (int)", key="reviewer_id", placeholder="int")
        reviewer_name = st.text_input("Reviewer Name (varchar)", key="reviewer_name", placeholder="varchar")
        affiliation = st.text_input("Affiliation (varchar)", key="affiliation", placeholder="varchar")
        mobile = st.text_input("Mobile (char)", key="mobile", placeholder="char")
        emailid = st.text_input("Email ID (varchar)", key="emailid", placeholder="varchar")

        if st.button("Add Reviewer"):
            if reviewer_id and reviewer_name and affiliation and mobile and emailid:
                # Insert the reviewer into the MySQL database
                add_reviewer(int(reviewer_id), reviewer_name, affiliation, mobile, emailid)
                st.success("Reviewer added successfully!")

        if st.button("Update Reviewer"):
            if reviewer_id and reviewer_name and affiliation and mobile and emailid:
                # Update the reviewer into the MySQL database
                update_reviewer(int(reviewer_id), reviewer_name, affiliation, mobile, emailid)
                st.success("Reviewer updated successfully!")

        if st.button("Delete Reviewer"):
            if reviewer_id:
                # Update the reviewer into the MySQL database
                delete_reviewer(int(reviewer_id))
                st.success("Reviewer deleted successfully!")
                      
    # Fetch Reviewers
    def fetch_reviewers(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM reviewer")  # Assuming your table is named "reviewer"
        reviewer_data = cursor.fetchall()
        cursor.close()
        return reviewer_data

    reviewer_data = fetch_reviewers(st.session_state["connection"])

    if reviewer_data:
        # Get the column names from the table
        columns1 = ["Reviewer ID", "Reviewer Name", "Affiliation", "Mobile", "Email ID"]

        # Create dynamic search bars for each column
        search_terms = {}
        for column in columns1:
            search_terms[column] = st.text_input(f"Search by {column}", key=column)

        # Filter data based on search input
        filtered_data = reviewer_data
        for column, search_term in search_terms.items():
            if search_term:
                filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

        # If all search bars are empty, display all rows
        if all(not search_term for search_term in search_terms.values()):
            filtered_data = reviewer_data

        # Display the filtered data in a table
        df=pd.DataFrame(filtered_data,columns=(columns1))
        st.table(df)
    else:
        st.write("No reviewers found.")

