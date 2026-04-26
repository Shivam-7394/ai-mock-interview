import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_questions(resume_text):
    try:
        prompt = f"""
Generate exactly 5 interview questions based on this resume.

Rules:
- Number them 1 to 5
- Do NOT add headings
- Keep them clear and professional

Resume:
{resume_text}
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


def evaluate_answer(question, answer):
    try:
        prompt = f"""
Evaluate the answer.

Give:
Score: X/10
Strengths (2 points)
Improvements (2 points)

Be fair (avoid extreme scoring).

Question: {question}
Answer: {answer}
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
