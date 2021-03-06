import sys
import argparse

from numpy import iinfo, arange, reshape, interp , linspace , log2 , sqrt, hamming, ones
from scipy.io.wavfile import read
from matplotlib.pyplot import xlabel, ylabel, xlim, ylim, figure, plot, show
from matplotlib.mlab import specgram

#----------------------------------------------------------------------------

def _openWavFile(filename):
    (fm,s) = read(filename)
    s = s / iinfo(s.dtype).max
    return (fm, s)

def _applyWindow(signal, fm, t1, t2, type='hamming'):
    n1 = int((t1*fm) / 1000)
    n2 = int((t2*fm) / 1000)
    
    window = None
    if (type == 'square'):
        window = ones(n2 - n1)
    elif (type == 'hamming'):
        window = hamming(n2 - n1)

    s = signal[n1:n2]
    s = s * window

    return s


def _FMPD(N, k, signal):
    # intial variables
    C = 1 / (N - k)
    res = []

    # summation
    for i in range(N - k):
        res.append( C * abs(signal[i] - signal[i + k]) )

    return res

def _plot_signal(s, fm, t1, t2, A1=-0.5, A2=0.5):
    # initial variables
    dt = 1/fm
    N = len(s)
    t = arange(N)*dt*1000

    # plot the signal
    figure (1)
    plot(t,s)
    xlabel('Time (ms)')
    xlim( (t1, t2) )
    ylim( (A1, A2) )
    show()

def _plot_spectrum(s, fm):
    N = len(s)
    (S,f, _) = specgram(s, N, fm, detrend=None, window=None, noverlap=None, pad_to=None, sides=None, scale_by_freq=None, mode='magnitude')
    S = reshape(S, len(S))
    S = S / (N/4)

    # plot spectrum
    figure (1)
    plot(f,S)
    xlabel('Frequency (Hz)')

    # plot sonority
    fmax = fm / 2
    x = linspace( 0, 5.7*log2(1+fmax/230), 1000 )
    fc=(2**(x/5.7)-1)*230
    S = sqrt( interp(fc, f, S) )
    figure (2)
    plot( x, S/max(S) )
    ylabel('Relative specific sonority (sones)')
    xlabel('Distance from the cochlea base (mm)')
    show()

#----------------------------------------------------------------------------

def plot_signal(filename, t1, t2):
    # load the WAV file
    (fm, s) = _openWavFile(filename)

    # plot the signal
    _plot_signal(s, fm, t1, t2)

def plot_fmpd(filename, k, t1, t2, A1, A2):
    # load the WAV file
    (fm, s) = _openWavFile(filename)
    s = _applyWindow(s, fm, t1, t2, 'square')

    # calculate the FMPD
    k = (k*fm) / 1000
    fmpd = _FMPD(len(s), int(k), s)

    # plot FMPD
    _plot_signal(fmpd, fm, 0, t2 - t1, A1, A2)

def plot_spectrum(filename, t1, t2):
    # load the WAV file
    (fm, s) = _openWavFile(filename)
    s = _applyWindow(s, fm, t1, t2)

    # plot the signal spectrum
    _plot_spectrum(s, fm)

#----------------------------------------------------------------------------

def cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Assignment 1 of the Audio Processing course.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'plot_signal',          'Plot of the audio signal')
    p.add_argument(     '--filename',           help='Path of the WAV file', default='')
    p.add_argument(     '--t1',                 help='Start time (ms) to plot', type=int, default=200)
    p.add_argument(     '--t2',                 help='End time (ms) to plot', type=int, default=300)

    p = add_command(    'plot_fmpd',            'Plot of the audio signal FMPD')
    p.add_argument(     '--filename',           help='Path of the WAV file', default='')
    p.add_argument(     '--k',                  help='FMPD factor', type=float, default=1.0)
    p.add_argument(     '--t1',                 help='Start time (ms) to plot', type=int, default=200)
    p.add_argument(     '--t2',                 help='End time (ms) to plot', type=int, default=300)
    p.add_argument(     '--A1',                 help='Low amplitude', type=float, default=0)
    p.add_argument(     '--A2',                 help='Hight amplitude', type=float, default=0.001)

    p = add_command(    'plot_spectrum',        'Plot of the audio signal spectrum')
    p.add_argument(     '--filename',           help='Path of the WAV file', default='')
    p.add_argument(     '--t1',                 help='Start time (ms) to plot', type=int, default=200)
    p.add_argument(     '--t2',                 help='End time (ms) to plot', type=int, default=300)

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    cmdline(sys.argv)

#----------------------------------------------------------------------------