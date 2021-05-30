from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy import signal

AudioName = 'myVoice.wav'

song = AudioSegment.from_file(AudioName)
song = song.set_channels(1)


fs, m = wavfile.read(AudioName)
Audiodata = np.array(song.get_array_of_samples())

N = 1024*2  # Number of point in the fft
f, t, Sxx = signal.spectrogram(Audiodata, fs, window=signal.windows.hann(N), nfft=N)

Powers = []
maxPowers = []
views = np.array_split(Sxx, 3, axis=1)
for view in views:
    for i in range(len(view)):
        sum = view[i].sum()
        Powers.append(sum)
    maxPowers.append((np.max(Powers), np.argmax(Powers)))
    Powers = []
print(maxPowers)
for p in maxPowers:
    print("Max power:{}, f1: {}, f2: {}, f3: {}".format(
        p[0], f[p[1]], f[p[1] * 2], f[p[1] * 4]))



plt.figure()
#plt.pcolormesh(t, f, 20 * np.log10(Sxx))
plt.pcolormesh(t, f[:128*2], 20*np.log10(Sxx[:128*2]))
plt.yticks(np.arange(0, 5000, 256))
#plt.pcolormesh(t, f,Sxx) # Lineal spectrogram
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram', size=16)
plt.show()
