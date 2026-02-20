import streamlit as st
import json
from utils import call_llm, extract_candidate_json
from prompts import get_interviewer_prompt

st.set_page_config(page_title="TalentScout AI", page_icon="🎯", layout="wide")

# --- CUSTOM UI ---
st.markdown("""<style>.stChatMessage { border-radius: 10px; }</style>""", unsafe_allow_html=True)

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
    st.title("📋 Profile Progress")
    st.caption("Auto-extracted by AI")
    for field, value in st.session_state.candidate_data.items():
        if field == "Sentiment": continue
        st.write(f"{'✅' if value else '⏳'} **{field}:** {value if value else 'Pending...'}")
    
    if st.session_state.candidate_data.get("Sentiment"):
        st.divider()
        st.metric("Detected Vibe", st.session_state.candidate_data["Sentiment"])

# --- CHAT INTERFACE ---
st.title("🤖 Hiring Assistant")

if not st.session_state.messages:
    greeting = "👋 Hello! I'm the TalentScout Assistant. To start, could you tell me your **Name** and the **Position** you are interested in?"
    st.session_state.messages.append({"role": "assistant", "content": greeting})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if st.session_state.interview_active:
    if user_input := st.chat_input("Reply to the assistant..."):
        # Handle Exit
        if any(w in user_input.lower() for w in ["exit", "quit", "bye"]):
            st.session_state.interview_active = False
            st.rerun()

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(user_input)

        # Process with AI
        with st.spinner("Analyzing..."):
            # Update Data in Background
            new_info = extract_candidate_json(st.session_state.messages)
            if new_info:
                for k, v in new_info.items():
                    if v: st.session_state.candidate_data[k] = v

            # Generate Response
            sys_instr = get_interviewer_prompt(st.session_state.candidate_data)
            ai_reply = call_llm(sys_instr, str(st.session_state.messages))
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
else:
    st.success("✅ Application Submitted. We will be in touch!")