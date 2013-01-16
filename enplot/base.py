"""
enplot library: A simple library with support functions for plotting using
matplotlib.

Requires:

   1) python
   2) SciPy
   3) matplotlib


Robert Johansson <robert@riken.jp>
License: LGPL
"""
from scipy import *
import numpy as np

import os
import copy
import sys

debug = 0


def data_matrix_sort(M, col):
    """
    Sort the columns in a given matrix according to give column.
    """

    MM = copy.copy(M)

    v = M[:, col]
    vv = copy.copy(sort(v))

    for i in range(0, len(vv)):
        for j in range(0, len(vv)):
            if M[j, col] != vv[i]:
                j += 1
            else:
                break

            MM[i, :] = M[j, :]

    return MM


def data_matrix_read_file(filename, sep="\t"):
    """
    Read a matrix from a field-separated values text file (by default tab
    separated, but the separator can be changed by the optional second
    argument)
    """

    N = 0
    M = 0

    file = open(filename, "r")
    for line in file.readlines():
        M += 1
    elemlist = line.strip().split(sep)
    N = len(elemlist)
    file.close

    if debug != 0:
        print "Found matrix of size MxN =", M, "x", N
    mat = zeros((M, N), float)

    file = open(filename, "r")
    m = 0
    for line in file.readlines():
        if line[0] == '#':
            continue
        n = 0
        elemlist = line.strip().split(sep)
        for e in elemlist:
            if e:
                mat[m, n] = float(e)
            else:
                mat[m, n] = 0
            n += 1
        m += 1
    file.close

    return mat, N, M


def file_data_read(datafile, sep=None):
    """
    Read data from a field-separated values text file (by default tab
    separated, but the separator can be changed by the optional second
    argument). Return the data in matrix.
    """

    if datafile is None:
        raise ValueError("datafile is unspecified")

    f = open(datafile, "r")

    #
    # first count lines and numbers of
    #
    M = N = 0
    for line in f:
        # skip comment lines
        if line[0] == '#' or line[0] == '%':
            continue
        # find delim
        if N == 0 and sep is None:
            if len(line.rstrip().split(",")) > 1:
                sep = ","
            elif len(line.rstrip().split(";")) > 1:
                sep = ";"
            elif len(line.rstrip().split(":")) > 1:
                sep = ":"
            elif len(line.rstrip().split("|")) > 1:
                sep = "|"
            elif len(line.rstrip().split()) > 1:
                sep = None  # for a mix of white space deliminators
            else:
                raise ValueError("Unrecognized column deliminator")
        # split the line
        line_vec = line.split(sep)
        n = len(line_vec)
        if N == 0 and n > 0:
            N = n
            # check type
            if ("j" in line_vec[0]) or ("i" in line_vec[0]):
                numtype = "complex"
            else:
                numtype = "real"

            # check format
            if ("e" in line_vec[0]) or ("E" in line_vec[0]):
                numformat = "exp"
            else:
                numformat = "decimal"

        elif N != n:
            raise ValueError(
                "Badly formatted data file: unequal number of columns")
        M += 1

    #
    # read data and store in a matrix
    #
    f.seek(0)

    if numtype == "complex":
        data = zeros((M, N), dtype="complex")
        m = n = 0
        for line in f:
            # skip comment lines
            if line[0] == '#' or line[0] == '%':
                continue
            n = 0
            for item in line.rstrip().split(sep):
                data[m, n] = complex(item)
                n += 1
            m += 1

    else:
        data = zeros((M, N), dtype="float")
        m = n = 0
        for line in f:
            # skip comment lines
            if line[0] == '#' or line[0] == '%':
                continue
            n = 0
            for item in line.rstrip().split(sep):
                data[m, n] = float(item)
                n += 1
            m += 1

    f.close()

    return data, M, N


def build_matrix(M, x_range, y_range, xcol, ycol, zcol):
    """
    Constuct a matrix representation of data in list format.
    """

    n = x_range.size
    m = y_range.size

    if debug != 0:
        print "Building Z [" + str(n) + "x" + str(m) + "]"

    Z = np.zeros((m, n), float)

    for i in range(len(M[:, zcol])):
        a = np.nonzero(x_range == M[i, xcol])[0][0]
        b = np.nonzero(y_range == M[i, ycol])[0][0]
        Z[b, a] = M[i, zcol]

    return Z
