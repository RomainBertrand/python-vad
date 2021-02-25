"""Module to test many parameters on the VoiceActivityDetector, writing the results in a csv file"""
from scipy.io.wavfile import read
import sounddevice as sd

from vad import VoiceActivityDetector, split_audio_array

def test_vad(record, energy, f, sf):
    vad = VoiceActivityDetector(energy, f, f)
    return vad.detect_voice_activity(record)

def main(oneshot=True):
    duration = 10
    chunk_duration = 10
    splitted_audio_array = split_audio_array(recording, duration, chunk_duration)
    if oneshot:
        output = test_vad(splitted_audio_array, 0, 20, 0)
        sd.play(output)
        sd.wait()
    else:
        with open("results.csv", 'w') as csv_file:
            for energy in range(0, 200, 10):
                for f in range(0, 100, 20):
                    for sf in range(0, 20):
                        output = test_vad(splitted_audio_array, energy, f, sf)
                        csv_file.writelines(
                            str(energy)+","+str(f)+","+str(sf)+","+str(len(output))+'\n')

if __name__ == '__main__':
    fs, recording = read('output.wav')
    main()
