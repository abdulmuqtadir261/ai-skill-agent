🎯 AI Skill Intelligence Engine
An AI-powered skill assessment agent built for the Deccan AI Catalyst Hackathon.
🚀 What It Does

Takes a Job Description and Resume (PDF) as input
Analyzes the candidate's skills against job requirements
Scores each skill from 1-10
Identifies skill gaps
Creates a personalized learning plan with free resources
Gives an overall match score out of 100
Generates a downloadable PDF report

🛠️ Tools & Technologies Used

Groq API (LLaMA 3.1) - AI Brain
Streamlit - Web Interface
Python - Core Language
ReportLab - PDF Generation
PyPDF - Resume PDF Reading

⚙️ How To Run Locally
Step 1 - Clone the repo:
git clone https://github.com/abdulmuqtadir261/ai-skill-agent.git
Step 2 - Install requirements:
pip install streamlit groq pypdf reportlab
Step 3 - Add your Groq API key in app.py:
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
Step 4 - Run the app:
streamlit run app.py
📊 How It Works
User inputs Job Description + Resume PDF → AI reads and analyzes both → Scores each skill from 1 to 10 → Identifies skill gaps → Creates personalized learning plan → Generates PDF report
🏗️ Architecture

Frontend - Streamlit web interface
AI Engine - Groq API with LLaMA 3.1 model
PDF Parser - PyPDF extracts text from resume
Report Generator - ReportLab creates PDF output

📝 Sample Input
Job Description: Python Developer with Django, SQL, AWS experience
Resume: Any candidate resume in PDF format
✅ Sample Output

Skill scores table
Skill gaps analysis
Learning plan with resources and time estimates
Overall match score out of 100
Final hire/no hire recommendation

👨‍💻 Built By
Abdul Muqtadir - Deccan AI Catalyst Hackathon 2026
