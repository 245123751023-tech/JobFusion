import openai
from fpdf import FPDF
from django.core.files.base import ContentFile
import io

openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_resume(profile_data):
    """
    Generates AI-powered professional resume content
    and returns PDF bytes.
    """
    # Prepare AI prompt
    prompt = f"""
    Create a highly professional resume for the following candidate:
    
    Full Name: {profile_data['full_name']}
    Email: {profile_data['Email']}
    Role: {profile_data['Role']}
    LinkedIn: {profile_data.get('liurl', '')}
    Phone: {profile_data['phone']}
    Location: {profile_data['location']}
    Bio: {profile_data['bio']}
    Skills: {profile_data['skills']}
    Other Skills: {profile_data.get('otherskills','')}
    Experience: {profile_data.get('exp','')}
    Education:
      - Graduation: {profile_data.get('gclg','')} ({profile_data.get('gstartingyear','')}-{profile_data.get('gendingyear','')})
      - Intermediate: {profile_data.get('iclg','')} ({profile_data.get('istartingyear','')}-{profile_data.get('iendingyear','')})
      - School: {profile_data.get('schoolname','')} ({profile_data.get('sscyear','')})
    """
    
    # Call OpenAI to generate professional resume content
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"system", "content":"You are a professional resume writer."},
            {"role":"user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    resume_text = response['choices'][0]['message']['content'].strip()

    # Convert text to PDF using FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(0, 10, profile_data['full_name'], align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.ln(2)
    contact_info = f"Email: {profile_data['Email']} | Phone: {profile_data['phone']} | LinkedIn: {profile_data.get('liurl','')}\nLocation: {profile_data['location']}"
    pdf.multi_cell(0, 8, contact_info, align='C')
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Professional Resume", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, resume_text)
    
    # Save PDF to bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    
    return pdf_bytes
