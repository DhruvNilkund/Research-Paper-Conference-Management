import streamlit as st
import pandas as pd

if st.session_state["logged_in"]==False:
    st.title("Please Login")
else:
    connection = st.session_state["connection"]

    # Function to add a conference to the database
    def add_conference(conference_id, conference_name, location, website, start_date, end_date, college_id):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO conference (conference_id, conference_name, Loaction,website,st_dates,end_date,college_id) VALUES (%s, %s, %s ,%s,%s,%s,%s)", (conference_id, conference_name, location, website, start_date, end_date, college_id))
        connection.commit()
        cursor.close()

    st.title("Conference Page")

    #Function to update conference
    def update_conference(conference_id, new_conference_name, new_location, new_website, new_start_date, new_end_date, new_college_id):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE conference SET conference_name = %s, Loaction = %s, website = %s, st_dates = %s, end_date = %s, college_id = %s WHERE conference_id = %s",
            (new_conference_name, new_location, new_website, new_start_date, new_end_date, new_college_id, conference_id)
        )
        connection.commit()
        cursor.close()

    #Function to delete conference
    def delete_conference(conference_id):
        cursor = connection.cursor()
        cursor.execute(
            "delete from  conference WHERE conference_id = %s",
            (conference_id,)
        )
        connection.commit()
        cursor.close()
    
    def conference_visitors(conferenceID,t, connection):
        try:
            cursor = connection.cursor()
            sql_query = "SELECT COUNT(*) FROM conference WHERE conference_id = %s"
            cursor.execute(sql_query, (conferenceID,))
            result = cursor.fetchone()[0]
            conference_exists = result > 0
            if (conference_exists==True):
                cursor.execute("select conference_visitors(%s)",(conferenceID,))
                result = cursor.fetchone()[0]
                cursor.close()
                t=1
            else:
                t=0
                result = "Conference ID does not exist"
            return result,t
        except Exception as e:
            return None,t

    # Add Conference
    st.subheader("Add Conference Over Here")
    conference_id = st.text_input("Conference ID (int)", key="conference_id", placeholder="int")
    conference_name = st.text_input("Conference Name (varchar)", key="conference_name", placeholder="varchar")
    location = st.text_input("Location (varchar)", key="location", placeholder="varchar")
    website = st.text_input("Website (varchar)", key="website", placeholder="varchar")
    start_date = st.date_input("Start Date", key="start_date")
    end_date = st.date_input("End Date", key="end_date")
    college_id = st.text_input("College ID (int)", key="college_id", placeholder="int")

    if st.button("Add Conference"):
        if conference_id and conference_name and location and website and start_date and end_date and college_id:
            # Insert the conference into the MySQL database
            add_conference(int(conference_id), conference_name, location, website, start_date, end_date, int(college_id))
            st.success("Conference added successfully!")

    if st.button("Update Conference"):
        if conference_id and conference_name and location and website and start_date and end_date and college_id:
            # Update the conference record in the MySQL database
            update_conference(int(conference_id), conference_name, location, website, start_date, end_date, int(college_id))
            st.success("Conference record updated successfully!")

    if st.button("Delete Conference"):
        if conference_id:
            print(conference_id)
            # delete the conference record in the MySQL database
            delete_conference(int(conference_id))
            st.success("Conference record deleted successfully!")
    # Fetch Conferences
    def fetch_conferences(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM conference")  # Assuming your table is named "conference"
        conference_data = cursor.fetchall()
        cursor.close()
        return conference_data

    conference_data = fetch_conferences(st.session_state["connection"])

    if conference_data:
        # Get the column names from the table
        columns1 = ["Conference ID", "Conference Name", "Location", "Website", "Start Date", "End Date", "College ID"]
        st.subheader("Add your Filters Here")
        # Create dynamic search bars for each column
        search_terms = {}
        for column in columns1:
            search_terms[column] = st.text_input(f"Search by {column}", key=column)

        # Filter data based on search input
        filtered_data = conference_data
        for column, search_term in search_terms.items():
            if search_term:
                filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

        # If all search bars are empty, display all rows
        if all(not search_term for search_term in search_terms.values()):
            filtered_data = conference_data
        st.subheader("The table for all conferences")
        # Display the filtered data in a table
        df=pd.DataFrame(filtered_data,columns=(columns1))
        st.table(df)
        
        conference_id = st.number_input("Enter Conference ID:", min_value=1, step=1)

        if st.button("Calculate Visitors"):
            if conference_id:
                # Call the conference_visitors function and display the result
                t=0
                result,t = conference_visitors(conference_id,t, connection)
                if result is not None and t==1:
                    st.success(f"Total visitors for Conference {conference_id}: {result}")
                elif t==0:
                    st.success(f"{result}")
                else:
                    st.warning("Conference ID ")
            else:
                st.warning("Please enter a valid Conference ID.")
    else:
        st.write("No conferences found.")

