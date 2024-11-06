import streamlit as st
import zipfile
import io

def download():
    framework = "mydocs/SkillsFramework_Sample.xlsx"
    sample_jd = "mydocs/Sample Intern JD.docx"
    resume1 = "mydocs/Sample Accountant Resume.pdf"
    resume2 = "mydocs/Sample Machine Learning Resume.pdf"
    resume3 = "mydocs/Sample Marketing Resume.docx"
    resume4 = "mydocs/Sample Software Engineering Resume.pdf"

    st.header("Download Sample Files Here")
    st.write("Or feel free to use your own 😉")
    st.divider()
    st.subheader("Sample Software Engineering JD")
    with open(sample_jd, "rb") as file:
        docx_bytes = file.read()
        st.download_button(
            label="Download Sample JD Doc",
            data=docx_bytes,
            file_name="your_file.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    st.divider()
    st.subheader("Skills Future Framework")
    with open(framework, "rb") as file:
        file_bytes = file.read()
        st.download_button(
            label="Download Sample SkillsFuture Framework Excel",
            data=file_bytes,
            file_name="SkillsFutureFramework_Sample.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"   
        )

    st.divider()
    st.subheader("4 Sample Resumes")
    st.write("Background of the sample resumes (docx & pdf mix):")
    st.markdown("""
    <ul>
        <li><b>Alice Tan Thia Koon: </b>Software Engineer</li>
        <li><b>Yunlong Jiao: </b>Machine Learning Engineer</li>
        <li><b>Caleb Tan Jun Jie: </b>Marketing Resume</li>
        <li><b>Peter Barker: </b>Accountant</li>
    </ul>
    """, unsafe_allow_html=True)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.write(resume1, "Sample Accountant Resume.pdf")
        zip_file.write(resume2, "Sample Machine Learning Resume.pdf")
        zip_file.write(resume3, "Sample Marketing Resume.docx")
        zip_file.write(resume4, "Sample Software Engineering Resume.pdf")

    zip_buffer.seek(0)

    st.download_button(
        label="Download All Resumes",
        data=zip_buffer,
        file_name="all_sample_resume.zip",
        mime="application/zip"
    )