import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
import json
import zipfile
import io
from about import about_page
from methodology import methodology_page
from download import download
from helper.utility import check_password
from helper.file_handler import process_job_description_file
from helper.skills_mapping import load_skills_future_framework, llm_assisted_skill_matching, remove_duplicate_skills
from helper.bulk_resume_processor import process_bulk_resumes
from helper.scoring import score_all_candidates
from helper.assessment_generator import generate_assessment_with_answers, create_candidate_docs, create_answer_key_doc
  
# region <--------- Streamlit Page Configuration --------->

st.set_page_config(layout="centered", page_title="Candidate Scoring App", initial_sidebar_state="collapsed")

# Do not continue if check_password is not True.  
if not check_password():
    st.stop()

# Custom CSS having issues with navbar, so I decided to remove custom button css.

# endregion <--------- Streamlit Page Configuration --------->

# Page Selector with st.selectbox
pages = ["Home", "Sample Files", "About", "Methodology"]

styles = {
    "nav": {
        "background-color": "#004B87",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "#FFFFFF",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(pages, styles=styles)

if page == "About":
    # Call the About Page Function
    about_page()
elif page == "Methodology":
    methodology_page()
elif page == "Sample Files":
    download()
elif page == "Home":
    # Main page content
    st.title("LLM-Powered Job Description Parsing and Candidate Scoring")
    with st.expander("IMPORTANT NOTICE"):
        st.write("""
            This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

            Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

            Always consult with qualified professionals for accurate and personalized advice.
        """)

    # Step 1: Upload necessary files
    st.subheader("Step 1: Upload Files")

    # Upload a job description file
    jd_file = st.file_uploader("Upload a Job Description (.docx, .pdf)", type=["docx", "pdf"])

    # Upload the SkillsFuture Framework
    framework_file = st.file_uploader("Upload the SkillsFuture Framework (.xlsx)", type=["xlsx"])

    # Bulk upload different resumes
    resume_files = st.file_uploader("Upload Resumes (.docx, .pdf)", type=["docx", "pdf"], accept_multiple_files=True)

    # Check if all files are uploaded
    if jd_file and framework_file and resume_files:
        st.success("Files uploaded successfully!")

        # Step 2: Prompt the user for the number of top candidates
        st.subheader("Step 2: Select Number of Top Candidates")
        top_n = st.number_input("Enter the number of top candidates to display", min_value=1, max_value=len(resume_files))

        # Step 3: Process and store results in a DataFrame or recompute if requested
        button_label = "Recompute Score" if "candidate_df" in st.session_state else "Process Candidate Resumes"

        if st.button(button_label):
            # Clear or reset any session state variables to avoid display of old data
            st.session_state.pop("candidate_df", None)
            st.session_state.pop("jd_matched_skills", None)
            st.session_state.pop("top_n_candidates", None)
            st.session_state.pop("assessment_generated", None)
            st.session_state.pop("candidate_results", None)  # Clear old candidate_results

            # Process Job Description and Skills Framework
            with st.spinner("Loading..."):
                jd_text, _ = process_job_description_file(jd_file)
                framework_df = load_skills_future_framework(framework_file)
                jd_matched_skills = llm_assisted_skill_matching(jd_text, framework_df)

                # Remove duplicates and save jd_matched_skills in session state
                jd_matched_skills = remove_duplicate_skills(json.loads(jd_matched_skills))
                st.session_state["jd_matched_skills"] = jd_matched_skills

                # Process resumes with progress bar
                progress_bar = st.progress(0)
                total_files = len(resume_files)

                candidate_results = {}

                # Process resumes with progress bar
                for index, resume_file in enumerate(resume_files):
                    # Process each resume
                    result = process_bulk_resumes([resume_file], framework_df)
                    candidate_results.update(result)
                    
                    # Update progress bar
                    progress_bar.progress((index + 1) / total_files)

                # Clear the progress bar once done
                progress_bar.empty()
                                
                # Store candidate results in session state
                st.session_state["candidate_results"] = candidate_results  # <-- Store results here

                # Score candidates and save results
                candidate_scores = score_all_candidates(candidate_results, jd_matched_skills)
                
                # Store the scores in a DataFrame and in session state
                candidate_df = pd.DataFrame(candidate_scores.items(), columns=["Candidate", "Score"])
                candidate_df = candidate_df.sort_values(by="Score", ascending=False).reset_index(drop=True)
                st.session_state["candidate_df"] = candidate_df

        # Step 4: Display Results with Expandable Details
        if "candidate_df" in st.session_state:
            st.subheader(f"Top {top_n} Candidates:")
            
            # Display each candidate's details in an expander
            top_candidates = st.session_state.candidate_df.head(top_n)
            candidate_results = st.session_state["candidate_results"]  # Load candidate skills data
            
            for _, row in top_candidates.iterrows():
                candidate_name = row["Candidate"]
                score = row["Score"]
                
                # Create an expander for each candidate
                with st.expander(f"{candidate_name} - {score:.2f}%"):
                    st.write(f"**Overall Score**: {score:.2f}%")
                    
                    # Fetch this candidate’s detailed info from candidate_results
                    candidate_info = candidate_results.get(candidate_name, {})
                    
                    # Display candidate qualifications if available
                    qualification = candidate_info.get("Qualification", "N/A")
                    st.write(f"**Qualification**: {qualification}")
                    
                    # Display matched skills and their proficiency levels
                    st.write("**Matched Skills:**")
                    skills = candidate_info.get("Skills", [])
                    if skills:
                        for skill in skills:
                            skill_name = skill.get("Skill", "Unknown Skill")
                            proficiency = skill.get("Proficiency Level", "Unknown Proficiency")
                            explanation = skill.get("Explanation", "No explanation provided")
                            
                            # Show each skill with its details in an organized format
                            st.markdown(f"""
                            - **{skill_name}**
                                - **Proficiency Level**: {proficiency}
                                - **Explanation**: {explanation}
                            """)
                    else:
                        st.write("No matched skills found for this candidate.")

            # Generate Assessment Button (reset the generated state if recomputing)
            generate_label = f"Generate {top_n} Assessment Documents"
            if st.button(generate_label, disabled=st.session_state.get("is_generating_assessment", False)):
                # Set the flag to indicate assessment generation is in progress
                st.session_state["is_generating_assessment"] = True
                st.session_state["assessment_generated"] = False

                # Retrieve candidate names from the top N candidates in the session state DataFrame
                top_candidates = st.session_state.candidate_df.head(top_n)
                candidate_names = top_candidates["Candidate"].tolist()
                
                # Generate assessment with progress bar
                with st.spinner("Generating assessment documents..."):
                    assessment_data = generate_assessment_with_answers(st.session_state["jd_matched_skills"])
                    
                    # Progress bar for generating assessment documents
                    assessment_progress_bar = st.progress(0)
                    total_candidates = len(candidate_names)

                    for index, candidate_name in enumerate(candidate_names):
                        create_candidate_docs([candidate_name], assessment_data)
                        
                        # Update progress bar
                        assessment_progress_bar.progress((index + 1) / total_candidates)

                    # Clear the progress bar once done
                    assessment_progress_bar.empty()

                    create_answer_key_doc(assessment_data)
                    
                    # Zip the generated files
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                        for candidate_name in candidate_names:
                            filename = f"{candidate_name.replace(' ', '_')}_Assessment.docx"
                            zip_file.write(filename)
                        zip_file.write("Assessment_Answer_Key.docx")
                    zip_buffer.seek(0)
                    
                    st.session_state["zip_buffer"] = zip_buffer
                    st.session_state["assessment_generated"] = True

                # Reset the loading flag
                st.session_state["is_generating_assessment"] = False

                # Display download button only if assessment is generated
                if st.session_state.get("assessment_generated", False):
                    st.download_button(
                        label="Download Assessment Files",
                        data=st.session_state["zip_buffer"],
                        file_name="Assessments.zip",
                        mime="application/zip"
                    )
