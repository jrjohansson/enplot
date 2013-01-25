enplot
======

one-line plotting toolenplot: a one-line plot command

enplot use python and matplotlib to provide a simple command-line interface
that be used to quickly plot data in CSV format.

Example
-------

A one-line command to plot the column data in the file `qubit_population.dat`

    enplot -x 0 -y 1,2 -X "time" -Y "Probabilities" qubit_population.dat 

Plot 3D data:

    enplot -x 0 -y 1 -z 2 -c -v 3d tests/example-data1.dat

Plot 3D data as color map:

    enplot -x 0 -y 1 -z 2 -c tests/example-data1.dat
