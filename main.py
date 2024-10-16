import streamlit as st
from helper.utility import check_password
from helper.file_handler import process_job_description_file
  
# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

st.title("LLM-Powered Job Description Parsing")

# Upload a job description file
uploaded_file = st.file_uploader("Upload a Job Description (.docx)", type=["docx"])

if uploaded_file:
    st.write("File uploaded successfully!")
    
    # Call the main function to handle the file and LLM parsing
    jd_text, parsed_output = process_job_description_file(uploaded_file)
    
    # Display the parsed output from LLM
    st.write("Parsed Output from LLM:")
    st.write(parsed_output)
