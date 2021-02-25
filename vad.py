"""A class to detect voice activity
When executed directly, records duration seconds of audio, plays it back
and then plays the voice activity detected"""
import numpy as np
import sounddevice as sd


class VoiceActivityDetector(object):
    def __init__(self, energy_primthreshold=40, f_primthreshold=185, sf_primthreshold=5):
        self.frame_size = 10
        self.energy_primthreshold = energy_primthreshold
        self.f_primthreshold = f_primthreshold
        self.sf_primthreshold = sf_primthreshold
        # we intantiate lists to keep track of the audio arrays received
        self.energy = []
        self.f = []
        self.sf = []
        self.is_audio_speech = []
        self.silence_count = 0

    def frame_energy(self, frame):
        """Returns the noramlized energy of an audio array"""
        return np.sqrt((np.sum(frame**2)/len(frame)))

    def fft_frame(self, frame):
        """Returns the fast Fourier transform of an array"""
        return np.fft.fft(frame)

    def detect_voice_activity(self, audio_array):
        num_frames = len(audio_array)
        print("num frames", num_frames)
        for i in range(num_frames):
            self.energy.append(self.frame_energy(audio_array[i]))
            fft = self.fft_frame(audio_array[i])
            self.f.append(max(fft))
            arithmetic_mean, geometric_mean = np.mean(
                fft), np.exp(np.log(fft).mean())
            self.sf.append(10*np.log10(arithmetic_mean/geometric_mean))
            if i == 30:  # we assume at least the first 30 audio arrays are silence
                min_e = min(self.energy)
                self.silence_count = 30
            elif i > 30:
                thresh_e = self.energy_primthreshold*np.log(min_e)
                thresh_f = self.f_primthreshold
                thresh_sf = self.sf_primthreshold
                counter = 0
                if self.energy[-1] >= thresh_e:
                    counter += 1
                if self.f[-1] >= thresh_f:
                    counter += 1
                if self.sf[-1] >= thresh_sf:
                    counter += 1
                speech = counter > 1
                self.is_audio_speech.append(speech)
                if not speech:
                    min_e = (self.silence_count*min_e +
                             self.energy[-1])/(self.silence_count + 1)
                    self.silence_count += 1
                thresh_e = self.energy_primthreshold*np.log(min_e)
        arrays_to_return = []
        for i, is_speech in enumerate(self.is_audio_speech):
            if is_speech:
                arrays_to_return += list(audio_array[i])
        return np.array(arrays_to_return)

def split_audio_array(audio_array, array_duration, chunk_duration):
    """Given an audio array, its duration (in seconds) and a chunk length,
    Returns a splitted array with chunks of the provided duration.
    It can also use only the first channel on a dual array"""
    if np.shape(audio_array)[1] == 2:
        audio_array = audio_array[:,0]
    return np.split(audio_array, len(audio_array)*chunk_duration/(array_duration*1000))


if __name__ == '__main__':
    print(sd.query_devices())
    sd.check_input_settings()
    rec_rate = 44000
    duration = 5
    recording = sd.rec(duration*rec_rate, channels=2)
    sd.wait()
    sd.play(recording[:, 0])
    sd.wait()
    vad = VoiceActivityDetector()
    output = vad.detect_voice_activity(split_audio_array(recording, duration, 10))
    sd.play(output)
    sd.wait()
