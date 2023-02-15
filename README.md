# ujoules
Python script that measures energy usage over a certain time-span using RAPL.

## Dependencies

 * python3
 * /sys/devices/virtual/powercap/intel-rapl/

## Usage

This script need to be run with root privileges, as rapl data is inaccessible otherwise.

```
$ sudo ./ujoules.py sleep 600
find /sys/devices/virtual/powercap/intel-rapl -name intel-rapl\:\* -print
RAPL zones found:  ['package-0', 'core', 'uncore']
start test
ended test
Used energy in μjoules:
package-0   11454415074
core         6079606628
uncore        303380083
```

## Author

Bram Stolk (b.stolk@canonical.com)

## License

GPLv3

