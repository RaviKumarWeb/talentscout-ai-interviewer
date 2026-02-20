# TalentScout AI: Intelligent Hiring Assistant 🎯

## 📝 Project Overview
TalentScout AI is an intelligent screening chatbot developed for the fictional recruitment agency **"TalentScout."** The system is designed to streamline the early stages of recruitment by automating candidate information gathering and performing initial technical screenings. 

### Core Capabilities:
* **Automated Information Gathering**: Collects Name, Email, Phone, Experience, Location, and Tech Stack.
* **Dynamic Technical Screening**: Generates 3-5 tailored technical questions based on the candidate’s specific technologies.
* **Context-Aware Guardrails**: Stays strictly on-topic, refusing to answer non-recruitment queries (e.g., food, sports, or general advice).
* **Real-time Profile Extraction**: Uses a "Shadow Agent" to parse unstructured chat into structured data in the sidebar.

---

## 🏗️ Technical Details
### Architecture & Design Decisions
* **Modular Adapter Pattern**: The system is split into `main.py` (UI), `utils.py` (Logic/API), and `prompts.py` (Instructions). This ensures the code is maintainable and scalable.
* **Model-Agnostic Backend**: Implemented an LLM Adapter that allows switching between **Google Gemini** and **OpenAI GPT** with a single configuration change in `utils.py`.
* **Zero-Cost Implementation**: Developed using the **Google Gemini 1.5 Flash Free Tier**, making the application accessible for testing without incurring API costs.
* **In-Memory State Management**: Utilizes Streamlit `session_state` to store candidate data during the session, ensuring no permanent data footprint is left behind.



### Libraries & Tools
* **Streamlit**: For the clean, interactive frontend.
* **Google Generative AI SDK**: Primary LLM provider (Free Tier optimized).
* **OpenAI SDK**: Support for GPT models and OpenRouter.
* **Python-Dotenv**: For secure management of API keys.

---

## 🧠 Prompt Design
The "brain" of the chatbot relies on a sophisticated dual-prompt strategy:



1.  **The Interviewer Agent**: 
    * **Persona**: Senior Technical Recruiter.
    * **Strategy**: Uses "Missing Field Detection" to ask for data point-by-point rather than a robotic form.
    * **Adaptability**: Adjusts the difficulty of technical questions based on the candidate's declared "Years of Experience."

2.  **The Extraction Agent (Shadow Agent)**:
    * **Strategy**: Operates invisibly on every message to parse entities (Name, Email, Stack, etc.) into JSON.
    * **Sentiment Analysis**: (Bonus) Analyzes the candidate's tone (Confident, Professional, Nervous) to provide a "Candidate Vibe" metric in the UI.

---

## ⚙️ Installation Instructions
To run TalentScout AI locally, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/talentscout-ai.git](https://github.com/your-username/talentscout-ai.git)
    cd talentscout-ai
    ```

2.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment Variables**:
    Create a file named `.env` in the root folder. **You must provide your own API keys to test the application**:
    ```env
    GEMINI_API_KEY=your_gemini_key_here
    OPENAI_API_KEY=your_openai_key_here
    ```
    > **Note:** I used free Gemini API key at [Google AI Studio](https://aistudio.google.com/).

5.  **Run the App**:
    ```bash
    streamlit run main.py
    ```

---

## 📖 Usage Guide
1.  **Initiate**: The bot will greet you and explain its purpose.
2.  **Information Phase**: Reply naturally. You can give all info at once or one by one.
3.  **Technical Phase**: Once you declare your tech stack (e.g., "MERN Stack"), the bot will switch to technical screening mode.
4.  **Guardrail Check**: Try asking the bot a non-job question (e.g., "What's the weather?") to see the fallback mechanism in action.
5.  **Exit**: Type **"exit"**, **"quit"**, or **"bye"** to end the session gracefully.

---

## 🛡️ Data Handling & Privacy
* **GDPR Compliance**: All candidate data is handled in compliance with data privacy standards. No data is stored permanently.
* **Simulated Backend**: Data is stored in-memory. For demonstration, a "Download JSON" feature is provided to show how data would be prepared for a real backend.
* **PII Masking**: The sidebar extracts data but does not display full sensitive information in "Privacy Mode."

---

## ⚠️ Challenges & Solutions
* **Challenge**: LLMs often "hallucinate" or include conversational text when asked for JSON data.
    * **Solution**: Implemented a **JSON Response Healing** function that strips markdown markers and ensures valid parsing.
* **Challenge**: Managing API Rate Limits on the Free Tier.
    * **Solution**: Integrated **Resource Caching** using `@st.cache_resource` and error handling to ensure a smooth user experience even when limits are reached.
* **Challenge**: Maintaining context across multiple questions.
    * **Solution**: Designed a rolling history window that passes the entire conversation context to the LLM for every turn.