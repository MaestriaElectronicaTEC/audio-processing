# Assignment 1

Here is the implementation corresponding to the first assignment for the Audio Processing course. The *assignment_1.py* script has the following functions:
 - *plot_signal*: Plot some audio signal.
 - *plot_fmpd*: Plot the magnitude diference of a signal.
 - *plot_spectrum*: Plot the spectrum and the distance to the cochlea of an audio signal.

```
$ python assignment_1.py --help
usage: assignment_1.py [-h] {plot_signal,plot_fmpd,plot_spectrum} ...

Assignment 1 of the Audio Processing course.

positional arguments:
  {plot_signal,plot_fmpd,plot_spectrum}
    plot_signal         Plot of the audio signal
    plot_fmpd           Plot of the audio signal FMPD
    plot_spectrum       Plot of the audio signal spectrum

optional arguments:
  -h, --help            show this help message and exit

Type "assignment_1.py <command> -h" for more information.
```

```
$ python assignment_1.py plot_signal --help
usage: assignment_1.py plot_signal [-h] [--filename FILENAME] [--t1 T1]
                                   [--t2 T2]

Plot of the audio signal

optional arguments:
  -h, --help           show this help message and exit
  --filename FILENAME  Path of the WAV file
  --t1 T1              Start time (ms) to plot
  --t2 T2              End time (ms) to plot
```

```
$ python assignment_1.py plot_fmpd --help
usage: assignment_1.py plot_fmpd [-h] [--filename FILENAME] [--k K] [--t1 T1]
                                 [--t2 T2] [--A1 A1] [--A2 A2]

Plot of the audio signal FMPD

optional arguments:
  -h, --help           show this help message and exit
  --filename FILENAME  Path of the WAV file
  --k K                FMPD factor
  --t1 T1              Start time (ms) to plot
  --t2 T2              End time (ms) to plot
  --A1 A1              Low amplitude
  --A2 A2              Hight amplitude
```

```
$ python assignment_1.py plot_spectrum --help
usage: assignment_1.py plot_spectrum [-h] [--filename FILENAME] [--t1 T1]
                                     [--t2 T2]

Plot of the audio signal spectrum

optional arguments:
  -h, --help           show this help message and exit
  --filename FILENAME  Path of the WAV file
  --t1 T1              Start time (ms) to plot
  --t2 T2              End time (ms) to plot
```
