import streamlit as st
import pandas as pd

connection = st.session_state["connection"]

if st.session_state["logged_in"]==False:
    st.title("Please Login first")
else:
    # Function to add an attendee to the database
    def add_attendee(conference_id, visit_id, visit_name, attendee_type):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO attendee (conference_id, visit_id, Visit_name, attendee_type) VALUES (%s, %s, %s, %s)",
                    (conference_id, visit_id, visit_name, attendee_type))
        connection.commit()
        cursor.close()
        
    def update_attendee(visit_id, visit_name, attendee_type):
        cursor = connection.cursor()
        cursor.execute("UPDATE attendee SET visit_name = %s,attendee_type = %s where visit_id = %s",
                    (visit_name, attendee_type,visit_id))
        connection.commit()
        cursor.close()

    def delete_attendee(visit_id):
        cursor = connection.cursor()
        cursor.execute("delete from attendee  where visit_id = %s",
                    (visit_id,))
        connection.commit()
        cursor.close()

    st.title("Attendee Page")

    if st.session_state["type"]=="ADMIN":
        # Add Attendee
        st.subheader("Add Attendee Over Here")
        conference_id = st.text_input("Conference ID (int)", key="conference_id", placeholder="int")
        # attendee_id = st.text_input("Attendee ID (int)", key="attendee_id", placeholder="int")
        visit_id = st.text_input("Visit ID (int)", key="visit_id", placeholder="int")
        visit_name = st.text_input("Visit Name (varchar)", key="visit_name", placeholder="varchar")
        attendee_type = st.selectbox("Attendee Type", ["STU", "TEACH"])

        if st.button("Add Attendee"):
            if conference_id  and visit_id and visit_name and attendee_type:
                # Insert the attendee into the MySQL database
                add_attendee(int(conference_id), int(visit_id), visit_name, attendee_type)
                st.success("Attendee added successfully!")

        if st.button("Update Attendee"):
            if visit_id and visit_name and attendee_type:
                # Insert the attendee into the MySQL database
                update_attendee(int(visit_id), visit_name, attendee_type)
                st.success("Attendee updated successfully!")
                
        if st.button("Delete Attendee"):
            if  visit_id :
                # Insert the attendee into the MySQL database
                delete_attendee(int(visit_id))
                st.success("Attendee deleted successfully!")
                
    # Fetch Attendees
    def fetch_attendees(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM attendee")  # Assuming your table is named "attendee"
        attendee_data = cursor.fetchall()
        cursor.close()
        return attendee_data

    attendee_data = fetch_attendees(st.session_state["connection"])

    if attendee_data:
        # Get the column names from the table
        columns1 = ["Conference ID", "Visit ID", "Visit Name", "Attendee Type"]

        # Create dynamic search bars for each column
        search_terms = {}
        for column in columns1:
            search_terms[column] = st.text_input(f"Search by {column}", key=column)

        # Filter data based on search input
        filtered_data = attendee_data
        for column, search_term in search_terms.items():
            if search_term:
                filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

        # If all search bars are empty, display all rows
        if all(not search_term for search_term in search_terms.values()):
            filtered_data = attendee_data

        # Display the filtered data in a table
        df=pd.DataFrame(filtered_data,columns=(columns1))
        st.table(df)
    else:
        st.write("No attendees found.")

