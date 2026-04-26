from tts_utils import speak_text
import streamlit as st
import time
import re
import pandas as pd

from resume_parser import extract_text
from llm import generate_questions, evaluate_answer

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI Mock Interview", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #f1f5f9;
}
h1 {
    text-align: center;
    color: #38bdf8;
}
.question-box {
    background: #1e293b;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 12px;
}
.stButton > button {
    background: #38bdf8;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TYPEWRITER ----------------
def typewriter(text, speed=0.01):
    placeholder = st.empty()
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(f"**{typed}**")
        time.sleep(speed)

# ---------------- CONFIDENCE ----------------
def confidence_score(answer):
    length = len(answer.split())
    if length < 5:
        return "Low 😐"
    elif length < 15:
        return "Medium 🙂"
    else:
        return "High 💪"

# ---------------- EMOTION ----------------
def detect_emotion(text):
    words = len(text.split())
    if words < 5:
        return "😐 Nervous"
    elif words < 15:
        return "🙂 Neutral"
    elif words < 30:
        return "😊 Confident"
    else:
        return "🔥 Very Confident"

def emotion_meter(emotion):
    if "Nervous" in emotion:
        st.progress(0.3)
    elif "Neutral" in emotion:
        st.progress(0.5)
    elif "Confident" in emotion:
        st.progress(0.7)
    else:
        st.progress(0.9)

def avatar_reaction(score):
    if score < 4:
        st.image("https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif")
    elif score < 7:
        st.image("https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif")
    else:
        st.image("https://media.giphy.com/media/111ebonMs90YLu/giphy.gif")

# ---------------- AI SUMMARY ----------------
def generate_summary(questions, answers, scores):
    combined = ""

    for i in answers:
        combined += f"Q{i+1}: {questions[i]}\n"
        combined += f"A{i+1}: {answers[i]}\n"
        combined += f"Score: {scores.get(i, '')}/10\n\n"

    prompt = f"""
    Analyze this interview and give:
    1. Strengths
    2. Weaknesses
    3. Improvement tips

    {combined}
    """

    return evaluate_answer("summary", prompt)

# ---------------- HEADER ----------------
st.markdown("<h1>🎤 AI Mock Interview</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Practice. Improve. Crack Interviews 🚀</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📊 Live Score")

    if st.session_state.get("scores"):
        scores = list(st.session_state.scores.values())
        avg = sum(scores) / len(scores)
        st.metric("Average", f"{avg:.1f}/10")
        st.progress(avg / 10)

    st.markdown("---")
    st.title("⚙️ Tips")
    st.write("- Speak clearly")
    st.write("- Be confident")
    st.write("- Use real examples")

# ---------------- SESSION ----------------
if "questions" not in st.session_state:
    st.session_state.questions = []

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "answers" not in st.session_state:
    st.session_state.answers = {}

# ---------------- RESET ----------------
if st.button("🔄 Reset"):
    st.session_state.clear()
    st.rerun()

# =========================
# 📝 TEXT INTERVIEW ONLY
# =========================

file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if file:
    resume_text = extract_text(file)
    st.success("Resume uploaded!")

    if st.button("Generate Questions"):

        q_text = generate_questions(resume_text)
        questions = [q.strip() for q in q_text.split("\n") if q.strip()]

        st.session_state.questions = questions
        st.session_state.scores = {}
        st.session_state.answers = {}

if st.session_state.questions:

    for i, q in enumerate(st.session_state.questions[:5]):

        st.markdown(f"<div class='question-box'><b>Q{i+1}:</b> {q}</div>", unsafe_allow_html=True)

        ans = st.text_input(f"Answer {i+1}", key=f"text_{i}")

        if st.button(f"Evaluate {i+1}"):

            st.session_state.answers[i] = ans

            feedback = evaluate_answer(q, ans)
            st.info(feedback)

            conf = confidence_score(ans)
            emotion = detect_emotion(ans)

            st.info(f"Confidence: {conf}")
            st.info(f"Emotion: {emotion}")
            emotion_meter(emotion)

            match = re.search(r'\b(10|[0-9])\b', feedback)
            if match:
                score = int(match.group())
                st.session_state.scores[i] = score
                avatar_reaction(score)

# =========================
# 📊 DASHBOARD
# =========================
if st.session_state.scores:

    st.markdown("## 📊 Performance Dashboard")

    scores = list(st.session_state.scores.values())
    avg = sum(scores) / len(scores)

    st.metric("Average Score", f"{avg:.1f}/10")
    st.line_chart(scores)

    if avg < 4:
        st.error("⚠️ Weak Areas: Communication + Structure")
    elif avg < 7:
        st.warning("⚠️ Improve clarity and depth")
    else:
        st.success("✅ Strong performance overall")

    if st.button("🧠 Generate AI Summary"):

        summary = generate_summary(
            st.session_state.questions,
            st.session_state.answers,
            st.session_state.scores
        )

        st.success("📋 AI Summary")
        st.write(summary)

        report = f"AI MOCK INTERVIEW REPORT\n\nAverage Score: {avg:.1f}/10\n\n"

        for i in st.session_state.answers:
            report += f"""
Q{i+1}: {st.session_state.questions[i]}
Answer: {st.session_state.answers[i]}
Score: {st.session_state.scores.get(i, 'N/A')}/10
"""

        report += f"\n\nSUMMARY:\n{summary}"

        st.download_button(
            "📥 Download Report",
            report,
            file_name="interview_report.txt"
        )
