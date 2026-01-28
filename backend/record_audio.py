import sounddevice as sd
from scipy.io.wavfile import write

def record_voice(filename="input.wav", duration=15):
    fs = 44100
    print("Recording... Speak clearly")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("Saved:", filename)

if __name__ == "__main__":
    record_voice()
