import streamlit as st
from groq import Groq

# Initialize session state for chat history and user input
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

def llma(user_input):
    client = Groq(
        api_key=st.secrets["groq"]["api_key"],  # Access the API key from secrets
    )

    try:
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

    except Exception as e:
        st.error(f"Error: {e}")

# UI for the chatbot
st.title("Chat-bot")

selected_model = st.selectbox("Select Model", ["LLMA"])
# Use the separate session state variable for user input
user_input = st.text_input("Enter your message", value=st.session_state['user_input'], key="input")  
submit = st.button("Submit")

if selected_model == "LLAMA":
    if submit and user_input:
        with st.spinner("Processing..."):
            llma(user_input)
            # Clear the input after submission by updating the session state variable
            st.session_state['user_input'] = ""  # Clear the input value

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
