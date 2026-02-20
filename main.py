import streamlit as st
import json
from utils import call_llm, extract_candidate_json
from prompts import get_interviewer_prompt

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TalentScout AI | Hiring Assistant", 
    page_icon="🎯", 
    layout="wide"
)

# --- ADVANCED UI STYLING (The "Wow" Factor) ---
st.markdown("""
    <style>
    /* Professional Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E2E; /* Deep Charcoal Blue */
        color: #FFFFFF;
        border-right: 1px solid #313244;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #89B4FA !important; /* Soft Blue Accents */
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #CDD6F4 !important; /* Off-white text for readability */
    }
    
    /* Chat Bubble Styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Professional Vibe Metric */
    [data-testid="stMetricValue"] {
        color: #A6E3A1 !important; /* Success Green */
        font-weight: bold;
    }
    
    /* Custom Button */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #45475A;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #89B4FA;
        color: #1E1E2E;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.candidate_data = {
        "Name": None, "Email": None, "Phone": None, 
        "Exp": None, "Position": None, "Location": None, "Stack": None, "Sentiment": None
    }
    st.session_state.interview_active = True

# --- SIDEBAR: PROGRESS TRACKER ---
with st.sidebar:
    st.title("📋 Candidate Profile")
    st.caption("AI-Powered Live Extraction")
    
    st.divider()
    
    # High-Contrast Data Tracking
    for field, value in st.session_state.candidate_data.items():
        if field == "Sentiment": continue
        if value:
            st.markdown(f"✅ **{field}:** <span style='color: #A6E3A1;'>{value}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"⏳ **{field}:** <span style='color: #F38BA8;'>Pending...</span>", unsafe_allow_html=True)
    
    # Sentiment Enhancement
    if st.session_state.candidate_data.get("Sentiment"):
        st.divider()
        st.metric("Detected Vibe", st.session_state.candidate_data["Sentiment"])

    # Data Export Button
    st.divider()
    if st.button("📥 Generate Candidate JSON"):
        data_str = json.dumps(st.session_state.candidate_data, indent=4)
        st.download_button(
            label="Download Data",
            data=data_str,
            file_name=f"candidate_{st.session_state.candidate_data['Name'] or 'profile'}.json",
            mime="application/json"
        )
    st.caption("GDPR: Data is processed in-memory.")

# --- MAIN CHAT ---
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("---")

if not st.session_state.messages:
    greet = "👋 Welcome to TalentScout! I'm your AI recruiter. To begin, please share your **Name** and the **Position** you're applying for."
    st.session_state.messages.append({"role": "assistant", "content": greet})

# History Rendering
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Interview Process
if st.session_state.interview_active:
    if prompt := st.chat_input("Reply to the assistant..."):
        
        # Graceful Exit
        if any(w in prompt.lower() for w in ["exit", "quit", "bye"]):
            st.session_state.interview_active = False
            st.rerun()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.spinner("Analyzing response..."):
            # Update Profile in Background
            new_data = extract_candidate_json(st.session_state.messages)
            if new_data:
                for k, v in new_data.items():
                    if v: st.session_state.candidate_data[k] = v

            # Generate Interview Response
            sys_instr = get_interviewer_prompt(st.session_state.candidate_data)
            response = call_llm(sys_instr, str(st.session_state.messages))
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
else:
    st.success("✅ Application successfully submitted. Thank you!")