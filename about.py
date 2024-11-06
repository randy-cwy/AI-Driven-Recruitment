import streamlit as st

def about_page():
    # Add CSS for styling
    st.markdown("""
        <style>
        .about-header {
            font-size: 26px;
            color: #004B87;
            margin-bottom: 10px;
        }
        .about-subheader {
            font-size: 20px;
            margin-bottom: 10px;
        }
        .about-paragraph {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        ul.about-list {
            list-style-type: disc;
            padding-left: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Content
    st.title("About This Project")
    st.markdown('<div class="about-header">Project Scope</div>', unsafe_allow_html=True)
    st.markdown('<p class="about-paragraph">This project is an AI-powered job description parsing and candidate scoring application. It leverages large language models (LLMs) to match job responsibilities with relevant skills, assess candidates based on their resumes, and generate customized assessments.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-header">Objectives/Use Case</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="about-list">
        <li><b>Automate Candidate Assessment:</b> Reduce manual effort in scoring candidates by automating skill matching and assessment generation.</li>
        <li><b>Efficiently Rank Candidates:</b> Provide a streamlined process to rank candidates based on relevant skills and experience.</li>
        <li><b>Generate Tailored Assessments:</b> Create customized assessments for each job role, assessing the skills most important to that role.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown('<div class="about-header">Data Sources</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="about-paragraph">This application utilizes:</p>
    <ul class="about-list">
        <li><b>Job Description:</b> A job description document provided by the user.</li>
        <li><b>SkillsFuture Framework:</b> The publically available SkillsFuture Framework that allows for matching job responsibilities to relevant skills.</li>
        <li><b>Candidate Resumes:</b> Bulk-uploaded resumes of candidates for skill extraction and scoring.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("**I have included some files to use as samples for the application which you can find in the 'Sample Files' page.**")

    st.markdown('<div class="about-header">Key Features</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="about-list">
        <li><b>Job Description Parsing:</b> Uses an LLM to parse job descriptions and match them with relevant skills from the SkillsFuture framework.</li>
        <li><b>Candidate Scoring:</b> Scores candidates based on matched skills, proficiency levels, and job relevance (importance score).</li>
        <li><b>Assessment Generation:</b> Creates a tailored assessment for the top candidates and generates an answer key for evaluation.</li>
        <li><b>Downloadable Assessments:</b> Allows users to download generated assessment files with a suggested answer key for each candidate in a ZIP file.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="about-header">Future Improvements</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="about-list">
        <li><b>Integration with External Databases:</b> Enabling automatic data retrieval from online sources or company databases.</li>
        <li><b>Dynamic Job Descriptions:</b> Allowing users to add or customize job responsibilities within the app.</li>
        <li><b>Advanced Filtering and Sorting:</b> Adding more filters and sorting options for candidates based on various criteria.</li>
        <li><b>Enhanced UI Design:</b> Incorporating additional CSS or JavaScript for a more interactive experience.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add an image or logo if relevant
    # st.image("path/to/image.png", caption="Project Logo or Illustration")

