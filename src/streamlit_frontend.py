import streamlit as st
import requests
# import json
import os

from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
APP_PASSWORD = os.getenv("APP_PASSWORD", "demo123")  # Set this in secrets

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    """Password check function"""    
    if not st.session_state.authenticated:
        st.title("🔒 Assessment Grading System")
        st.markdown("Please enter the password to access the application")

        st.info("""
        🔑 This is a portfolio demonstration project.  
        💼 **Recruiters:** Please email me for the access password.  
        
        *Note: Your browser may suggest saving this password - you can safely ignore this prompt.*
        """)

        with st.form("access_form", clear_on_submit=True):
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter demo password"
            )
            submitted = st.form_submit_button(
                "Access Demo", 
                use_container_width=True,
            )

            if submitted:
                if password == APP_PASSWORD:
                    st.session_state.authenticated = True
                    st.success("✅ Access granted!")
                    st.rerun()
                else:
                    st.error(f"❌ Incorrect password. Please contact me for access.")

        st.stop()

check_password()

# Logout button in sidebar
with st.sidebar:
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.set_page_config(page_title="AI Grading System", page_icon="🎓", layout="wide")

st.title("🎓 AI Assessment Grading System")
st.markdown("Automated grading powered by LLMs")

# Load questions
@st.cache_data
def load_questions():
    response = requests.get(f"{API_URL}/api/questions")
    return response.json()

try:
    questions = load_questions()
    
    # Question selection
    question_options = {f"{q['subject']}, {q['topic']} - {q['question'][:50]}...": q for q in questions}
    selected_label = st.selectbox("Select a question:", list(question_options.keys()))
    selected_question = question_options[selected_label]
    
    # Display question
    # st.info(f"**Question ({selected_question['marks']} marks):** {selected_question['text']}")
    st.info(f"**Question:** {selected_question['question']}")
    
    # Answer input
    answer_text = st.text_area(
        "Your Answer:",
        height=200,
        placeholder="Type your answer here..."
    )
    
    # Grade button
    if st.button("Grade Answer", type="primary"):
        if not answer_text.strip():
            st.error("Please enter an answer")
        else:
            with st.spinner("Grading your answer..."):
                response = requests.post(
                    f"{API_URL}/api/grade",
                    json={
                        "question_text": selected_question['question'],
                        "answer_text": answer_text
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # # Display results
                    # col1, col2 = st.columns([2, 1])
                    
                    # with col1:
                    #     st.success(f"**Total Score: {result['total_score']} / {result['total_possible']}**")
                    
                    # with col2:
                    #     confidence_color = {
                    #         "high": "🟢",
                    #         "medium": "🟡",
                    #         "low": "🔴"
                    #     }
                    #     st.metric("Confidence", f"{confidence_color.get(result['confidence'], '')} {result['confidence'].upper()}")
                    
                    # Criterion breakdown
                    st.subheader("Criterion Breakdown")
                    for criterion in result['scores_by_criteria']:
                        # with st.expander(f"{criterion['criterion']}: {criterion['assigned_score']}/{criterion['max_score']}"):
                        with st.expander(f"{criterion['criterion']}: {criterion['assigned_score']}"):
                            st.write(criterion['justification'])
                    
                    # # Feedback
                    # st.subheader("Feedback")
                    # st.info(result['feedback'])
                else:
                    st.error("Grading failed. Please try again.")
    
except Exception as e:
    st.error(f"Error connecting to API: {e}")
    st.info("Make sure the FastAPI server is running at http://localhost:8000")