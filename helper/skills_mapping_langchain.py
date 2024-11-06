import streamlit as st
import pandas as pd
from helper.file_handler import parse_job_description
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import json

# Initialize the LangChain LLM
llm = OpenAI(api_key=st.secrets["PERSONAL_OPENAI_API_KEY"])

def load_skills_future_framework(file_path):
    """
    Loads the SkillsFuture Framework from an Excel file and returns a DataFrame.
    """
    framework_df = pd.read_excel(file_path)
    return framework_df 

def extract_keywords_from_job_description(jd_text):
    """
    Extracts relevant keywords from a parsed job description.
    """
    # Use the existing parse function to get structured job description data
    parsed_data = parse_job_description(jd_text)
    
    # Combine keywords from all relevant fields
    responsibilities = parsed_data.get("Responsibilities", [])
    qualifications = parsed_data.get("Qualifications", [])
    skills = parsed_data.get("Skills", [])
    
    # Consolidate all keywords into a single list and preprocess
    keywords = responsibilities + qualifications + skills
    keywords = [keyword.lower() for keyword in keywords]  # Normalize to lowercase
    
    # Remove duplicates
    keywords = list(set(keywords))
    
    return keywords

# Define LangChain prompt templates for the chaining process
# First prompt: Extract skills and responsibilities from the job description
extract_skills_prompt = PromptTemplate(
    input_variables=["job_description"],
    template="""
    Given the job description below, identify at most 10 key skills and responsibilities required for this role.
    List them in a strict JSON format as follows:
    [
      {{"responsibility": "responsibility text 1"}},
      {{"responsibility": "responsibility text 2"}},
      ...
    ]

    Job Description:
    {job_description}
    """
)

# Second prompt: Match extracted responsibilities to the SkillsFuture Framework
match_skills_prompt = PromptTemplate(
    input_variables=["extracted_skills", "framework_text"],
    template="""
    Based on the extracted skills and responsibilities below (maximum of 8 extracted skills), match each one with the closest relevant skill from the SkillsFuture Framework.
    Output the result in strict JSON format as follows:
    [
      {{"responsibility": "responsibility text 1", "matched_skill": "relevant skill from framework"}},
      {{"responsibility": "responsibility text 2", "matched_skill": "relevant skill from framework"}},
      ...
    ]

    Extracted Skills:
    {extracted_skills}

    SkillsFuture Framework:
    {framework_text}
    """
)

# Create individual LLMChains for each prompt
extract_chain = LLMChain(llm=llm, prompt=extract_skills_prompt, output_key="extracted_skills")
match_chain = LLMChain(llm=llm, prompt=match_skills_prompt, output_key="matched_skills")

# Combine them into a SequentialChain
sequential_chain = SequentialChain(
    chains=[extract_chain, match_chain],
    input_variables=["job_description", "framework_text"],
    output_variables=["matched_skills"]
)

def llm_assisted_skill_matching(job_description, framework_df):
    """
    Uses LangChain to match job description responsibilities to relevant skills in the SkillsFuture Framework.
    
    Args:
        job_description (str): The full text of the job description.
        framework_df (DataFrame): The SkillsFuture Framework DataFrame.
        
    Returns:
        list: Structured output with matched skills and importance ranking.
    """
    # Convert the skills framework into a text format the LLM can read
    framework_text = json.dumps(framework_df.to_dict(orient="records"))

    # First, extract skills and responsibilities
    extracted_skills_response = extract_chain.run({"job_description": job_description})
    extracted_skills_response = extracted_skills_response.strip("```json").strip("```").strip()  # Clean JSON output
    print("Raw LLM Response for Extracted Skills:", extracted_skills_response)  # Debugging line
    extracted_skills = json.loads(extracted_skills_response)

    # Next, match the extracted skills to the SkillsFuture Framework
    matched_skills_response = match_chain.run({"extracted_skills": json.dumps(extracted_skills), "framework_text": framework_text})
    matched_skills_response = matched_skills_response.strip("```json").strip("```").strip()  # Clean JSON output
    print("Raw LLM Response for Matched Skills:", matched_skills_response)  # Debugging line
    matched_skills = json.loads(matched_skills_response)

    return matched_skills

def remove_duplicate_skills(jd_matched_skills):
    """
    Removes duplicate skills from the job description matched skills.
    Keeps the entry with the highest proficiency level if duplicates exist.

    Args:
        jd_matched_skills (list): List of skills matched to the job description.

    Returns:
        list: List of unique skills for the job description.
    """
    unique_skills = {}
    
    for skill in jd_matched_skills:
        skill_name = skill["Skill"]
        
        # If the skill is not already in unique_skills, add it
        # If it is, replace it only if the new entry has a higher proficiency level
        if skill_name not in unique_skills:
            unique_skills[skill_name] = skill
        else:
            # Check if the current skill has a higher proficiency level than the existing one
            current_proficiency = skill.get("Proficiency Level", "N/A")
            existing_proficiency = unique_skills[skill_name].get("Proficiency Level", "N/A")
            
            # Define a simple proficiency hierarchy for comparison, if necessary
            proficiency_order = {"Basic": 1, "Intermediate": 2, "Advanced": 3}
            if proficiency_order.get(current_proficiency, 0) > proficiency_order.get(existing_proficiency, 0):
                unique_skills[skill_name] = skill

    return list(unique_skills.values())
