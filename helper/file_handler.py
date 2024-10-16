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
    Sends the job description text to the LLM and returns the parsed output.
    """
    prompt = f"""
    
    Extract the key responsibilities, required skills, and qualifications from the following job description:\n\n{jd_text}
    
    
    """
    
    # Call the LLM using the get_completion function
    response = get_completion(prompt)
    return response

# Main function that runs the entire file handling and parsing flow
def process_job_description_file(docx_file):
    """
    Main function to handle file extraction and LLM parsing.
    This function extracts the text from the Word file and sends it to the LLM for parsing.
    """
    # Step 1: Extract text from the .docx file
    jd_text = extract_text_from_docx(docx_file)
    
    # Step 2: Send the extracted text to the LLM for parsing
    parsed_output = parse_job_description(jd_text)
    
    # Return both the extracted text and parsed output
    return jd_text, parsed_output
