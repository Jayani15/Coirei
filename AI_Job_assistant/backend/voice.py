def speech_to_text(audio):

    """
    Convert speech into text using
    Whisper or another STT model.
    """

    # Add Whisper implementation here

    return "Transcribed text"


def text_to_speech(text):

    """
    Convert AI response into speech using
    Kokoro, Piper, XTTS, etc.
    """

    # Add TTS implementation here

    return "audio_file_path"


def voice_chat(audio, user_id):

    # Speech → Text
    text = speech_to_text(audio)

    return text