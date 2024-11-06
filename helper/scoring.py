import json
from helper.llm import get_completion

def load_json_data(jd_skills_str, candidate_results_str):
    """
    Converts JSON strings into dictionaries.
    
    Args:
        jd_skills_str (str): JSON string of job description matched skills.
        candidate_results_str (str): JSON string of all candidate results.
        
    Returns:
        tuple: Job description skills and candidate results as dictionaries.
    """
    jd_skills = json.loads(jd_skills_str)
    candidate_results = json.loads(candidate_results_str)
    return jd_skills, candidate_results

def evaluate_skill_relevance(candidate_skill, jd_skill):
    """
    Uses the LLM to evaluate the relevance of a candidate's skill to the job description skill.
    
    Args:
        candidate_skill (dict): A skill from the candidate's skillset.
        jd_skill (dict): A skill from the job description's requirements.
        
    Returns:
        float: Relevance score (1.0 for Full Match, 0.5 for Partial Match, 0.0 for No Match).
    """
    prompt = f"""
    Evaluate the relevance of the candidate's skill to the job description skill.
    
    Candidate Skill: {candidate_skill['Skill']}
    Job Description Skill: {jd_skill['Skill']}
    
    Please respond with one of the following:
    - "Full Match" if the skills are the same or nearly identical.
    - "Partial Match" if there is some relevance between the skills.
    - "No Match" if the skills are not relevant.
    """
    
    response = get_completion(prompt).strip()
    
    relevance_mapping = {
        "Full Match": 1.0,
        "Partial Match": 0.5,
        "No Match": 0.0
    }
    return relevance_mapping.get(response, 0.0)

def calculate_skill_score(candidate_skill, jd_skill):
    """
    Calculates the score for a single skill based on relevance, proficiency, and importance, with applied weights.
    Proficiency is awarded fully if the candidate has the required or higher proficiency level.
    Importance is only considered if the skill is relevant; non-matching skills are penalized based on their importance.
    
    Args:
        candidate_skill (dict): The candidate's matched skill with proficiency level.
        jd_skill (dict): The job description's required skill with proficiency level and importance.
        
    Returns:
        float: The weighted score for this skill match.
    """
    # Define weights for each scoring category
    relevance_weight = 0.6
    proficiency_weight = 0.20
    importance_weight = 0.20

    # Calculate relevance score using LLM
    relevance_points = evaluate_skill_relevance(candidate_skill, jd_skill)
    
    proficiency_points = 0
    importance_points = 0
    
    # Calculate proficiency and importance points based on relevance
    if relevance_points > 0:
        # Calculate proficiency score with your modification for higher proficiency levels
        if candidate_skill["Proficiency Level"] == jd_skill["Proficiency Level"]:
            proficiency_points = 1
        elif (candidate_skill["Proficiency Level"], jd_skill["Proficiency Level"]) in [
            ("Advanced", "Intermediate"),
            ("Advanced", "Basic"),
            ("Intermediate", "Basic")
        ]:
            proficiency_points = 1
        elif (candidate_skill["Proficiency Level"], jd_skill["Proficiency Level"]) in [
            ("Intermediate", "Advanced"), 
            ("Basic", "Intermediate")
        ]:
            proficiency_points = 0.5

        # Calculate importance points based on JD importance level
        importance_points = jd_skill.get("Importance", 3) * importance_weight
    else:
        # Apply a penalty for non-matching skills based on importance level
        importance_points = 0 if jd_skill.get("Importance", 3) <= 2 else 0.1

    # Calculate the total weighted score for the skill
    weighted_score = (
        (relevance_points * relevance_weight) +
        (proficiency_points * proficiency_weight) +
        (importance_points)
    )
    
    return weighted_score

def score_candidate(candidate_info, jd_matched_skills):
    total_score = 0.0
    
    for jd_skill in jd_matched_skills:
        for candidate_skill in candidate_info["Skills"]:            
            # Check if the structure is as expected
            if isinstance(jd_skill, dict) and isinstance(candidate_skill, dict):
                if candidate_skill["Skill"] == jd_skill["Skill"]:
                    total_score += calculate_skill_score(candidate_skill, jd_skill)
                    break
            else:
                print("Unexpected data structure:", jd_skill, candidate_skill)  # Debugging line
                
    max_possible_score = len(jd_matched_skills) * 1.5
    normalized_score = (total_score / max_possible_score) * 100
    return min(normalized_score, 100)

def score_all_candidates(candidate_results, jd_matched_skills):
    """
    Scores all candidates and returns a dictionary with candidate names and their scores.
    
    Args:
        candidate_results (dict): All candidate data.
        jd_matched_skills (list): Job description matched skills with importance and proficiency levels.
        
    Returns:
        dict: Scores for each candidate, normalized to a 0-100 range.
    """
    candidate_scores = {}
    for candidate_name, candidate_info in candidate_results.items():
        candidate_scores[candidate_name] = score_candidate(candidate_info, jd_matched_skills)
    return candidate_scores
