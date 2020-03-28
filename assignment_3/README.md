# Assignment 3

Here is the implementation corresponding to the third assignment for the Audio Processing course. The *assignment_3.py* script has the following functions:
 - *sawtoothWindowAnalysis*: Window analysis of a sawtooth wave.
 - *audioWindowAnalysis*: Window analysis of a WAV file.

```
$ python assignment_3.py --help
usage: assignment_3.py [-h] {sawtoothWindowAnalysis,audioWindowAnalysis} ...

Assignment 3 of the Audio Processing course.

positional arguments:
  {sawtoothWindowAnalysis,audioWindowAnalysis}
    sawtoothWindowAnalysis
                        Window analysis of the Sawtooth signal
    audioWindowAnalysis
                        Window analysis of a WAV file

optional arguments:
  -h, --help            show this help message and exit

Type "assignment_3.py <command> -h" for more information.
```

```
$ python assignment_3.py sawtoothWindowAnalysis --help
usage: assignment_3.py sawtoothWindowAnalysis [-h] [--f F] [--M M]
                                              [--winType WINTYPE]

Window analysis of the Sawtooth signal

optional arguments:
  -h, --help         show this help message and exit
  --f F              Frecuency of the Sawthooth signal
  --M M              Lenght in milliseconds of the window
  --winType WINTYPE  Window type: 0 - Rectangular, 1 - Hanning, 2 - Hamming
```

```
$ python assignment_3.py audioWindowAnalysis --help
usage: assignment_3.py audioWindowAnalysis [-h] [--filename FILENAME] [--M M]
                                           [--winType WINTYPE]

Window analysis of a WAV file

optional arguments:
  -h, --help           show this help message and exit
  --filename FILENAME  Path of the WAV file
  --M M                Lenght in milliseconds of the window
  --winType WINTYPE    Window type: 0 - Rectangular, 1 - Hanning, 2 - Hamming
```
