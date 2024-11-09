import PyPDF2
from docx import Document  # python-docx for .docx processing
from helper.llm import get_completion
import json

def extract_text_from_file(file):
    """
    Extracts text from a .docx or .pdf file.
    
    Args:
        file (UploadedFile): The resume file uploaded by the user.
        
    Returns:
        str: Extracted text from the file.
    """
    if file.name.endswith('.docx'):
        # Read .docx file
        doc = Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file.name.endswith('.pdf'):
        # Read .pdf file using PyPDF2
        pdf_text = ""
        pdf_reader = PyPDF2.PdfReader(file)  # Use PyPDF2 to read the PDF

        # Loop through all the pages and extract text
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text

        # Return or use the extracted text as needed
        return pdf_text
    else:
        raise ValueError("Unsupported file format")

def match_candidate_skills(resume_text, framework_df):
    """
    Uses the LLM to match the resume text with relevant skills from the SkillsFuture Framework.
    
    Args:
        resume_text (str): The text extracted from a resume.
        framework_df (DataFrame): The SkillsFuture Framework DataFrame.
        
    Returns:
        dict: A structured output with the candidate's qualifications and matched skills.
    """
    # Convert SkillsFuture Framework to a JSON-like format
    framework_text = framework_df.to_dict(orient="records")
    
    # Craft the prompt to extract qualifications and map skills
    prompt = f"""
    Given the following resume text, extract the candidate's full name, qualifications and match their skills to the most relevant skills from the SkillsFuture Framework. You are not allowed to use or create your own 'Skill' and are to strictly use relevant skills from the SkillsFuture Framework.
    
    Only match skills that have been mentioned anywhere in the resume. For example, do not assume that the candidate has "Communication" skill unless there is a phrase stating that "Possess good communication skill".

    To determine the proficiency level that the candidate possesses, you will have to either find out how long they have studied the skill in school or how many years of experience they have with the skill through reading their job history. If it cannot be determined from the method above, you can make an educated guess, for example, if the candidate is a fresh graduate, skill profiency should not be at an advanced level. However, if the candidate has 10 years of experience in the field, skill proficiency should not be at a basic level.
    
    Resume Text:
    <resume_text>{resume_text}</resume_text>
    
    SkillsFuture Framework:
    <SkillsFuture_Framework>{framework_text}</SkillsFuture_Framework>
    
    Please output the result in strict JSON format as shown in the example:
    {{
      "Name": "Candidate's full name",
      "Qualification": "Extracted qualification information",
      "Skills": [
        {{
          "Skill": "Skill name from framework",
          "Category": "Category name",
          "Proficiency Level": "Proficiency level",
          "Explanation": "The text from the resume you used to determine this data"
        }},
        ...
      ]
    }}
    """
    
    response = get_completion(prompt)

    # Clean up the response to remove any extra formatting like ```json
    response = response.strip("```json").strip("```").strip()

    #print("LLM Response:", response)

    try:
        return json.loads(response)  # Attempt to parse JSON
    except json.JSONDecodeError:
        print("Invalid JSON response from LLM:", response)  # Log invalid response for debugging
        return {
            "Name": "Unknown",
            "Qualification": "N/A",
            "Skills": []
        }


def process_bulk_resumes(resume_files, framework_df):
    """
    Processes multiple resumes and generates a JSON output for each candidate's name, qualifications, and skills.
    
    Args:
        resume_files (list): List of resume files uploaded by the user.
        framework_df (DataFrame): The SkillsFuture Framework DataFrame.
        
    Returns:
        dict: A dictionary containing each candidate's data by their name.
    """
    candidate_data = {}
    
    for resume_file in resume_files:
        # Extract text from the resume
        resume_text = extract_text_from_file(resume_file)
        
        # Match candidate's skills and extract name, qualifications, and skills using LLM
        candidate_info = match_candidate_skills(resume_text, framework_df)
        
        # Use extracted name as candidate identifier in the output
        candidate_name = candidate_info.get("Name", "Unknown Candidate")
        candidate_data[candidate_name] = candidate_info
    
    return candidate_data

