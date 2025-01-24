import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import os
from utils import prompt_process

# Model setups
_ = load_dotenv(find_dotenv()) # read local .env file
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model_name = "gemini-1.5-flash" # gemini-1.5-flash, gemini-1.5-flash-8b

prompt_obj = prompt_process(file_path = 'data/250120_preprocessed_prompts.xlsx')
prompt_obj.load_prompt()
prompt = prompt_obj.get_prompt(prompt_id = 0)

model = genai.GenerativeModel(model_name = model_name, 
                              system_instruction=prompt)
chat = model.start_chat(
    history=[]
)

# Streamed response emulator
def response_generator(chat, prompt):
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        yield chunk.text + " "
        # time.sleep(0.05)

# Streamlit app
st.title(f"Chat with `{model_name}`")

# Add a text box that can be miniminzed for showing the prompt
with st.expander("Prompt"):
    st.write(prompt)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(chat, prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})