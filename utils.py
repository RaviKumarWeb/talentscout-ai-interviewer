import streamlit as st
import json
import os
import google.generativeai as genai
import openai
from dotenv import load_dotenv

load_dotenv()

# --- PROVIDER CONFIGURATION ---
# Toggle between "GEMINI" or "OPENAI" here.
PROVIDER = "GEMINI" 

def call_llm(system_instruction, user_content):
    """Routes requests to the chosen provider."""
    if PROVIDER == "GEMINI":
        return _call_gemini(system_instruction, user_content)
    elif PROVIDER == "OPENAI":
        return _call_openai(system_instruction, user_content)
    return "Error: Unsupported Provider"

def _call_gemini(sys_instr, user_msg):
    """Gemini-specific implementation using google-generativeai."""
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Using the latest 2026 stable identifier
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(f"{sys_instr}\n\nUser: {user_msg}")
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

def _call_openai(sys_instr, user_msg):
    """OpenAI-specific implementation using the openai SDK."""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o", # Recommended for professional screening logic
            messages=[
                {"role": "system", "content": sys_instr},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {str(e)}"

def extract_candidate_json(messages):
    """Shadow agent for real-time entity extraction."""
    from prompts import PARSER_PROMPT
    if not messages: return None
    
    ai_response = call_llm(PARSER_PROMPT, str(messages))
    try:
        # Removes markdown artifacts if the AI includes them
        clean_json = ai_response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except:
        return None
