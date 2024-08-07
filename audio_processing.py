import sounddevice as sd
import numpy as np
import wavio
import streamlit as st
import os

# Create an audio directory if it doesn't exist
UPLOAD_DIR = "audio"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
def record_audio(filename, duration=20, samplerate=44100):
    """
    Record audio from the microphone and save it as a WAV file.

    Args:
        filename (str): Path where the recorded audio file will be saved.
        duration (int): Maximum duration (in seconds) to record audio. Default is 20 seconds.
        samplerate (int): Sample rate for the recording. Default is 44100 Hz.
    """
    # st.info("Recording... 🎙️")
    # Record audio from the microphone
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    
    # Save the recorded audio data to a directory
    filename = f"{UPLOAD_DIR}/{filename}"
    wavio.write(filename, audio, samplerate, sampwidth=2)
    # st.info("Recording complete.")
        
    



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