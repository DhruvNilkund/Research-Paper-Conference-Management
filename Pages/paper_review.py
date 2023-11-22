import streamlit as st
import pandas as pd

st.title("Paper Review Page")

connection = st.session_state["connection"]

# Function to add a paper review to the database
def add_paper_review(reviewer_id, paper_id, review_comments, student_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE paper_review set review_comments=%s,timestamp= Now() where reviewer_id = %s and paper_id = %s and student_id = %s", (review_comments,reviewer_id,paper_id,student_id))
    connection.commit()
    cursor.close()

if st.session_state["type"]=="REVIEWER":
    # Add Paper Review
    st.subheader("Add Paper Review Here")
    reviewer_id = st.text_input("Reviewer ID (int)", key="reviewer_id", placeholder="int")
    paper_id = st.text_input("Paper ID (int)", key="paper_id", placeholder="int")
    review_comments = st.text_area("Review Comments", key="review_comments", placeholder="Enter review comments here")
    student_id = st.text_input("Student ID (int)", key="student_id", placeholder="int")

    if st.button("Add Paper Review"):
        if reviewer_id and paper_id and review_comments and student_id:
            # Insert the paper review into the MySQL database
            add_paper_review(int(reviewer_id), int(paper_id), review_comments, int(student_id))
            st.success("Paper Review added successfully!")

# Fetch Paper Reviews
def fetch_paper_reviews(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM paper_review")
    paper_review_data = cursor.fetchall()
    cursor.close()
    return paper_review_data

paper_review_data = fetch_paper_reviews(st.session_state["connection"])

if paper_review_data:
    # Get the column names from the table
    columns1 = ["Reviewer ID", "Paper ID", "Review Comments", "Student ID","Time Stamp"]

    # Create dynamic search bars for each column
    search_terms = {}
    for column in columns1:
        search_terms[column] = st.text_input(f"Search by {column}", key=column)

    # Filter data based on search input
    filtered_data = paper_review_data
    for column, search_term in search_terms.items():
        if search_term:
            filtered_data = [row for row in filtered_data if search_term.lower() in str(row[columns1.index(column)]).lower()]

    # If all search bars are empty, display all rows
    if all(not search_term for search_term in search_terms.values()):
        filtered_data = paper_review_data

    # Display the filtered data in a table
    df = pd.DataFrame(filtered_data, columns=columns1)
    st.table(df)
else:
    st.write("No paper reviews found.")
