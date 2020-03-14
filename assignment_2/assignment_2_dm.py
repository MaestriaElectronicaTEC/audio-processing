import samplerate
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import butter, filtfilt, resample

A_c = 1
f_c = 890000

(fm,modulator) = read('sounds/AM870,890,910.wav')
modulator = modulator / np.iinfo(modulator.dtype).max

t = np.linspace(0, len(modulator), len(modulator))
carrier = A_c*np.cos(2*np.pi*(f_c/fm)*t)

# Demodulation
original = modulator * carrier

# Filter requirements.
fs = 4000000    # sample rate, Hz
cutoff = 10000 # desired cutoff frequency of the filter, Hz
nyq = 0.5 * fm  # Nyquist Frequency
order = 2       # sin wave can be approx represented as quadratic

normal_cutoff = cutoff / nyq
b, a = butter(order, normal_cutoff, btype='low', analog=False)
original = filtfilt(b, a, original)

plt.subplot(3,1,1)
plt.title('Amplitude Modulation')
plt.plot(modulator,'g')
plt.ylabel('Amplitude')
plt.xlabel('Message signal')

plt.subplot(3,1,2)
plt.plot(carrier, 'r')
plt.ylabel('Amplitude')
plt.xlabel('Carrier signal')

plt.subplot(3,1,3)
plt.plot(original, color="purple")
plt.ylabel('Amplitude')
plt.xlabel('AM signal')

plt.subplots_adjust(hspace=1)
plt.rc('font', size=15)
fig = plt.gcf()
fig.set_size_inches(16, 9)
plt.show()

# save wav file
write("UCR.wav", fm, original)

plt.magnitude_spectrum(original,Fs=fm)
plt.show()