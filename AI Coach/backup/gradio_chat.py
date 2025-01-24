import gradio as gr
import openai
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.Client()

def chat_with_gpt(user_input, chat_history=[]):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for user_msg, bot_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    bot_response = response.choices[0].message.content
    # chat_history.append((user_input, bot_response))
    return {"role": "system", "content": bot_response}

chatbot_ui = gr.ChatInterface(fn=chat_with_gpt, title="ChatGPT Bot", description="Ask me anything!")

# Launch with a public link
chatbot_ui.launch(share=True)