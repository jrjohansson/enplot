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
import numpy as np
import copy

debug = False


def data_matrix_sort(M, col):
    """
    Sort the columns in a given matrix according to give column.
    """

    isort = M[:, col].argsort()
    for i in np.arange(M.shape[1]):
        M[:,i] = M[:,i][isort]    

    return M


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

    if debug:
        print("Found matrix of size MxN = %dx%d" % (M, N))

    mat = np.zeros((M, N), float)

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


def file_data_read(datafile, sep=None, header=0):
    """
    Read data from a field-separated values text file (by default tab
    separated, but the separator can be changed by the optional second
    argument). Return the data in matrix.
    """

    if datafile is None:
        raise ValueError("datafile is unspecified")
    f = open(datafile, "r")

    i_header=0
    sep = ""
    for line in f:
        # skip header lines
        if i_header <= header:
            i_header += 1
        else:
            if line[0] != '#' and line[0] != '%':
                if sep == "":
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
                break

    f.close()
    data = np.genfromtxt(datafile, delimiter=sep, skip_header=header)
    M, N = data.shape
    return data, M, N

def build_matrix(M, xcol, ycol, zcol, x_range=None, y_range=None):
    """
    Constuct a matrix representation of data in list format.
    """

    if not x_range:
        x_range = np.sort(np.unique(M[:, xcol]))

    if not y_range:
        y_range = np.sort(np.unique(M[:, ycol]))

    n = x_range.size
    m = y_range.size

    if debug != 0:
        print("Building Z [" + str(n) + "x" + str(m) + "]")

    Z = np.zeros((m, n), float)

    for i in range(len(M[:, zcol])):

        a = np.nonzero(x_range == M[i, xcol])[0][0]
        b = np.nonzero(y_range == M[i, ycol])[0][0]

        Z[b, a] = M[i, zcol]

    X, Y = np.meshgrid(x_range, y_range)

    return X, Y, Z
