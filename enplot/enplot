#!/usr/bin/env python
#
# enplot: A plot tool for quickly plotting data in TSV,SSV,CSV formats from the command line.
#
# Requires:
#
#    1) python
#    2) SciPy
#    3) matplotlib (pylab)
#
# Purpose:
#
#    To quickly plot a data file from the command line for general inspection.
#    Publication quality figures should be generated with some other software. 
#
# Robert Johansson <robert@riken.jp>
# License: GPL

from scipy import *
from pylab import *
import os
import copy
import getopt
import sys

rc('text', usetex=True)
rc('font', family='serif')

def usage():
    print "plottoolsep [-t title] [-p plot.png] [-x xcol] [-y ycol_list] [-X x_label] [-Y y_label] [-d dim] data_files"
    print
    print " ycol_list:    is a comma separated list of integers which indicate which columns to plot"
    print " data_files:    is a blank space separated list of data files to plot"
    print
    print "Additional options:"
    print
#    print " -d D        using data file delimiter D (i.e., space or \t)"
#    print " -S sep        using data file separator sep (values 'space' or 'tab')
    print " -s        sort the data point by the x-axis"
    return

try:     
    opts, args = getopt.getopt(sys.argv[1:], "hbd:p:x:y:X:Y:t:DsS:qa:l:", ["help", "debug", "dim=", "plot=", "xcol=", "ycol", "xlbl","ylbl=", "title=", "dots", "sort", "scale", "quiet", "style=", "legend="]) 

except getopt.GetoptError:     
    usage()  
    sys.exit(2)                     

# Defaults
legend_str = ""
style_str  = ""

plot_file = ""
data_files = 0 
xcol = -1
ycol = [1]
xlbl = "x"
ylbl = "y"
yscale = 1
debug = 0
dim = "\t"
title_text = ""
style = ("-b", "-g", "-k", "-r")
style_no = 4
sort_flag = 0 
quiet = 0

# parse command line arguments
for opt, arg in opts:                
    if opt in ("-h", "--help"):      
        usage()                     
        sys.exit()                  
    elif opt in ("-p", "--plot"): 
        plot_file = arg   
    elif opt in ("-x", "--xcol"): 
        xcol = int(arg)     
    elif opt in ("-y", "--ycol"): 
        ycol = arg.split(",")
    elif opt in ("-X", "--xlbl"): 
        xlbl = arg     
    elif opt in ("-Y", "--xlbl"): 
        ylbl = arg     
    elif opt in ("-Y", "--xlbl"): 
        ylbl = arg     
    elif opt in ("-d", "--dim"): 
        dim = arg 
    elif opt in ("-t", "--title"): 
        title_text = arg     
    elif opt in ("-l", "--legend"): 
        legend_str = arg     
    elif opt in ("--style"): 
        style_str = arg     
    elif opt in ("-S", "--separator"): 
        if arg == "space":
            dim = " "
        elif arg == "tab":
            dim = "\t"
    elif opt in ("-D", "--dots"): 
        style = (".r", ".b", ".g", ".k")
    elif opt in ("-s", "--sort"): 
        sort_flag = 1
    elif opt in ("-d", "--debug"): 
        debug = 1
    elif opt in ("-q", "--quiet"):
        quiet = 1


if style_str and (style_str) > 0:
    style = style_str.split(":")


data_files = args

if len(data_files) < 1:
    usage()
    sys.exit()

if debug != 0:
    print "Plot data in", data_files, "and store in", plot_file
    print " - plot column", str(xcol), "vs columns",ycol
    print " - label them", xlbl, "vs", ylbl

def matrix_sort(M, col):

    MM = copy.copy(M)

    v = M[:,col]
    vv = copy.copy(sort(v))

    for i in range(0, len(vv)):
        for j in range(0, len(vv)):
            if M[j,col] != vv[i]:
                j += 1
            else:
                break

            MM[i,:] = M[j,:]

    return MM

def read_matrix_file(filename, sep = "\t"):

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
    mat = zeros((M,N), float)
    
    file = open(filename, "r")
    m = 0
    for line in file.readlines():
        if line[0] == '#':
            continue
        n = 0
        elemlist = line.strip().split(sep)
        for e in elemlist:
            if e:
                mat[m,n] = float(e)
            else:
                mat[m,n] = 0
            n += 1
        m += 1
    file.close

    return mat, N, M 

# ------------------------------------------------------------------------------
# Read matrix data from a file
#
def file_data_read(datafile, sep=None):

    if datafile == None:
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
        if N == 0 and sep == None:
            if len(line.rstrip().split(",")) > 1:
                sep = ","
            elif len(line.rstrip().split(";")) > 1:
                sep = ";"
            elif len(line.rstrip().split(":")) > 1:
                sep = ":"
            elif len(line.rstrip().split("|")) > 1:
                sep = "|"
            elif len(line.rstrip().split()) > 1:
                sep = None # sepical case for a mix of white space deliminators
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
            raise ValueError("Badly formatted data file: unequal number of columns")
        M += 1

    #
    # read data and store in a matrix
    #
    f.seek(0)

    if numtype == "complex":
        data = zeros((M,N), dtype="complex")
        m = n = 0
        for line in f:
            # skip comment lines
            if line[0] == '#' or line[0] == '%':
                continue
            n = 0
            for item in line.rstrip().split(sep):
                data[m,n] = complex(item)
                n += 1
            m += 1
    
    else:
        data = zeros((M,N), dtype="float")        
        m = n = 0
        for line in f:
            # skip comment lines
            if line[0] == '#' or line[0] == '%':
                continue
            n = 0
            for item in line.rstrip().split(sep):
                data[m,n] = float(item)
                n += 1
            m += 1

    f.close()

    return data, M, N

# ------------------------------------------------------------------------------
# Read matrix data from a file
#
si = 0
for data_file in data_files:

    if debug != 0:
        print "Processing data file ", data_file

    M, m, n = file_data_read(data_file)

    if sort_flag == 1:
        M = matrix_sort(M, xcol)

    for i in ycol:
        if int(i) < int(n):
            if xcol != -1:
                plot(M[:,xcol], M[:,int(i)] * yscale, style[si % style_no])
            else:
                plot(M[:,int(i)] * yscale, style[si % style_no])
            si = si + 1
        else:
            print "The data file", data_file, ": column", i, "does not exist.", n

if len(title_text) > 0:
    title(title_text)

xlabel(xlbl)
ylabel(ylbl)

if legend_str and (legend_str) > 0:
    legend(legend_str.split(":"))
    
if len(plot_file) > 0:
    savefig(plot_file)
        
if (quiet == 0):
    show()

