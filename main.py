import os 
import dotenv
import streamlit as st
from audio_processing import record_audio, convert_audio_to_text
from tts import response_text_to_speech
from chatbot import get_response

# # Load environment variables from the .env file
# dotenv.load_dotenv()

# Retrieve API key from environment variables
api_key = st.secrets["api"]["GORQ_API_KEY"]

# Check if the API key is available
if api_key:
    print("API Key found")
else:
    raise Exception("API Key not found")

# Initialize session state variables if they do not already exist
if "messages" not in st.session_state:
    # List to hold chat messages and their audio files
    st.session_state.messages = []

if "next_query" not in st.session_state:
    # make the session state for exception handling
    st.session_state.next_query = False

if "chat_count" not in st.session_state:
    # Counter to track the number of chats
    st.session_state.chat_count = 0


def chat():
    # Increment the chat count to get a unique identifier for this chat session
    chat_number = st.session_state.chat_count + 1

    # Generate a filename for the recorded audio based on the chat number
    filename = f"audio_{chat_number}.mp3"
    # Audio directory
    UPLOAD_DIR = "audio"

    # Record audio from the microphone and save it as a WAV file
    record_audio(filename, duration=20)
    
    # Show a processing message while the audio is being processed
    st.info("Processing... ⏳")

    # Convert the recorded audio to text
    user_text = convert_audio_to_text(filename)
    
    if user_text:
        # Show a spinner while the AI is generating a response
        with st.spinner("Thinking... 🤔"):
            # Get the AI's response based on the user's text
            ai_response = get_response(user_text, api_key)
            
            # Generate a filename for the AI's response audio
            response_filename = f"response_{chat_number}.mp3"
            
            # Convert the AI's response text to speech and save it to the specified file
            response_text_to_speech(ai_response, response_filename)
            
            # Add the user's message and the AI's response to the session state messages
            st.session_state.messages.append((f"Chat {chat_number} - 👤 User", os.path.join(UPLOAD_DIR, filename)))
            st.session_state.messages.append((f"Chat {chat_number} - 🤖 AI", os.path.join(UPLOAD_DIR,response_filename)))
            
            # Display the most recent user and AI messages with their corresponding audio files
            if st.session_state.messages:
                # Display the last user message
                speaker, audio_file = st.session_state.messages[-2]
                st.write(f"{speaker} Message")
                st.audio(audio_file)

                # Display the last AI response
                speaker, audio_file = st.session_state.messages[-1]
                st.write(f"{speaker} Message")
                st.audio(audio_file)
            
            # Update the chat count and set the flag to show the next query button
            st.session_state.chat_count = chat_number
            st.session_state.show_next_query = True


def main():
    # Set the title of the Streamlit app
    st.title("🎙️ Welcome to Voice Chatbot")

    # Create buttons in the sidebar for user interactions
    start_chat_button = st.sidebar.button("Start chatting")
    next_query_button = st.sidebar.button("Next Query")
    show_previous_chat_button = st.sidebar.button("Show Previous Chats")
    exit_button = st.sidebar.button("End chat")

    # Handle the action when the "Start chatting" button is clicked
    if start_chat_button:
        # Check if the next query button has been shown
        if not st.session_state.next_query:
            chat()
        else:
            st.info("The chat will be started for the next query; click on the 'Next Query' button")

    # Handle the action when the "Next Query" button is clicked
    if next_query_button:
        # Check if the next query button has been shown
        if st.session_state.next_query:
            chat() 
        else:
            st.info("Please click 'Start chatting' to initiate the chat process.")

    # Handle the action when the "Show Previous Chats" button is clicked
    if show_previous_chat_button:
        # Check if there are any messages in the session state
        if st.session_state.messages:
            st.header("**Previous Chats:**")  
            # Iterate over the stored messages and display them
            for i, (speaker, audio_file) in enumerate(st.session_state.messages):
                st.write(f"{speaker} Message") 
                st.audio(audio_file) 
        else:
            st.info("Please click 'Start chatting' to initiate the chat process.")

    # Handle the action when the "End chat" button is clicked
    if exit_button:
        # Clear the session state to reset the app's state
        st.session_state.clear()

        # Refresh the page to simulate a restart of the app
        st.rerun()

if __name__ == "__main__":
    # Execute the main function if this script is run directly
    main()
