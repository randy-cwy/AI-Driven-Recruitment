import streamlit as st

def methodology_page():
    # Add CSS for styling
    st.markdown("""
        <style>
        .methodology-header {
            font-size: 26px;
            color: #004B87;
            margin-bottom: 10px;
        }
        .methodology-subheader {
            font-size: 20px;
            margin-bottom: 10px;
        }
        .methodology-paragraph {
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        ul.methodology-list {
            list-style-type: disc;
            padding-left: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Content
    st.title("Methodology")
    
    st.markdown('<div class="methodology-header">Data Flow & Implementation</div>', unsafe_allow_html=True)
    st.markdown("""
    <p class="methodology-paragraph">The project's data flow involves structured steps, beginning with parsing the job description and proceeding through candidate evaluation, scoring, and assessment generation. Implementation details are also covered in this section.</p>
    <ul class="methodology-list">
        <li><b>Step 1: Job Description Parsing, found in <code>helper/file_handler.py</code>:</b>
            <ul>
                <li>The job description file, which can be a <code>.docx</code> or <code>.pdf</code> format, is uploaded by the user.</li>
                <li>The file is read, and the LLM is tasked with extracting specific sections relevant to the role, such as job responsibilities, qualifications, and desired skills.</li>
                <li>The extracted text undergoes further text processing to consolidate key phrases. This parsing ensures that each responsibility or skill is clearly identified before moving on to the skills matching phase.</li>
                <li>Each identified responsibility or skill is formatted into a JSON structure, making it easier for subsequent processes to consume and analyze the data.</li>
            </ul>
        </li>
        <li><b>Step 2: SkillsFuture Framework Matching, found in <code>helper/skills_mapping.py</code>:</b>
            <ul>
                <li>The SkillsFuture Framework file, an <code>.xlsx</code> spreadsheet, is uploaded to provide a structured list of skills with their categories, proficiency levels, and descriptions. The file is loaded into a DataFrame for easier manipulation and access.</li>
                <li>Using the parsed job description data, the LLM matches each responsibility and skill requirement with the most relevant skills in the SkillsFuture Framework. This matching accounts for:
                    <ul>
                        <li><b>Relevance:</b> The LLM identifies the closest skill within the framework based on the context and content of the job description.</li>
                        <li><b>Proficiency Level:</b> For each skill match, the LLM assigns a proficiency level, selecting the highest relevant proficiency if multiple options are available within the framework.</li>
                    </ul>
                </li>
                <li>The output includes the job responsibility, matched skill, assigned proficiency, a rationale explaining the match, and an <b>importance ranking</b> (1-5, with 1 being most important) for each matched skill based on the job's requirements.</li>
                <li>To maintain accuracy, duplicates are removed at the end of this matching process.</li>
            </ul>
        </li>
        <li><b>Step 3: Candidate Resume Processing, found in <code>helper/bulk_resume_processor.py</code>:</b>
            <ul>
                <li><b>Bulk Resume Upload:</b> The application supports simultaneous uploads of multiple resumes in <code>.docx</code> and <code>.pdf</code> formats, streamlining the processing of multiple candidates in a single action.</li>
                <li><b>Text Extraction:</b> For each resume, text extraction is tailored based on file type. <code>.docx</code> files are read directly, while <code>.pdf</code> files are processed using <code>PyMuPDF</code> to accurately extract the text for analysis.</li>
                <li><b>Candidate Name Identification:</b> The LLM identifies the candidate's name directly from the resume content. This name is consistently used as a unique identifier throughout the application to organize and display each candidate's information.</li>
                <li><b>Skill Extraction:</b> The extracted resume text is sent to the LLM for skill extraction. The LLM scans for relevant skills, qualifications, and experiences, identifying any keywords or phrases that indicate valuable competencies for the job.</li>
                <li><b>Skills Matching Against Framework:</b> Each identified skill is matched against the SkillsFuture Framework for relevancy
                <li><b>Proficiency Evaluation:</b>
                    <ul>
                        <li><b>Determining Proficiency Levels:</b> The LLM assesses each candidate's skill proficiency based on their resume's details, guided by a custom prompt:
                            <ul>
                                <li><b>Experience-Based:</b> Proficiency is estimated by years of relevant experience—e.g., 10+ years implies advanced proficiency, while fresh graduates are assigned lower levels.</li>
                                <li><b>Education-Based:</b> The duration or intensity of skill study in formal education can raise proficiency levels, even without extensive work experience.</li>
                                <li><b>Heuristic-Based:</b> If experience or education is unclear, the LLM infers proficiency based on typical career stages—assigning lower levels to new grads and higher levels to seasoned professionals.</li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ul>
        </li>
        <li><b>Step 4: Candidate Scoring and Ranking, found in <code>helper/scoring.py</code>:</b>
            <ul>
                <li><b>Matching Relevance:</b> Each candidate's skill is compared with the job description's matched skills and scored as follows:
                    <ul>
                        <li><b>Full Match:</b> A full score is awarded when the candidate's skill directly aligns with the job requirement.</li>
                        <li><b>Partial Match:</b> A partial score is awarded when the candidate's skill is related but not an exact match.</li>
                        <li><b>No Match:</b> No points are given when no related skill is found for a given job requirement.</li>
                    </ul>
                </li>
                <li><b>Proficiency Scoring:</b> For each matched skill, the candidate's proficiency level is assessed and scored:
                    <ul>
                        <li><b>Higher Proficiency:</b> A full score is given if the candidate's proficiency exceeds the required level.</li>
                        <li><b>Equal Proficiency:</b> A full score is awarded if the candidate's proficiency matches the job requirement.</li>
                        <li><b>Lower Proficiency:</b> A partial score is given if the candidate's proficiency is slightly below the required level.</li>
                        <li><b>Too Low Proficiency:</b> No score is given if the candidate's proficiency is too far below the required level.</li>
                    </ul>
                </li>
                <li><b>Importance Weighting:</b> Each skill from the job description is ranked by importance (on a scale of 1-5, with 1 being the most critical). Higher-importance skills contribute more significantly to the overall score, emphasizing skills essential to the role.</li>
                <li><b>Weightages for Scoring Components:</b> To accurately reflect each scoring component's importance, weightages were assigned as follows:
                    <ul>
                        <li><b>Relevance Weight (0.60):</b> Given the most significance, as matching the required skills directly impacts the candidate's suitability for the job.</li>
                        <li><b>Proficiency Weight (0.20):</b> Lower weight, since a match in skills is more critical than proficiency. However, proficiency still plays an important role in distinguishing candidates.</li>
                        <li><b>Importance Weight (0.20):</b> Similarly weighted to proficiency, since critical job responsibilities should have a meaningful influence on the candidate's final score.</li>
                    </ul>
                </li>
                <li><b>Normalization of Scores:</b> Each candidate's total score is normalized to a 0-100 scale, ensuring consistent comparison across candidates regardless of specific skill requirements or job weights.</li>
                <li><b>Final Ranking:</b> Candidates are ranked by their normalized scores, with the highest-scoring candidates displayed at the top. This ranking enables hiring managers to quickly identify the best-qualified candidates for the job role.</li>
            </ul>
        <li><b>Step 5: Candidate Filtering, found in <code>main.py</code>:</b> After scoring, candidates are ranked based on their total scores, allowing the user to specify the number of top candidates to display.
            <ul>
                <li><b>Filtering Top X Candidates:</b> The user can input the desired number of top candidates (e.g., top 5 or top 10). The system filters the highest-ranking candidates based on their final scores, ensuring that only the most suitable candidates are highlighted.</li>
                <li><b>Dynamic Selection:</b> This filtering is dynamically adjustable, so users can modify the number of top candidates displayed without recalculating scores, as the candidate rankings are saved for easy access and sorting.</li>
            </ul>
        </li>
        <li><b>Step 6: Assessment Generation and Answer Key, found in <code>helper/assessment_generator.py</code>:</b> The system generates tailored assessments for each of the top X candidates based on the selected number in the previous filtering step.
            <ul>
                <li><b>Custom Assessment Questions:</b> The application generates a set of skill-based questions, each tailored to the job's requirements. Every candidate receives the same assessment document, focusing on key skills identified during job description parsing.</li>
                <li><b>Answer Key Generation:</b> Alongside the assessments, the system creates a suggested answer key document. This answer key includes model answers for each question to guide HR staff or hiring managers during the evaluation process.</li>
                <li><b>Zipped File for Download:</b> After generating individual assessment documents for each candidate and an answer key, all files are automatically zipped into a single downloadable file. Users can download this file conveniently with one click, saving time and ensuring all assessment materials are securely grouped together.</li>
            </ul>
        </li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown('<div class="methodology-header">Design Considerations</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="methodology-list">
        <li><b>No Prompt Chaining:</b>
            <ul>
                <li><b>Increased Computation Time:</b> During development, I experimented with both manual prompt chaining and LangChain but ultimately chose not to include them due to performance impacts. Manual prompt chaining noticeably extended computation time, as each additional prompt cycle accumulated processing delays. To keep the user experience responsive, I prioritized reducing these delays, especially since the difference in results (with/without prompt chaining) was minimal.</li>
                <li><b>Token Limits and Truncated Responses:</b> With LangChain, I frequently encountered token limits, resulting in truncated responses. This made LangChain unreliable for handling longer job descriptions and multiple resumes.</li>
            </ul>
        </li>
        <li><b>Agents Not Required:</b>
            <ul>
                <li><b>Linear Workflow:</b> This project follows a straightforward sequence—parsing job descriptions, matching skills, scoring candidates, and generating assessments. Since each step is handled once with static inputs, an iterative agent wasn't necessary.</li>
                <li><b>No Dynamic Adaptation Needed:</b> The workflow doesn't require adjustments based on prior actions or feedback. Since there are no branching paths or real-time decision-making requirements, agents would have added unnecessary complexity.</li>
                <li><b>Clear, Predefined Steps:</b> With a defined pathway and no need for exploring alternative strategies, agents were not needed to manage complex decision flows.</li>
            </ul>
        </li>
        <li><b>No Prompt Injection Protections Needed:</b>
            <ul>
                <li><b>Restricted LLM Access:</b> I did not implement prompt injection safeguards since end users do not have direct access to the LLM. All interactions with the LLM are managed through predefined workflows, ensuring a controlled environment with no opportunity for prompt manipulation.</li>
            </ul>
        </li>
        <li><b>User Experience (UX) Optimization:</b>
            <ul>
                <li><b>Interactive Feedback:</b> I implemented a progress bar and loading spinner to keep users informed of long processing times, particularly for scoring and assessment generation, improving transparency and engagement.</li>
                <li><b>Session State Management:</b> Session state variables were utilized to manage and retain data across steps (e.g., candidate scores, JD skill matching), ensuring that results are not recomputed unnecessarily and providing a faster user experience when revisiting certain steps.</li>
            </ul>
        </li>
        <li><b>Performance Efficiency:</b>
            <ul>
                <li><b>Selective LLM Use:</b> The application leverages the LLM selectively for intensive, context-rich tasks, such as skill matching and assessment generation. Simpler tasks, such as filtering and scoring, are handled by the application's core logic to optimize processing speed and API usage.</li>
                <li><b>Data Structure Optimization:</b> Results are stored in structured formats (e.g., JSON, DataFrames), enabling easy access, filtering, and ranking without redundant LLM calls. This approach minimizes both computation time and token usage.</li>
            </ul>
        </li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown('<div class="methodology-header">Flowchart</div>', unsafe_allow_html=True)
    st.image("mydocs/flowchart.png", caption="Project Workflow Diagram")
