from gtts import gTTS
import os
def response_text_to_speech(text, filename):
    """Convert response text to speech and save it as an audio file.
    
    Args:
        text (str): The text to convert into speech.
        filename (str): The path where the audio file will be saved.
    """
    #Save audio to a directory
    UPLOAD_DIR = "audio"
    # Initialize the gTTS object with the given text and language
    tts = gTTS(text=text, lang='ur')
    
    # Save the generated speech to the specified file
    tts.save(os.path.join(UPLOAD_DIR, filename))
