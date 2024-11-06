# 🚀 LLM-Powered Job Description Parsing and Candidate Scoring App

Welcome to the **LLM-Powered Job Description Parsing and Candidate Scoring App**! This proof-of-concept (POC) application automates job description parsing, skill matching, scoring, and assessment generation for candidate evaluation. Using Large Language Models (LLMs), this app provides a streamlined, efficient way to screen candidates and generate custom assessments.

## 📜 Table of Contents
- [📚 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🔄 Data Flow & Methodology](#-data-flow--methodology)
- [🛠 Design Considerations](#-design-considerations)
- [🚀 Usage](#-usage)
- [🌱 Future Improvements](#-future-improvements)

## 📚 Project Overview
This app supports HR teams by automating aspects of the candidate evaluation process. It takes a job description and bulk-uploaded candidate resumes, extracts relevant skills, scores candidates based on proficiency and job relevance, and generates custom assessments for top candidates. The goal is to make candidate evaluation efficient and reduce manual effort.

## ✨ Features
- **🔍 Job Description Parsing**: Analyzes job descriptions to identify critical skills and responsibilities.
- **📊 Skills Matching with SkillsFuture Framework**: Matches parsed skills to the SkillsFuture Framework, incorporating proficiency-based scoring.
- **📈 Candidate Scoring**: Scores candidates based on skill alignment, proficiency, and job relevance.
- **📝 Assessment Generation**: Creates tailored assessments and an answer key, downloadable as a ZIP file.
- **🖥 User-Friendly Interface**: A Streamlit-based UI with expanders, progress bars, and download options.

## 🔄 Data Flow & Methodology
### 🧩 Job Description Parsing
- **Parsing Key Skills**: The LLM parses the job description, identifying key responsibilities and skills.
- **SkillsFuture Framework Matching**: Extracted job skills are mapped to the SkillsFuture Framework to determine relevant skills, proficiency levels, and job importance.

### 📝 Candidate Resume Processing
- **Skill Matching**: The LLM identifies relevant skills from each candidate’s resume, assigns proficiency levels, and outputs results in a structured JSON format.
- **Proficiency Evaluation**: The model determines proficiency based on experience or educational background, guided by a custom prompt.

### 🏆 Scoring & Ranking
- **Weighted Scoring Criteria**: Each scoring component is weighted to emphasize skill relevance (60%), proficiency (20%), and job importance (20%).
- **Normalization**: Scores are normalized to a 0–100% scale for comparative ranking.
- **Candidate Ranking**: Users can select the top X candidates for assessment generation.

### 📝 Assessment Generation
- **Custom Assessments**: Generates unique assessments for the job role, along with an answer key for evaluation, all zipped into a downloadable file.

## 🛠 Design Considerations
- **🚫 Avoided Prompt Chaining**: Avoided prompt chaining due to computation delays and token limitations, improving response time.
- **👥 No Agents Needed**: The linear workflow didn’t require agents, simplifying the project’s architecture.
- **🔒 No Prompt Injection Techniques**: Users don’t directly interact with the LLM, making prompt injection unnecessary.
- **📊 Progress Indicators**: Progress bars enhance the user experience, particularly for large data uploads.

## 🚀 Usage

1. **Access the App**:  
   Simply visit [this link to access the LLM-Powered Recruitment App](https://ai-champions-llm-recruitment.streamlit.app/).

2. **Navigate through the App**:
   - **Home**: This is the main page where you’ll upload the required files, select the number of top candidates, and run the scoring and assessment generation processes.
   - **Sample Files**: View and download sample files (e.g., job description, SkillsFuture Framework, and candidate resumes) to understand the format requirements.
   - **About**: Learn about the project’s objectives, scope, and key features, as well as considerations taken during development.
   - **Methodology**: Explore the data flow, technical implementation, and scoring methodology for a deep dive into the app's inner workings.

3. **Steps on the Home Page**:
   - **Step 1**: Upload the job description, SkillsFuture Framework file, and candidate resumes.
   - **Step 2**: Select the number of top candidates you’d like to display.
   - **Step 3**: Generate assessment files for the chosen candidates, and download them as a ZIP package with a single click.

## 🌱 Future Improvements
- **🔗 Database Integration**: Enable direct data retrieval from external databases or job portals.
- **🧹 Advanced Filtering & Sorting**: Add more filters for refined candidate rankings.
- **🎨 Enhanced UI Design**: Incorporate additional CSS customization for an improved user experience.

---

> This project is designed as a proof-of-concept. Please use responsibly, as generated data should not be relied upon for critical decisions without verification.

