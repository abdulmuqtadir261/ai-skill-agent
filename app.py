from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import streamlit as st
from groq import Groq
import re
from pypdf import PdfReader

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Skill Agent", layout="wide")

# ================= LIGHT CREAM CSS =================
st.markdown("""
<style>
.stApp {
    background: #fdf6e3;
    color: #1f2937;
    font-family: 'Inter', sans-serif;
}
h1 {
    text-align: center;
    font-size: 48px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2, h3, p, label {
    color: #1f2937 !important;
}
textarea {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 16px !important;
    border: 1px solid #d1d5db !important;
}
section[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 16px;
    padding: 12px;
}
section[data-testid="stFileUploader"] * {
    color: #374151 !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    font-weight: 700;
    border-radius: 14px;
    padding: 12px 24px;
    border: none;
}
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 16px;
}
details {
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    padding: 10px;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= CLEAN FUNCTION =================
def clean_ai_output(text):
    text = text.replace("**", "")
    text = re.sub(r"(\d{2})(\d{2}) hours", r"\1-\2 hours", text)
    text = re.sub(r"(\d{2})(\d{2}) weeks", r"\1-\2 weeks", text)
    return text

# ================= PDF GENERATOR =================
def generate_pdf(text):
    doc = SimpleDocTemplate(
        "analysis_report.pdf",
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#7c3aed'),
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#000000'),
        spaceAfter=6,
        leading=16
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#000000'),
        leftIndent=20,
        spaceAfter=5,
        leading=16
    )

    content = []
    content.append(Paragraph("AI Skill Assessment Report", title_style))
    content.append(Spacer(1, 10))

    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            content.append(Spacer(1, 6))
            continue

        if any(heading in line.upper() for heading in [
            "SKILL SCORES", "SKILL GAPS", "LEARNING PLAN",
            "OVERALL MATCH SCORE", "FINAL RECOMMENDATION"
        ]):
            content.append(Spacer(1, 10))
            content.append(Paragraph(line, heading_style))

        elif line.startswith("-") or line.startswith("•") or line.startswith("*"):
            content.append(Paragraph(f"• {line[1:].strip()}", bullet_style))

        elif "|" in line:
            clean_line = line.replace("|", " | ").strip()
            if clean_line.replace("|", "").replace("-", "").replace(" ", "") != "":
                content.append(Paragraph(clean_line, normal_style))

        else:
            content.append(Paragraph(line, normal_style))

    doc.build(content)
    return "analysis_report.pdf"

# ================= GROQ CLIENT =================
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

# ================= UI =================
st.title("🎯 AI Skill Intelligence Engine")

st.markdown("""
### 🚀 AI-Powered Resume Analyzer
Upload your resume and job description to get:
- Skill scoring (AI-based)
- Gap analysis
- Learning roadmap
- Hiring recommendation
""")

st.divider()

# ================= INPUT =================
col1, col2 = st.columns(2)

with col1:
    jd = st.text_area("📋 Job Description", height=250)

with col2:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

resume = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume += text

if resume.strip() == "":
    resume = "No readable text found in resume PDF."

# ================= BUTTON =================
analyze = st.button("🚀 Analyze My Skills", use_container_width=True)

# ================= ANALYSIS =================
if analyze:

    if not jd or not uploaded_file:
        st.warning("⚠️ Please fill both Job Description and Upload Resume")
        st.stop()

    with st.spinner("AI is analyzing your profile..."):

        prompt = f"""
You are an expert AI recruiter and skill assessor.

Analyze the resume against the job description and return EXACTLY in this format:

SKILL SCORES
List each skill with score out of 10 in a table format

SKILL GAPS
List the gaps as bullet points

LEARNING PLAN
For each gap provide:
- Resource name and link
- Time estimate to learn

OVERALL MATCH SCORE
Give a score out of 100 with explanation

FINAL RECOMMENDATION
Give a clear hire or no hire recommendation with reason

Job Description:
{jd}

Resume:
{resume}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        result = clean_ai_output(response.choices[0].message.content)

    # ================= RESULTS =================
    st.markdown("## 📊 Analysis Dashboard")
    st.markdown("### 📄 AI Output")
    st.write(result)

    pdf_file = generate_pdf(result)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "📥 Download PDF Report",
            f,
            file_name="AI_Skill_Report.pdf",
            mime="application/pdf"
        )