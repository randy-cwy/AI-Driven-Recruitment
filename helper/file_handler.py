import docx
from helper.llm import get_completion

# Function to extract text from a .docx file
def extract_text_from_docx(docx_file):
    """
    Extracts and returns text from a Word (.docx) file.
    """
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to call LLM for parsing the JD text
def parse_job_description(jd_text):
    """
    Sends the job description text to the LLM and returns the parsed output using advanced prompt techniques.
    """
    prompt = f"""
    Analyze the following job description and extract key information step by step:
    1. First, extract the job title.
    2. Then, list the top 5 responsibilities mentioned.
    3. Next, list the required qualifications.
    4. Finally, extract the key skills required based on the top 5 responsibilities.
    Return the result in the following structured format:
    {{
      "Job Title": "...",
      "Responsibilities": ["...", "...", "..."],
      "Qualifications": ["...", "..."],
      "Skills": ["...", "..."]
    }}
    
    Job Description:
    {jd_text}
    """
    
    response = get_completion(prompt)

    try:
        parsed_data = eval(response)  # Converts the response string to a dictionary (use with caution)
    except:
        parsed_data = {"Job Title": None, "Responsibilities": [], "Qualifications": [], "Skills": []}
    
    return parsed_data

# Main function that runs the entire file handling and parsing flow
def process_job_description_file(docx_file):
    """
    Main function to handle file extraction and LLM parsing.
    This function extracts the text from the Word file and sends it to the LLM for parsing.
    """
    jd_text = extract_text_from_docx(docx_file)
    
    parsed_output = parse_job_description(jd_text)
    
    return jd_text, parsed_output
