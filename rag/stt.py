import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

model = WhisperModel("base")

def record_audio(filename="input.wav", duration=5):

    fs = 16000

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, fs, recording)

    return filename


def speech_to_text(audio_file):

    segments, _ = model.transcribe(audio_file)

    text = ""

    for segment in segments:
        text += segment.text

    return text