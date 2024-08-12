import streamlit as st
from extraction_pipeline import pdf_page_to_image

# Streamlit page title
st.title("Resume Builder using Job Description")

# PDF input
uploaded_pdf = st.file_uploader("Upload your resume (PDF format)", type="pdf")

# Job description input
job_description = st.text_area("Enter the job description")

# Variables to store inputs
resume_image_path = None
jobd = ""

# Convert PDF to image, save to temp folder, and display
if uploaded_pdf is not None:
    pdf_bytes = uploaded_pdf.read()
    resume_image_path = pdf_page_to_image()
    if resume_image_path:
        st.write("Extracted Resume Image:")
        st.image(resume_image_path, caption='Resume Page', use_column_width=True)

# Store job description
if job_description:
    jobd = job_description
    st.write("Job Description:")
    st.write(jobd)

# Add logic here to handle the backend processing
# For example, you could call a function here that processes the resume image path and job description
# process_resume(resume_image_path, jobd)
