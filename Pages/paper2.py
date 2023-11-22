import streamlit as st
import mysql.connector
import os
from io import BytesIO
import base64
import fitz
from PyPDF2 import PdfReader
from pdfreader import SimplePDFViewer
import binascii
import webbrowser
import pandas as pd

if st.session_state["logged_in"]==False:
    st.title("Please Login")
# Main Streamlit app
else:
    st.title("Research Papers")

    # Function to fetch research papers from the database
    def fetch_research_papers(connection):
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT research_paper_id, research_paper_name, journal, time_of_release, research_paper, conference_id FROM research_paper")

            papers = cursor.fetchall()
            return papers

        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()

    # # Function to display PDF content using PyPDF2
    # def display_pdf(pdf_content):
    #     st.set_option('deprecation.showfileUploaderEncoding', False)

    #     with st.spinner('Loading PDF...'):
    #         pdf_file = BytesIO(pdf_content)
    #         st.write(pdf_file.read())

    # def fetch_pdf_blob(research_paper_id,connection):
    #     try:
    #         cursor = connection.cursor()
            
    #         cursor.execute("SELECT research_paper FROM research_paper WHERE research_paper_id = %s", (research_paper_id,))
    #         pdf_blob = cursor.fetchone()[0]
            
    #         return pdf_blob

    #     except Exception as e:
    #         st.error(f"Error: {e}")
    #     finally:
    #         cursor.close()

    # def read_and_display_pdf(research_paper_id):
    #     pdf_blob = fetch_pdf_blob(research_paper_id)
    #     if pdf_blob is not None:
    #         pdf_document = fitz.open("pdf", pdf_blob)
    #         st.image(pdf_document[0].convert_to_page().get_pixmap().get_png_data(), use_container_width=True)
    #     else:
    #         st.error("PDF not found in the database.")

    def write_file(data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)

        # Read the text file
        with open(f'C:/Users/User/Desktop/DBMS/multipage/{filename}', 'rb') as file:
            pdf_data = file.read()

        # Remove line breaks and any leading/trailing spaces
        # pdf_data = pdf_data.replace('\n', '').strip()
        bst = bin(int(binascii.hexlify(pdf_data), 16))
        n = int(bst, 2)
        binary_data = binascii.unhexlify('%x' % n) 
        # Convert the hexadecimal string to binary
        # binary_data = binascii.unhexlify(pdf_data)

        # Save the binary data to a PDF file
        with open(f'C:/Users/User/Desktop/DBMS/multipage/{filename}.pdf', 'wb') as pdf_file:
            pdf_file.write(binary_data)

        webbrowser.open_new(f"C:/Users/User/Desktop/DBMS/multipage/{filename}.pdf")


    def readBLOB(research_paper_id, pdffile,connection):
        print("Reading BLOB data from python_employee table")

        try:
            cursor = connection.cursor()
            sql_fetch_blob_query = """SELECT * from research_paper where research_paper_id = %s"""

            cursor.execute(sql_fetch_blob_query, (research_paper_id,))
            record = cursor.fetchall()
            for row in record:
                print("Id = ", row[0], )
                print("Name = ", row[1])
                print(type(row[4]))
                file =row[4]
                print("Storing pdf on disk \n")
                write_file(file, pdffile)

        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))

        finally:
            if connection.is_connected():
                cursor.close()
    
    def research_track(track_id):
        cursor=connection.cursor()
        cursor.callproc("research_track", (track_id,))
        results = cursor.stored_results()
        results=list(results)
        if results:
            result_set = results[0]
            return result_set.fetchall()
        cursor.close()
        return []

    def main(connection):
        i=100
        papers = fetch_research_papers(connection)
        st.subheader("Search Research Paper by track ID")
        track_id = st.text_input("Enter Track ID (int)", key="track_id", placeholder="int")

        if st.button("Search Research Papers"):
            if track_id:
                track_id = int(track_id)
                research_results = research_track(track_id)

                if research_results:
                    columns = ["ID", "Paper Name", "Journal", "Time of Release", "Conference Name"]
                    # df = pd.DataFrame(research_results, columns=columns)
                    k=0
                    for j in research_results:
                        paper_id = j[0]
                        paper_name = j[1]
                        journal =j[2]
                        time = j[3]
                        con_name = j[4]
                        print(paper_id,con_name)
                        table_data=[
                        {
                            "Paper ID":{paper_id},
                            "Paper Name": {paper_name},
                            "Journal": {journal},
                            "Time of Release": {time},
                            "Conference Name:":{con_name}
                        }]
                        st.table(table_data)
                        if st.button("View File",key=k):
                                readBLOB(int(paper[0]),f"{paper[1]}.txt",connection)
                        k+=1
                else:
                        st.write("No research papers found for the specified track.")
        
        st.subheader("All Research Papers")
        for paper in papers:
            table_data=[
                {
                    "Paper ID":{paper[0]},
                    "Paper Name": {paper[1]},
                    "Journal": {paper[2]},
                    "Time of Release": {paper[3]},
                    "Conference ID:":{paper[5]}
                }]
            st.table(table_data)

            if st.button("View File",key=i):
                    readBLOB(int(paper[0]),f"{paper[1]}.txt",connection)
            i+=1
        



    if __name__=="__main__":
        connection = st.session_state["connection"]
        main(connection)
        st.write("End of Research Papers")