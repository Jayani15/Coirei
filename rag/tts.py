from gtts import gTTS
from playsound import playsound

def speak(text):

    tts = gTTS(text=text)

    tts.save("response.mp3")

    playsound("response.mp3")