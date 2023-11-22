import streamlit as st
import pandas as pd

if st.session_state["logged_in"]==False:
    st.title("Please Login")
else:
    st.title("Track Page")

    connection = st.session_state["connection"]
    def add_track(track_id, track_name):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO track (track_id, track_name) VALUES (%s, %s)", (track_id, track_name))
        connection.commit()
        cursor.close()

    def update_track(track_id, track_name):
        cursor = connection.cursor()
        cursor.execute("UPDATE track SET track_name = %s where track_id = %s", (track_name,track_id))
        connection.commit()
        cursor.close()      

    def delete_track(track_id):
        cursor = connection.cursor()
        cursor.execute("delete from track where track_id = %s", (track_id,))
        connection.commit()
        cursor.close()     
        
    if st.session_state["type"]=="ADMIN":
        st.write("Add Track Over Here")
        track_id = st.text_input("Track ID (int)", key="track_id", placeholder="int")
        track_name = st.text_input("Track Name (varchar)", key="track_name", placeholder="varchar")

        if st.button("Add"):
                    if track_id and track_name:
                        # Insert the track into the MySQL database
                        add_track(int(track_id), track_name)
                        st.success("Track added successfully!")    
        if st.button("Update"):
                    if track_id and track_name:
                        # Insert the track into the MySQL database
                        update_track( int(track_id), track_name)
                        st.success("Track updated successfully!")
        # if st.button("Delete"):
        #             if conference_id and track_id:
        #                 # Insert the track into the MySQL database
        #                 add_track(int(conference_id), int(track_id))
        #                 st.success("Track added successfully!")

    def fetch_tracks(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT track_id,track_name FROM track")  # Assuming your table is named "track"
        track_data = cursor.fetchall()
        cursor.close()
        return track_data

    track_data = fetch_tracks(st.session_state["connection"])

    if track_data:
        # Get the column names from the table
        columns1 = ["Track ID", "Track Name"]

        # Create dynamic search bars for each column
        search_terms = {}
        for column in columns1:
            search_terms[column] = st.text_input(f"Search by {column}", key=column)

        # Filter data based on search input
        filtered_data = track_data
        for column, search_term in search_terms.items():
            if search_term:
                filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

        # If all search bars are empty, display all rows
        if all(not search_term for search_term in search_terms.values()):
            filtered_data = track_data

        # Display the filtered data in a table
        df=pd.DataFrame(filtered_data,columns=(columns1))
        st.table(df)
    else:
        st.write("No tracks found.")

