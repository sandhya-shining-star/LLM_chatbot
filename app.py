import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config
st.set_page_config(page_title="AI Tutor", page_icon="🎓")
st.title("🎓 AI Tutor for Freshers")

# 2. Get API Key safely from Streamlit Secrets
# (We will set this up in the Streamlit Cloud dashboard later)
try:
    api_key = st.secrets["openai_API_Key"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Please set the GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# 3. System Prompt
SYSTEM_PROMPT = "You are an AI tutor for freshers. Explain concepts step-by-step using simple language."

# 4. Initialize Chat History (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input
if prompt := st.chat_input("Ask me anything about coding..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
        )
        st.markdown(response.text)

        st.session_state.messages.append({"role": "assistant", "content": response.text})
