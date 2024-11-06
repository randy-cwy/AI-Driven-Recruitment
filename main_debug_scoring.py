import streamlit as st
import json
from helper.utility import check_password
from helper.file_handler import process_job_description_file
from helper.skills_mapping import load_skills_future_framework, llm_assisted_skill_matching, remove_duplicate_skills
from helper.bulk_resume_processor import process_bulk_resumes
from helper.scoring import score_all_candidates, load_json_data
  
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
jd_file = st.file_uploader("Upload a Job Description (.docx, .pdf)", type=["docx", "pdf"])

# Upload the SkillsFuture Framework
framework_file = st.file_uploader("Upload the SkillsFuture Framework (.xlsx)", type=["xlsx"])

# Bulk upload different resumes
resume_files = st.file_uploader("Upload Resumes (.docx, .pdf)", type=["docx", "pdf"], accept_multiple_files=True)

if jd_file and framework_file and resume_files:
    st.write("Files uploaded successfully!")
    
    # Process the job description file
    jd_text, parsed_output = process_job_description_file(jd_file)
    
    # Load the SkillsFuture Framework
    framework_df = load_skills_future_framework(framework_file)
    
    # Use LLM to match job description with relevant skills from framework
    jd_matched_skills = llm_assisted_skill_matching(jd_text, framework_df)

    # Parse JSON string to convert it into a list of dictionaries
    if isinstance(jd_matched_skills, str):
        jd_matched_skills = json.loads(jd_matched_skills)

    jd_matched_skills = remove_duplicate_skills(jd_matched_skills)

    # Display the JD matched skills with proficiency and importance
    st.subheader("Job Description Matched Skills")
    jd_skill_details = [
        {
            "Skill": skill["Skill"],
            "Proficiency Level": skill.get("Proficiency Level", "N/A"),
            "Importance": skill.get("Importance", "N/A")
        }
        for skill in jd_matched_skills
    ]
    st.write(jd_skill_details)
    
    st.write("Processing resumes...")
    
    # Process all resumes and get results
    candidate_results = process_bulk_resumes(resume_files, framework_df)
    
    # Display each candidate's skills with proficiency
    for candidate_name, candidate_info in candidate_results.items():
        st.subheader(f"Candidate: {candidate_name}")
        candidate_skill_details = [
            {
                "Skill": skill["Skill"],
                "Proficiency Level": skill.get("Proficiency Level", "N/A")
            }
            for skill in candidate_info["Skills"]
        ]
        st.write(candidate_skill_details)

    # Calculate and display candidate scores
    st.subheader("Candidate Scores")
    candidate_scores = score_all_candidates(candidate_results, jd_matched_skills)
    
    for candidate_name, score in candidate_scores.items():
        st.write(f"{candidate_name}: {score:.2f}%")
