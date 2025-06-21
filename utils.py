import fitz  # PyMuPDF
from docx import Document
import requests

# Extract text from PDF files
def extract_text_from_pdfs(pdf_files):
    text = ""
    for pdf in pdf_files:
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    return text

# Use LLM to fill a .docx template
def fill_docx_with_llm(template_file, extracted_text):
    # Load .docx
    doc = Document(template_file)

    # Prompt to extract key-value pairs
    prompt = f"""
You are a document assistant. Extract relevant key-value pairs to fill an insurance report template from the following text:\n\n{extracted_text}
Only return key-value pairs in the format:

Field Name: Value
Field Name: Value
...
"""

    # Send to OpenRouter API (replace YOUR_KEY)
    headers = {
        "Authorization": "Bearer YOUR_OPENROUTER_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # or use another LLM
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()["choices"][0]["message"]["content"]

    # Parse LLM response
    field_data = {}
    for line in result.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            field_data[key.strip()] = value.strip()

    # Replace text in docx
    for p in doc.paragraphs:
        for key, value in field_data.items():
            if key in p.text:
                p.text = p.text.replace(key, value)

    return doc
