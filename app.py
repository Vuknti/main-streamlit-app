 import streamlit as st
from docx import Document
import fitz  # PyMuPDF
from utils import extract_text_from_pdfs, fill_docx_with_llm

st.title("📋 GLR Template Filler – Insurance Automation")

st.markdown("Upload a `.docx` template and one or more `.pdf` photo reports:")

template_file = st.file_uploader("Upload Insurance Template (.docx)", type=["docx"])
pdf_files = st.file_uploader("Upload Photo Report PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("Generate Filled Template") and template_file and pdf_files:
    with st.spinner("Extracting text and contacting LLM..."):
        # Read and extract from PDFs
        full_text = extract_text_from_pdfs(pdf_files)
        
        # Fill template with LLM response
        filled_docx = fill_docx_with_llm(template_file, full_text)

        # Save to BytesIO for download
        from io import BytesIO
        output = BytesIO()
        filled_docx.save(output)
        output.seek(0)

        st.success("✅ Template filled successfully!")
        st.download_button(
            label="📥 Download Filled Template",
            data=output,
            file_name="filled_template.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
