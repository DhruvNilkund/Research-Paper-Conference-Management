import streamlit as st
import mysql.connector
from io import BytesIO

if st.session_state["logged_in"]==False:
    st.title("Please Login")
elif st.session_state["type"]=="REVIEWER" or st.session_state["type"]=="VIEWER":
    st.title("You are Not authorized for this page")
else:
    # Database connection configuration
    connection = st.session_state["connection"]

    # Function to check if the student is authorized to upload
    def is_authorized(student_id, research_paper_id):
        try:
        
            cursor = connection.cursor()

            cursor.execute("INSERT INTO  research_student (student_id,research_paper_id) VALUES (%s,%s)", (student_id, research_paper_id))
            #count = cursor.fetchone()[0]
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
        return True

    # Function to upload a research paper as BLOB
    def upload_paper(student_id, research_paper_id, research_paper_file,name,journal,conferenceid,trackid):
        try:
            cursor = connection.cursor()

            # if is_authorized(student_id, research_paper_id):
            if True:#:
                # Read the uploaded PDF file and convert it to bytes
                pdf_bytes = research_paper_file.read()

                # Insert the research paper as BLOB into the database
                cursor.execute("INSERT INTO research_paper (research_paper_id, research_paper_name, journal, time_of_release, research_paper, conference_id,track_id) VALUES (%s, %s, %s, NOW(), %s, %s,%s)",
                            (research_paper_id, f'{name}', f'{journal}', pdf_bytes, conferenceid,trackid))
                is_authorized(student_id, research_paper_id)
                connection.commit()
                st.success(f"Research paper uploaded successfully.")
            else:
                st.error("You are not authorized to upload this paper.")

        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()

    # Main Streamlit app
    st.title("Research Paper Upload Page")

    # Student input (you may use a login system to identify the student)
    student_id = st.number_input("Student ID")

    # Research Paper input
    research_paper_id = st.number_input("Research Paper ID")
    research_paper_file = st.file_uploader("Upload Research Paper (PDF)", type=['pdf'])
    journal = st.text_input("Enter journal name here")
    conferenceid = st.number_input("Conference id in which research paper produced")
    trackid = st.number_input("Track ID")

    if st.button("Upload Research Paper"):
        if research_paper_file is not None:
            upload_paper(student_id, research_paper_id, research_paper_file,research_paper_file.name,journal,conferenceid,trackid)

    st.write("End of Research Paper Upload")
