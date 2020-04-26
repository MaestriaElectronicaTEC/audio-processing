import sys
import argparse
import matplotlib.pyplot as plt

from numpy import amax, argmax, arange, concatenate, interp, prod, zeros, around, mean, cos, iinfo
from numpy.random import normal
from scipy.signal import hann, sawtooth
from scipy.io.wavfile import read, write
from math import log2, pi

# Algoirihtms of pitch detection
from a1 import a1
from a2 import a2
from a3 import a3
from a4 import a4
from a5 import a5
from a6 import a6
from a7 import a7

from matplotlib.pyplot import gca, imshow, xlabel, ylabel, plot

#----------------------------------------------------------------------------

def plot_score_matrix(S, pc, t):
    imshow (S , aspect='auto')
    ax = gca()
    yticks = around(arange(0, len(pc), len(pc)/10)).astype(int)
    ax.set_yticks(yticks)
    ax.set_yticklabels(around(pc[yticks]).astype(int))
    xticks = around(arange(0, len(t), len(t)/10)).astype(int)
    ylabel('Pitch (Hz)')
    ax.set_xticks(xticks)
    ax.set_xticklabels(around(t[xticks], 2))
    xlabel('Time (s)')
    plt.show()

def plot_scores(S, pc):
    plot(pc, S[:, round(S.shape[1]/2)])
    ylabel('Score')
    xlabel('Pitch (Hz)')
    plt.show()

def plot_winner_score(t, s):
    plot(1000*t, s)
    ylabel('Winner score')
    xlabel('Time (s)')
    plt.show()

def gen_sawtooth(f):
    fm = 10000
    Tm = 1/fm
    t = arange(0, 0.5, Tm)
    x = 2*pi*sawtooth(2*pi*f*t)
    #write('sawtooth.wav', fm, x/2)
    return (t, x, fm)

def gen_tone(f):
    fm = 10000
    Tm = 1/fm
    t = arange(0, 0.5, Tm)
    x = 2*pi*cos(2*pi*f*t)
    #write('tone' + str(f) + '.wav', fm, x/2)
    return (t, x, fm)

def gen_mixed_tones():
    fm = 10000
    Tm = 1/fm
    t = arange(0, 0.5, Tm)

    # 650 Hz
    f = 650
    x1 = 2*pi*cos(2*pi*f*t)

    # 950 Hz
    f = 950
    x2 = 2*pi*cos(2*pi*f*t)

    # 1250 Hz
    f = 1250
    x3 = 2*pi*cos(2*pi*f*t)

    x = x1 + x2 + x3

    return (t, x, fm)

def gen_white_noise():
    fm = 10000
    Tm = 1/fm
    t = arange(0, 0.5, Tm)
    mean = 0
    std = 1
    x = 2*pi*normal(mean, std, size=len(t))
    return (t, x, fm)

def openWavFile(filename):
    (fm,s) = read(filename)

    Tm = 1/fm
    t = arange(0, 1, Tm)

    x = s / iinfo(s.dtype).max
    return (t, x, fm)

#----------------------------------------------------------------------------

def HPS():
    #t, x, fm = gen_sawtooth(200)
    t, x, fm = gen_tone(200)
    (p,t,s,pc,S) = a1(x,fm) # invoca a HPS

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

def SHS():
    t, x, fm = gen_tone(200)
    (p,t,s,pc,S) = a2(x,fm) # invoca a SHS

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

def SHS2():
    #t, x, fm = gen_tone(200)
    t, x, fm = gen_white_noise()
    (p,t,s,pc,S) = a3(x,fm) # invoca a SHS2

    m = mean(s)
    print('mean: ' + str(m))

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)
    plot_winner_score(t, s)

def SHR():
    #t, x, fm = gen_tone(200)
    #t, x, fm = gen_white_noise()
    t, x, fm = gen_mixed_tones()
    (p,t,s,pc,S) = a4(x,fm) # invoca a SHR

    m = mean(s)
    print('mean: ' + str(m))

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)
    plot_winner_score(t, s)

def AC():
    t, x, fm = gen_mixed_tones()
    (p,t,s,pc,S) = a5(x,fm) # invoca a Autocorrelation

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

def AC2():
    t, x, fm = gen_mixed_tones()
    (p,t,s,pc,S) = a6(x,fm) # invoca a Autocorrelation 2

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

def AC3():
    #t, x, fm = gen_mixed_tones()
    t, x, fm = openWavFile('../assignment_1/sounds/anthem.wav')
    (p,t,s,pc,S) = a7(x,fm) # invoca a Autocorrelation 3

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

#----------------------------------------------------------------------------

def cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Assignment 4 of the Audio Processing course.',
        epilog      = 'Type "%s <command> -h" for more information.' % prog)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command(    'HPS',       'Harmonic Product Spectrum')
    p = add_command(    'SHS',       'Subharmonic summation')
    p = add_command(    'SHS2',      'Subharmonic summation with weighing')
    p = add_command(    'SHR',       'Subharmonic-to-harmonic ratio')
    p = add_command(    'AC',        'Autocorrelation')
    p = add_command(    'AC2',       'Autocorrelation 2')
    p = add_command(    'AC3',       'Autocorrelation 3')

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    cmdline(sys.argv)

#----------------------------------------------------------------------------
