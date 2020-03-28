import sys
import argparse
import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt, resample, lfilter, sawtooth, stft, welch, boxcar
from scipy.io.wavfile import read, write
import numpy as np
from numpy import iinfo, zeros, append

#----------------------------------------------------------------------------

RECTANGULAR = 0
HANNING = 1
HAMMING = 2

#----------------------------------------------------------------------------

def _openWavFile(filename):
    (fm,s) = read(filename)
    s = s / iinfo(s.dtype).max
    return (fm, s)

def _generateSawtooth(f, fs, M=10):
    # 0.032
    dt = 1/fs
    N = int(M/dt)
    t = np.arange(N)*dt
    s = sawtooth(2 * np.pi * f * t)  + 1
    plt.plot(t, s)
    plt.show()
    return s

def _generateWindow(fs, M, winType=RECTANGULAR):
    winSize = int(M)
    if (winType is RECTANGULAR):
        print('Rectangular window')
        w = boxcar(winSize)
        return w
    if (winType is HAMMING):
        print('Hamming window')
        w = np.hamming(winSize)
        return w
    if (winType is HANNING):
        print('Hanning window')
        w = np.hanning(winSize)
        return w

def _shortTimeFourierTransform(s, w, fs):
    #f, Pxx_spec = welch(s, fs, nperseg=len(w), window=w, scaling='spectrum')
    f, Pxx_spec = welch(s, fs, nperseg=len(w), window=w)
    plt.plot(f, Pxx_spec / np.amax(Pxx_spec))
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD')
    plt.show()

#----------------------------------------------------------------------------

def sawtoothWindowAnalysis(f, M, winType=RECTANGULAR):
    fs = 44100
    # get the sawtooth signal
    s = _generateSawtooth(f, fs)

    # get the window
    w = _generateWindow(fs, M, winType)

    # compute the short time Fourier transform
    _shortTimeFourierTransform(s, w, fs)

def audioWindowAnalysis(filename, M, winType=RECTANGULAR):
    # load the wav file
    fs, s = _openWavFile(filename)

    # get the window
    w = _generateWindow(fs, M, winType)

    # compute the short time Fourier transform
    _shortTimeFourierTransform(s, w, fs)

#----------------------------------------------------------------------------

def cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Assignment 3 of the Audio Processing course.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'sawtoothWindowAnalysis',       'Window analysis of the Sawtooth signal')
    p.add_argument(     '--f',                          help='Frecuency of the Sawthooth signal', type=float, default=5)
    p.add_argument(     '--M',                          help='Lenght in milliseconds of the window', type=float, default=100)
    p.add_argument(     '--winType',                    help='Window type: 0 - Rectangular, 1 - Hanning, 2 - Hamming', type=int, default=RECTANGULAR)

    p = add_command(    'audioWindowAnalysis',          'Window analysis of a WAV file')
    p.add_argument(     '--filename',                   help='Path of the WAV file', default='')
    p.add_argument(     '--M',                          help='Lenght in milliseconds of the window', type=float, default=100)
    p.add_argument(     '--winType',                    help='Window type: 0 - Rectangular, 1 - Hanning, 2 - Hamming', type=int, default=RECTANGULAR)

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    cmdline(sys.argv)

#----------------------------------------------------------------------------
