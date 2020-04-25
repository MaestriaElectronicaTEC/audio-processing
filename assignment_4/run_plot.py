import sys
import argparse
import matplotlib.pyplot as plt

from numpy import amax, argmax, arange, concatenate, interp, prod, zeros, around, mean
from scipy.signal import hann, sawtooth
from math import log2, pi

# Algoirihtms of pitch detection
from a1 import a1
from a2 import a2
from a3 import a3

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

#----------------------------------------------------------------------------

def HPS():
    fm = 8000 # frecuencia de muestreo
    dt = 1/fm # tiempo entre muestras
    t = arange(0,1,dt) # vector de tiempos
    x = sawtooth(2*pi*200*t) # senal de ejemplo
    #x = randn(round(fm/10)) # senal de ejemplo
    (p,t,s,pc,S) = a1(x,fm) # invoca a HPS

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

def SHS():
    fm = 8000 # frecuencia de muestreo
    dt = 1/fm # tiempo entre muestras
    t = arange(0,1,dt) # vector de tiempos
    x = sawtooth(2*pi*200*t) # senal de ejemplo
    #x = randn(round(fm/10)) # senal de ejemplo
    (p,t,s,pc,S) = a2(x,fm) # invoca a HPS

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)

def SHS2():
    fm = 8000 # frecuencia de muestreo
    dt = 1/fm # tiempo entre muestras
    t = arange(0,1,dt) # vector de tiempos
    x = sawtooth(2*pi*200*t) # senal de ejemplo
    #x = randn(round(fm/10)) # senal de ejemplo
    (p,t,s,pc,S) = a3(x,fm) # invoca a HPS

    m = mean(s)
    print('mean: ' + str(m))

    plot_score_matrix(S, pc, t)
    plot_scores(S, pc)
    plot_winner_score(t, s)

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

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['-h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

#----------------------------------------------------------------------------

if __name__ == "__main__":
    cmdline(sys.argv)

#----------------------------------------------------------------------------