# Assignment 4

Here is the implementation corresponding to the third assignment for the Audio Processing course. The *run_plot.py* script has the following functions:
- *HPS*: Harmonic Product Spectrum
- *SHS*: Subharmonic summation
- *SHS2*: Subharmonic summation with weighing
- *SHR*: Subharmonic-to-harmonic ratio
- *AC*: Autocorrelation
- *AC2*: Autocorrelation with proportion correction
- *AC3*: Autocorrelation with cochlea sampling


```
$ python run_plot.py --help
usage: run_plot.py [-h] {HPS,SHS,SHS2,SHR,AC,AC2,AC3} ...

Assignment 4 of the Audio Processing course.

positional arguments:
  {HPS,SHS,SHS2,SHR,AC,AC2,AC3}
    HPS                 Harmonic Product Spectrum
    SHS                 Subharmonic summation
    SHS2                Subharmonic summation with weighing
    SHR                 Subharmonic-to-harmonic ratio
    AC                  Autocorrelation
    AC2                 Autocorrelation 2
    AC3                 Autocorrelation 3

optional arguments:
  -h, --help            show this help message and exit

Type "run_plot.py <command> -h" for more information.

```
