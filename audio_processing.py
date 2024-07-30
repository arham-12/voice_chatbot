import speech_recognition as sr
import streamlit as st
import os

# Create an audio directory if it doesn't exist
UPLOAD_DIR = "audio"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def record_audio(filename, duration=20):
    """
    Record audio from the microphone and save it as a WAV file.

    Args:
        filename (str): Path where the recorded audio file will be saved.
        duration (int): Maximum duration (in seconds) to record audio. Default is 20 seconds.
    """
    # Create an instance of the Recognizer class
    recognizer = sr.Recognizer()
    
    # Create an instance of the Microphone class
    mic = sr.Microphone()

    # Open the microphone and start recording
    with mic as source:
        # Adjust for ambient noise to improve accuracy
        recognizer.adjust_for_ambient_noise(source)
        st.info("Listening... 🎙️")
        
        # Record audio from the microphone with a specified timeout
        audio = recognizer.listen(source, timeout=duration)
        
        # Save the recorded audio data to a directory
        filename = f"{UPLOAD_DIR}/{filename}"
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
    



def convert_audio_to_text(filename, language="ur"):
    """
    Convert audio file to text using the specified language.

    Args:
        filename (str): Path to the audio file to be converted.
        language (str): Language code for the speech recognition (default is 'ur' for Urdu).

    Returns:
        str: The recognized text from the audio file.
    """

    # Create an instance of the Recognizer class
    recognizer = sr.Recognizer()
    
    # Load the audio file
    audio_file = sr.AudioFile(os.path.join(UPLOAD_DIR, filename))
    
    # Open and process the audio file
    with audio_file as source:
        # Record the audio data from the file
        audio = recognizer.record(source)
        
        try:
            # Recognize the text from the audio using Google's speech recognition service
            text = recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            # Handle the case where the speech recognition could not understand the audio
            st.error("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            # Handle the case where there was an error with the request to the speech recognition service
            st.error(f"Could not request results from Google Speech Recognition service; {e}")