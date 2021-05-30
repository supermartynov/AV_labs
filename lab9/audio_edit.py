from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy import signal

AudioName = 'clearPiano.wav'

song = AudioSegment.from_file(AudioName)
song = song.set_channels(1)


fs, m = wavfile.read(AudioName)
Audiodata = np.array(song.get_array_of_samples())


N = 1024*2  # Number of point in the fft
f, t, Sxx = signal.spectrogram(Audiodata, fs, window=signal.windows.hann(N), nfft=N)
plt.figure()
#plt.pcolormesh(t, f, 20 * np.log10(Sxx))
plt.pcolormesh(t, f[:128*2], 20*np.log10(Sxx[:128*2])) # dB spectrogram
#plt.yticks(np.arange(0, 5000, 200))
#plt.pcolormesh(t, f,Sxx) # Lineal spectrogram
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram', size=16)
plt.savefig('spectrogrammBas')
plt.show()
