import sys
import argparse
import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt, resample, lfilter
from scipy.io.wavfile import read, write
import numpy as np
from numpy import iinfo, zeros, append

#----------------------------------------------------------------------------

def _openWavFile(filename):
    (fm,s) = read(filename)
    s = s / iinfo(s.dtype).max
    return (fm, s)

def _writeWavFile(filename, s,fs):
    write(filename, fs, s)

def _resample_size(s, fm, fs):
    T_old = 1 / fm
    T_new = 1 / fs
    N_old = len(s)
    N_new = int(T_old/T_new) * len(s)
    return N_old, N_new

def _plot(title, s, fm, t1=185, t2=200, A1=-0.5, A2=0.5):
    # initial variables
    dt = 1/fm
    N = len(s)
    t = np.arange(N)*dt*1000

    plt.subplot(2,1,1)
    plt.title(title)
    plt.plot(t, s,'g')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (ms)')
    plt.ylim( (A1, A2) )

    plt.subplot(2,1,2)
    plt.plot(t, s, 'r')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (ms)')
    plt.xlim( (t1, t2) )
    plt.ylim( (A1, A2) )

    plt.subplots_adjust(hspace=1)
    plt.rc('font', size=15)
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.show()

def _filter(s, fm):
    # Filter requirements.
    cutoff = 15000  # desired cutoff frequency of the filter, Hz
    nyq = 0.5 * fm  # Nyquist Frequency
    order = 2       # sin wave can be approx represented as quadratic

    # Apply lowpass filter
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    s = filtfilt(b, a, s)
    return s

def _modulate(s, f, fm, fs, t1, t2):
    # resample
    _, N_new = _resample_size(s, fm, fs)
    s = resample(s, N_new)

    # carrier
    t = np.linspace(0, len(s), len(s))
    carrier = np.cos(2*np.pi*(f/fs)*t)

    # Modulation
    product = carrier * s

    # plot
    _plot('Original signal', s, fs, t1, t2)
    _plot('Modulated signal', product, fs, t1, t2)
    
    return product

def _demodulate(s, f, fm, fs, t1, t2):
    
    N_old, N_new = _resample_size(s, fm, fs)
    factor = int(N_new / N_old)
    N_new = int(len(s) / factor)

    t = np.linspace(0, len(s), len(s))
    carrier = np.cos(2*np.pi*(f/fs)*t)

    # Demodulate
    original = s * carrier

    # Filter
    original = _filter(original, fs)

    # resample
    original = resample(original, N_new)

    # plot
    _plot('Reconstructed signal', original, fm, t1, t2)

    # Amplify the signal
    original = 10*original

    return original

#----------------------------------------------------------------------------

def impulse_response(hfilename, sfilename, outputfile, t1, t2):
    # load the impulse response
    fh, h = _openWavFile(hfilename)

    # load the voice
    fv, v = _openWavFile(sfilename)
    
    # apply the impulse response
    y, zf = lfilter(h, 1, v, zi=zeros(len(h) - 1))
    y = append(y, zf)
    y = ((y - np.min(y)) / np.ptp(y)) - 0.5

    # plot
    _plot('Impuse response', h, fh, 0, 50, -1, 1)
    _plot('Voice signal', v, fv, t1, t2)
    _plot('Voice with impulse response', y, fv, t1, t2, -0.6, 0.6)

    # save wav file
    write(outputfile, fv, y)

def amplitude_modulation(filename, outputfile, modulate, demodulate, f, fs, t1, t2):
    # load signal
    fm, s = _openWavFile(filename)

    # resample
    if (fs is -1):
        fs = fm

    # modulation
    if (modulate):
        s = _modulate(s, f, fm, fs, t1, t2)

    # demodulation
    if (demodulate):
        s = _demodulate(s, f, fm, fs, t1, t2)

    # save WAV
    _writeWavFile(outputfile, s, fm)


#----------------------------------------------------------------------------

def cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Assignment 2 of the Audio Processing course.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'impulse_response',     'Impulse response of a room')
    p.add_argument(     '--hfilename',          help='Path of the WAV file for the impulse response', default='')
    p.add_argument(     '--sfilename',          help='Path of the WAV file for the voice', default='')
    p.add_argument(     '--outputfile',         help='File name of the generated WAV file', default='')
    p.add_argument(     '--t1',                 help='Start time (ms)', type=float, default=100)
    p.add_argument(     '--t2',                 help='End time (ms)', type=float, default=200)

    p = add_command(    'amplitude_modulation', 'Amplitude modulation of a signal')
    p.add_argument(     '--filename',           help='Path of the WAV file', default='')
    p.add_argument(     '--outputfile',         help='File name of the generated WAV file', default='')
    p.add_argument(     '--modulate',           help='Apply modulation', action='store_true')
    p.add_argument(     '--demodulate',         help='Apply demodulation', action='store_true')
    p.add_argument(     '--f',                  help='Carrier frequency', type=int, default=870000)
    p.add_argument(     '--fs',                 help='Resample frequency', type=int, default=-1)
    p.add_argument(     '--t1',                 help='Start time (ms)', type=float, default=100)
    p.add_argument(     '--t2',                 help='End time (ms)', type=float, default=200)

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    cmdline(sys.argv)

#----------------------------------------------------------------------------