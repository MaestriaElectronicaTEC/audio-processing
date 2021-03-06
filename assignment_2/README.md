# Assignment 2

Here is the implementation corresponding to the second assignment for the Audio Processing course. The *assignment_2.py* script has the following functions:
 - *impulse_response*: Impulse response of a room.
 - *amplitude_modulation*: Amplitude modulation of a signal.

```
$ python assignment_2.py --help
usage: assignment_2.py [-h] {impulse_response,amplitude_modulation} ...

Assignment 2 of the Audio Processing course.

positional arguments:
  {impulse_response,amplitude_modulation}
    impulse_response    Impulse response of a room
    amplitude_modulation
                        Amplitude modulation of a signal

optional arguments:
  -h, --help            show this help message and exit

Type "assignment_2.py <command> -h" for more information.
```

```
$ python assignment_2.py impulse_response --help
usage: assignment_2.py impulse_response [-h] [--hfilename HFILENAME]
                                        [--sfilename SFILENAME]
                                        [--outputfile OUTPUTFILE] [--t1 T1]
                                        [--t2 T2]

Impulse response of a room

optional arguments:
  -h, --help            show this help message and exit
  --hfilename HFILENAME
                        Path of the WAV file for the impulse response
  --sfilename SFILENAME
                        Path of the WAV file for the voice
  --outputfile OUTPUTFILE
                        File name of the generated WAV file
  --t1 T1               Start time (ms)
  --t2 T2               End time (ms)
```

Example:
```
python assignment_2.py impulse_response --hfilename sounds/impulse2.wav --sfilename ../assignment_1/sounds/anthem.wav --outputfile testeando.wav --t1 200 --t2 210
```

```
$ python assignment_2.py amplitude_modulation --help
usage: assignment_2.py amplitude_modulation [-h] [--filename FILENAME]
                                            [--outputfile OUTPUTFILE]
                                            [--modulate] [--demodulate]
                                            [--f F] [--fs FS] [--t1 T1]
                                            [--t2 T2]

Amplitude modulation of a signal

optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME   Path of the WAV file
  --outputfile OUTPUTFILE
                        File name of the generated WAV file
  --modulate            Apply modulation
  --demodulate          Apply demodulation
  --f F                 Carrier frequency
  --fs FS               Resample frequency
  --t1 T1               Start time (ms)
  --t2 T2               End time (ms)
```

Examples:
```
python assignment_2.py amplitude_modulation --filename sounds/2m1.wav --outputfile test.wav --modulate --demodulate --f 870000 --fs 4000000 --t1 185 --t2 186

python assignment_2.py amplitude_modulation --filename sounds/AM870,890,910.wav --outputfile UCR.wav --demodulate --f 870000  --t1 185 --t2 186
```
