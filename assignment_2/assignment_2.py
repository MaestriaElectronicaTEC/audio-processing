from scipy.signal import lfilter
from scipy.io.wavfile import read, write
from numpy import iinfo, zeros, append
from matplotlib.pyplot import xlabel, ylabel, xlim, ylim, figure, plot, show

# load the voice
(fv, voice) = read('sounds/2m1.wav')
voice = voice / iinfo(voice.dtype).max

# load the impulse
(fi, impulse) = read('sounds/impulse1.wav')
impulse = impulse / iinfo(impulse.dtype).max

# apply the impulse response
y, zf = lfilter(impulse, 1, voice, zi=zeros(len(impulse) - 1))
y = append(y, zf)

# save wav file
write("example.wav", fv, y)

# plot the signals
figure(1)
plot(voice)
figure(2)
plot(impulse)
figure(3)
plot(y)
show()