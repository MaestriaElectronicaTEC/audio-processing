import samplerate
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.signal import butter, filtfilt, resample

A_c = 1
f_c = 870000

(fm,modulator) = read('../assignment_1/sounds/5w1.wav')
modulator = modulator / np.iinfo(modulator.dtype).max

fs = 4000000
T_old = 1 / fm
N_old = len(modulator)
T_new = 1 / fs
N_new = int(T_old/T_new) * len(modulator)

#ratio = 250
#converter = 'sinc_best'
#modulator = samplerate.resample(modulator, ratio, converter)
modulator = resample(modulator, N_new)

t = np.linspace(0, len(modulator), len(modulator))
carrier = A_c*np.cos(2*np.pi*(f_c/fs)*t)

# Modulation
product = carrier * modulator

# Demodulation
original = product * carrier

# Filter requirements.
fs = 4000000    # sample rate, Hz
cutoff = 8000   # desired cutoff frequency of the filter, Hz
nyq = 0.5 * fs  # Nyquist Frequency
order = 2       # sin wave can be approx represented as quadratic

normal_cutoff = cutoff / nyq
b, a = butter(order, normal_cutoff, btype='low', analog=False)
riginal = filtfilt(b, a, original)
original = resample(original, N_old)

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
write("dem.wav", fm, original)

#plt.magnitude_spectrum(original,Fs=4000000)
#plt.show()