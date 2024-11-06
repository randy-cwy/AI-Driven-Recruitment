import pandas as pd
from helper.llm import get_completion
import json

def load_skills_future_framework(file_path):
    """
    Loads the SkillsFuture Framework from an Excel file and returns a DataFrame.
    """
    framework_df = pd.read_excel(file_path)
    
    return framework_df 

# def extract_keywords_from_job_description(jd_text):
#     """
#     Extracts relevant keywords from a parsed job description.
#     """
#     # Use the existing parse function to get structured job description data
#     parsed_data = parse_job_description(jd_text)
    
#     # Combine keywords from all relevant fields
#     responsibilities = parsed_data.get("Responsibilities", [])
#     qualifications = parsed_data.get("Qualifications", [])
#     skills = parsed_data.get("Skills", [])
    
#     # Consolidate all keywords into a single list and preprocess
#     keywords = responsibilities + qualifications + skills
#     keywords = [keyword.lower() for keyword in keywords]  # Normalize to lowercase
    
#     # Remove duplicates
#     keywords = list(set(keywords))
    
#     return keywords

def llm_assisted_skill_matching(job_description, framework_df):
    """
    Uses the LLM to match job description responsibilities to relevant skills in the SkillsFuture Framework,
    including a ranking of importance.
    
    Args:
        job_description (str): The full text of the job description.
        framework_df (DataFrame): The SkillsFuture Framework DataFrame.
        
    Returns:
        str: The LLM's structured output with matched skills and importance ranking.
    """
    # Convert the skills framework into a format the LLM can read, e.g., JSON-like structure or text table
    framework_text = framework_df.to_dict(orient="records")
    
    # Craft the prompt for the LLM
    prompt = f"""
    Given the following job description, map each key responsibility and skill to the most relevant skills in the SkillsFuture Framework.

    Job Description:
    {job_description}

    SkillsFuture Framework:
    {framework_text}

    For each responsibility and skill mentioned in the job description, provide only one relevant skill from the SkillsFuture Framework, along with the proficiency level required. Explain why it matches and rank its importance for this job on a scale of 1 to 5, with 1 being critical to the role and 5 being least important.

    Important Instructions:
    - Each skill in the final output must be unique. Do not repeat any skills that have already been mapped.
    - If multiple relevant skills are identified for a responsibility, include only the single most relevant one.
    - If there are differing proficiency levels for relevant skills, choose the one with the highest proficiency level and omit others.
    - The output should be in strict JSON format.

    Please output each entry in the following format:
    {{
        "Job Responsibility": "Identify relevant data sources and perform data collection...",
        "Skill": "Web Development",
        "Proficiency Level": "Intermediate",
        "Explanation": "Web scraping often involves using web development techniques...",
        "Importance": 4
    }},
    {{
        "Job Responsibility": "Process data, which includes cleaning and organising datasets...",
        "Skill": "SQL Database Management",
        "Proficiency Level": "Advanced",
        "Explanation": "This responsibility involves managing and structuring data...",
        "Importance": 5
    }}
    """

    response = get_completion(prompt)

    response = response.strip("```json").strip("```").strip()
    
    return response

# Prompt Chaining

# def extract_responsibilities(job_description):
#     """
#     Step 1: Extract key responsibilities and skills from the job description.
#     """
#     prompt = f"""
#     Analyze the following job description and identify the key responsibilities and skills required.

#     Job Description:
#     {job_description}

#     Provide the output in JSON format for each responsibility as a JSON list like this:
#     [
#       {{"Job Responsibility": "Responsibility 1"}},
#       {{"Job Responsibility": "Responsibility 2"}},
#       ...
#     ]
#     """
#     response = get_completion(prompt)
#     response = response.strip("```json").strip("```").strip()
#     return json.loads(response)

# def match_skills_to_framework(responsibilities, framework_df):
#     """
#     Step 2: Match each responsibility with relevant skills from the SkillsFuture Framework.
#     """
#     framework_text = json.dumps(framework_df.to_dict(orient="records"))
    
#     prompt = f"""
#     Based on the extracted responsibilities, find the most relevant skill in the SkillsFuture Framework for each responsibility.

#     Responsibilities:
#     {json.dumps(responsibilities)}

#     SkillsFuture Framework:
#     {framework_text}

#     Provide the output in JSON format with the relevant skill matched to each responsibility:
#     [
#       {{"Job Responsibility": "Responsibility 1", "Skill": "Skill 1", "Proficiency Level": "Proficiency Level"}},
#       ...
#     ]
#     """
#     response = get_completion(prompt)
#     response = response.strip("```json").strip("```").strip()
#     return json.loads(response)

# def add_importance_ranking(matched_skills):
#     """
#     Step 3: Rank each skill by importance and add explanations.
#     """
#     prompt = f"""
#     Based on the following matched skills, rank the importance of each skill for the job role on a scale of 1 to 5,
#     with 1 being critical and 5 being least important. Provide a brief explanation for each.

#     Matched Skills:
#     {json.dumps(matched_skills)}

#     Provide the output in strict JSON format with each entry as a JSON object:
#     [
#       {{"Job Responsibility": "Responsibility 1", "Skill": "Skill 1", "Proficiency Level": "Proficiency Level", "importance": 3, "Explanation": "Explanation here"}},
#       ...
#     ]
#     """
#     response = get_completion(prompt)
#     response = response.strip("```json").strip("```").strip()
#     return json.loads(response)

# def llm_assisted_skill_matching(job_description, framework_df):
#     """
#     Main function to perform prompt chaining for skill matching.
#     """
#     # Step 1: Extract responsibilities from the job description
#     responsibilities = extract_responsibilities(job_description)
    
#     # Step 2: Match extracted responsibilities to framework skills
#     matched_skills = match_skills_to_framework(responsibilities, framework_df)
    
#     # Step 3: Add importance ranking
#     final_output = add_importance_ranking(matched_skills)

#     # Step 4: Remove duplicate skills
#     final_output_no_dup = remove_duplicate_skills(final_output)
    
#     return final_output_no_dup

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