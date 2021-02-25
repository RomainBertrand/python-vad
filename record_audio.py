"""Simple file to write an audio file"""
import sounddevice as sd
from scipy.io.wavfile import write

if __name__ == '__main__':
    duration = 10  # in seconds
    framerate = 44000
    recording = sd.rec(duration*framerate, channels=2)
    sd.wait()
    write("output.wav", framerate, recording[:, 0]) # to get only one channel
