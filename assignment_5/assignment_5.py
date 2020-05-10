import sys
import argparse

from math import ceil, log2, pi
from matplotlib.pyplot import figure, gca, grid, legend, plot, subplot, xlim, xlabel, ylabel, title, show, magnitude_spectrum
from numpy import absolute, arange, array, concatenate, iinfo, interp, sqrt, correlate, argmax, pad, amax
from numpy.linalg import norm
from scipy.io.wavfile import read
from scipy.signal import firwin2, freqz, lfilter

import numpy as np
import scipy as sp
import scipy.signal as sig
from scipy.fftpack import fft, fftfreq

#----------------------------------------------------------------------------

def loadWAV(filename):
    fm, s = read(filename)
    s = s / iinfo(s.dtype).max # Para que esté en el rango [-1,1], como en Matlab
    return (s, fm)

def windowing(s, N):
    # Partir en ventanas
    inicioVentanaCentral = round( len(s)/2 - N/2 )
    s = s[ inicioVentanaCentral : inicioVentanaCentral + N ]
    return s

def getACoefficient(fm, s):
    # Calcular coeficientes de prediccion lineal
    nCoefs = 1*round(fm/1000) # Regla del pulgar: num. de muestras en 1 ms
    return lpc_ref( s, nCoefs )

def plotFormants(fm, N, s, a):

    S = fft(s)
    freqs = fftfreq(len(s)) * fm
    S = np.abs(S)
    S = sqrt(S)
    S = S / norm(S)
    plot(freqs, S, label='$|S(f)|^{1/2}$')
    xlim( (0, 3000) )
    grid()

    b = outmidear(N,fm) # Oido disminuye efecto 1/f del espectro
    w, V = freqz( b, a )
    f = w/pi * fm/2 # Cambio de unidades: radianes por muestra a ciclos por seg. (Hz)
    V = absolute(V) # Nos interesa solo su amplitud
    RV = sqrt(V) # y aveces su raiz cuadrada
    NRV = RV / norm(RV) # normalizada
    plot( f, NRV, label='$|V(f)|^{1/2}$')
    xlim( (0, 3000) ) # Rango donde se encuentran los primeros dos formantes (F1 y F2)
    grid()
    xlabel('Frequency (Hz)')
    grid()

    legend()
    show()

def plotU(fm, s, a):
    u = lfilter( a, 1, s ) # convolucion de a y s
    t = arange(len(u)) / fm
    plot( 1000*t, u )
    xlim( (1000*t[0], 1000*t[-1]) )
    ylabel('$u(t)$') 
    xlabel('Time (ms)') 
    grid()
    show()

    return u

def plotAutocorrelation(fm, u):
    r = correlate( u, u, mode='full' )
    r = pad(r[argmax(r):-1], (0,1), 'constant') # Agrega cero al final
    r = r / amax(r) # Normaliza (máximo=1)
    t = arange(len(r)) / fm
    plot( 1000*t, r )
    xlim( (1000*t[0], 1000*t[-1]) )
    ylabel('$r(t)$') 
    xlabel('Time (ms)')
    grid()
    show()

# Tomado de http://pydoc.net/Python/scikits.talkbox/0.2.5/scikits.talkbox.linpred.py_lpc/
def lpc_ref(signal, order):
    """Compute the Linear Prediction Coefficients.

    Return the order + 1 LPC coefficients for the signal. c = lpc(x, k) will
    find the k+1 coefficients of a k order linear filter:

      xp[n] = -c[1] * x[n-2] - ... - c[k-1] * x[n-k-1]

    Such as the sum of the squared-error e[i] = xp[i] - x[i] is minimized.

    Parameters
    ----------
    signal: array_like
        input signal
    order : int
        LPC order (the output will have order + 1 items)

    Notes
    ----
    This is just for reference, as it is using the direct inversion of the
    toeplitz matrix, which is really slow"""
    if signal.ndim > 1:
        raise ValueError("Array of rank > 1 not supported yet")
    if order > signal.size:
        raise ValueError("Input signal must have a lenght >= lpc order")

    if order > 0:
        p = order + 1
        r = np.zeros(p, signal.dtype)
        # Number of non zero values in autocorrelation one needs for p LPC
        # coefficients
        nx = np.min([p, signal.size])
        x = np.correlate(signal, signal, 'full')
        r[:nx] = x[signal.size-1:signal.size+order]
        phi = np.dot(sp.linalg.inv(sp.linalg.toeplitz(r[:-1])), -r[1:])
        return np.concatenate(([1.], phi))
    else:
        return np.ones(1, dtype = signal.dtype)
        
def outmidear(n,fs):
# This funtion creates an N-coefficients FIR filter that simulates the
# outer-middle ear. FS is the sampling frequency of the signal to be
# filtered.
# The specification of the filter is taken from a figure in:
# B.R. Glasberg and B.C.J. Moore, A model of loudness applicable to 
# time-varying sounds, J. Audio Eng. Soc. 50: 331-342 (2002)
    f = array([             0, .02, .05,    .1, .2,  .5,  .6, .7, 1, 2, 3, 4,  5,  8,   9,  10, 12,  13,  14,  15]) * 1000
    g = array([ float('-inf'), -39, -19, -12.5, -8,  -2,  -1,  0, 0, 4, 8, 8,  5, -9, -11, -11, -9, -13, -19, -15]) # gain
    m = 10 ** (g/20)
    if fs/2 > f[-1]:
        f = concatenate( (f, [fs/2]) )
        m = concatenate( (m, [0]) )
    else:
        mend = interp( fs/2, f, m )
        i = f < fs/2
        f = concatenate( ( f[i], [fs/2] ) )
        m = concatenate( ( m[i], [mend] ) )
    oddsize = 2*ceil(n/2) + 1
    b = firwin2( oddsize, f/(fs/2), m )
    return b

#----------------------------------------------------------------------------

def formants(filename):
    #load WAV file
    s, fm = loadWAV(filename)

    N = 2 ** round( log2( 0.050*fm ) )
    s = windowing(s, N)
    a = getACoefficient(fm, s)
    plotFormants(fm, N, s, a)

def vocalTract(filename):
    #load WAV file
    s, fm = loadWAV(filename)

    N = 2 ** round( log2( 0.100*fm ) )
    s = windowing(s, N)
    a = getACoefficient(fm, s)
    u = plotU(fm, s, a)
    plotAutocorrelation(fm, u)

#----------------------------------------------------------------------------

def cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Assignment 5 of the Audio Processing course.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'formants',     'Window analysis of the Sawtooth signal')
    p.add_argument(     '--filename',   help='Path of the WAV file', default='')

    p = add_command(    'vocalTract',   'Window analysis of a WAV file')
    p.add_argument(     '--filename',   help='Path of the WAV file', default='')

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    cmdline(sys.argv)

#----------------------------------------------------------------------------