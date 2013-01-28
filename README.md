enplot
======

enplot: a one-line plot command

enplot use python and matplotlib to provide a simple command-line interface
that be used to quickly plot data in CSV and related formats.

Examples
--------

Plot lines corresponding to column data:

    enplot -x 0 -y 1,2 -X "time" -Y "Probabilities" -o tests/example-data0.png tests/example-data0.dat

![example-data0](https://raw.github.com/jrjohansson/enplot/master/tests/example-data0.png)

Plot 3D data:

    enplot -x 0 -y 1 -z 2 -c -v 3d -o tests/example-data1.png tests/example-data1.dat

![example-data1](/tests/example-data1.png)

Plot 3D data as color map:

    enplot -x 0 -y 1 -z 2 -c tests/example-data1.dat


