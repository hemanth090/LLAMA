import streamlit as st
import os
from groq import Groq

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def llma():
    client = Groq(
            api_key="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",
            )

    # Send the user's input to the chatbot
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama3-8b-8192",
    )
    
    # Get the bot's response
    bot_response = chat_completion.choices[0].message.content
    
    # Store the user input and bot response in the chat history
    st.session_state['chat_history'].append({"role": "you", "content": user_input})
    st.session_state['chat_history'].append({"role": "bot", "content": bot_response})
    
    # Display the bot's response with margin
    st.markdown("<div style='margin-top: 20px;'><strong>🤖 Bot</strong>: {}</div>".format(bot_response), unsafe_allow_html=True)

# UI for the chatbot
st.title("Chat-bot")

selected_model = st.selectbox("Select Model", ["LLMA"])
user_input = st.text_input("Enter your message")
submit = st.button("Submit")

if selected_model == "LLMA":
    if submit:
        llma()

# Add margin between the input and history
st.markdown("<hr style='margin-top: 40px;'>", unsafe_allow_html=True)

# Add "History" label in bold
st.markdown("<div style='margin-top: 10px;'><strong>History</strong></div>", unsafe_allow_html=True)

# Display chat history in "you" and "bot" format with emojis
if st.session_state['chat_history']:
    for message in st.session_state['chat_history']:
        if message["role"] == "you":
            st.markdown(f"<div style='margin-bottom: 10px;'><strong>🧑 You</strong>: {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='margin-bottom: 10px;'><strong>🤖 Bot</strong>: {message['content']}</div>", unsafe_allow_html=True)
