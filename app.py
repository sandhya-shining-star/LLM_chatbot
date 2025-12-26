import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config
st.set_page_config(page_title="AI Tutor", page_icon="🎓")
st.title("🎓 AI Tutor for Freshers")

# 2. Get API Key safely - Changed key name to be specific to Gemini
try:
    # Make sure this matches exactly what you typed in Streamlit Secrets
    api_key = st.secrets["GEMINI_API_KEY"] 
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("Missing GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# 3. System Prompt
SYSTEM_PROMPT = "You are an AI tutor for freshers. Explain concepts step-by-step using simple language."

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input
if prompt := st.chat_input("Ask me anything about coding..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt, # The SDK handles strings, but ensure the model name is correct
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7 # Optional: adds more creativity to tutoring
                )
            )
            
            # Check if response has text (handles safety blocks)
            if response.text:
                output_text = response.text
                st.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            else:
                st.warning("The model did not return a response (it might have been filtered).")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
