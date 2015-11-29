#!/usr/bin/env python
"""
enplot: A command-line tool for quickly plotting data in CSV and related
formats.

Requires:

   1) Python
   2) NumPy
   3) matplotlib

Robert Johansson <robert@riken.jp>
License: LGPL
"""

import argparse
import sys
import numpy as np
import itertools

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import enplot.version
import enplot.base


def main():
    #
    # Configure and parse the command-line arguments
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile",
                        help="a data file in a CSV-like format",
                        type=str, nargs='*')
    parser.add_argument("-t", "--title",
                        help="plot title", type=str)
    parser.add_argument("-o", "--output-file",
                        help="file name for output", type=str)
    parser.add_argument("-f", "--output-format",
                        help="file format for output", type=str)
    parser.add_argument("-x",
                        help=("column index in the data file for use as " +
                              "X variable"),
                        type=str)
    parser.add_argument("-y",
                        help=("comma-separated list of column index in " +
                              "the data file for use as Y variables"),
                        type=str)
    parser.add_argument("-z",
                        help=("comma-separated list of column index in " +
                              "the data file for use as Y variables"),
                        type=str)
    parser.add_argument("-C",
                        help=("column index in the data file " +
                              "for use as color code"),
                        type=str, default=-1)
    parser.add_argument("--log-x",
                        help=("plot using log of the values in x-axis"),
                        action='store_true', default=False)
    parser.add_argument("--log-y",
                        help=("plot using log of the values in y-axis"),
                        action='store_true', default=False)
    parser.add_argument("-H", "--header",
                        help="Number of header lines to ignore",
                        type=int, default=0)    
    parser.add_argument("-m", "--matrix-form",
                        help="data in matrix form", action='store_true')
    parser.add_argument("-T", "--matrix-transpose",
                        help="transpose data in matrix form",
                        action='store_true')
    parser.add_argument("-X", "--x-label",
                        help="label for use on X axis", type=str)
    parser.add_argument("-Y", "--y-label",
                        help="label for use on Y axis", type=str)
    parser.add_argument("-Z", "--z-label",
                        help="label for use on Z axis", type=str)
    parser.add_argument("-l", "--legends",
                        help="comma-separated list of legends", type=str)
    parser.add_argument("-S", "--sort",
                        help="sort the data by the X-axis data points",
                        action='store_true')
    parser.add_argument("-s", "--style",
                        help="graph style ('line', 'bar')",
                        default='line')
    parser.add_argument("-q", "--quiet", help="do not display plot window",
                        action='store_true', default=False)
    parser.add_argument("-d", "--debug", help="activate debug printouts",
                        action='store_true', default=False)
    parser.add_argument("-v", "--view",
                        help="view perspective (top or 3d)", type=str)
    parser.add_argument("-V", "--version",
                        help="show version information", action='store_true')
    parser.add_argument("-c", "--colorbar",
                        help="Show colorbar", action='store_true')
    parser.add_argument('--mplstyle',
                        help="Matplotlib style sheet to apply to the plot.",
                        default=None)
    args = parser.parse_args()

    #
    #
    #
    if args.version:
        print("version = %s [%s]" % (enplot.version.version,
                                     enplot.version.revision))
        sys.exit(0)

    #
    #
    #
    if len(args.datafile) < 1:
        parser.print_help()
        sys.exit(0)

    #
    # process command-line arguemnts
    #
    colorcycler = itertools.cycle(['blue', 'green', 'red', 'magenta', 'cyan'])

    if not args.z:
        xcol = int(args.x) if args.x else -1
        ycols = [int(y) for y in args.y.split(",")] if args.y else [0]
        zcols = []
    else:
        xcol = int(args.x) if args.x else 0
        ycol = int(args.y) if args.y else 1
        zcols = [int(z) for z in args.z.split(",")] if args.z else [0]

    #
    # Use matplotlib to create the plot
    #
    params = {'font.family': 'serif',
              'font.size': 16,
              'axes.labelsize': 18,
              'legend.fontsize': 18,
              'xtick.labelsize': 18,
              'ytick.labelsize': 18,
              'text.usetex': True}
    matplotlib.rcParams.update(params)

    #
    # If a matplotlib stylesheet is specified, apply it now.
    #
    if args.mplstyle is not None:
        plt.style.use(args.mplstyle)

    #
    # Read and process the data from a files.
    #
    if not args.z and not args.matrix_form:
        #
        # 2d plot
        #
        fig, axes = plt.subplots(1, 1, figsize=(8, 6))

        for data_file in args.datafile:

            if args.debug:
                print("Processing data file " + data_file)

            M, m, n = enplot.base.file_data_read(data_file,
                                                 header=args.header)

            if args.sort:
                M = enplot.base.data_matrix_sort(M, xcol)

            for i in ycols:
                if i < n:
                    colors = next(colorcycler)
                    if xcol != -1:
                        xdata = M[:, xcol]
                        ydata = M[:, int(i)]
                    else:
                        xdata = np.arange(len(M[:, int(i)]))
                        ydata = M[:, int(i)]
                    if args.log_x:
                        xdata = np.log10(xdata)
                    if args.log_y:
                        ydata = np.log10(ydata)                        
                    if args.style == 'line':
                        axes.plot(xdata, ydata, color=colors)
                    elif args.style == 'scatter':
                        if args.C != -1:
                            colors = M[:, args.C]
                        p = axes.scatter(xdata, ydata, c=colors, edgecolor="none")
                    elif args.style == 'fill':
                        axes.fill_between(
                            xdata, ydata, np.zeros(ydata.shape),
                            color=colors, alpha=0.25)
                    elif args.style == 'bar':
                        axes.bar(xdata, ydata,
                                 color=next(colorcycler), align='center')
                    else:
                        raise TypeError(
                            "unrecongized plot style (-s argument)")

                else:
                    print("The data file", data_file,
                          ": column", i, "does not exist.", n)

        #
        # Add plot title, labels and legend
        #
        if args.title and len(args.title) > 0:
            axes.set_title(args.title)

        if args.x_label and len(args.x_label) > 0:
            axes.set_xlabel(args.x_label)

        if args.y_label and len(args.y_label) > 0:
            axes.set_ylabel(args.y_label)

        if args.legends and len(args.legends) > 0:
            axes.legend(args.legends.split(","))

        if args.colorbar and args.C != -1:
            fig.colorbar(p, ax=axes, fraction=0.05, aspect=30)

        axes.autoscale(tight=True)

    else:
        #
        # 3D plots
        #
        fig = plt.figure(figsize=(8, 6))

        if args.z:
            nax = len(zcols)
            ax_cols = np.ceil(nax / np.sqrt(nax))
            ax_rows = np.ceil(nax / ax_cols)

        #
        #
        #
        for data_file in args.datafile:

            ax_idx = 1
            M, m, n = enplot.base.file_data_read(data_file,
                                                 header=args.header)

            if args.matrix_form:
                # data already in matrix form

                if args.matrix_transpose:
                    M = M.T

                if args.view == "3d":
                    ax = fig.add_subplot(1, 1, 1, projection='3d')
                    X, Y = np.meshgrid(range(m), range(n))
                    ax.plot_surface(X, Y, M, rstride=1, cstride=1,
                                    cmap=cm.jet,
                                    linewidth=0, antialiased=True)

                else:
                    ax = fig.add_subplot(1, 1, 1)
                    p = ax.pcolor(M, antialiased=False, cmap=cm.RdBu)
                    if args.colorbar:
                        fig.colorbar(p, ax=ax, fraction=0.05, aspect=30)

                ax.autoscale(tight=True)

            else:
                # data in list form
                for zcol in zcols:

                    if args.debug:
                        print("Processing z column", zcol, "data file ",
                              data_file)

                    X, Y, Z = enplot.base.build_matrix(M, xcol, ycol, zcol)

                    if args.view == "3d":
                        ax = fig.add_subplot(ax_rows, ax_cols, ax_idx,
                                             projection='3d')
                        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                                        cmap=cm.jet,
                                        linewidth=0, antialiased=False)

                    else:
                        ax = fig.add_subplot(ax_rows, ax_cols, ax_idx)
                        p = ax.pcolor(X, Y, Z.T, antialiased=False,
                                      cmap=cm.RdBu)
                        if args.colorbar:
                            fig.colorbar(p, fraction=0.05, aspect=30)

                    ax.autoscale(tight=True)

            #
            # Add plot title, labels and legend
            #
            if args.title and len(args.title) > 0:
                ax.set_title(args.title)

            if args.x_label and len(args.x_label) > 0:
                ax.set_xlabel(args.x_label)

            if args.y_label and len(args.y_label) > 0:
                ax.set_ylabel(args.y_label)

            if args.legends and len(args.legends) > 0:
                ax.legend(args.legends.split(","), loc='best')

            ax_idx = ax_idx + 1

    #
    # save and/or display figure
    #
    if args.output_file and len(args.output_file):
        if args.output_format and len(args.output_format):
            fig.savefig(args.output_file, format=args.output_format)
        else:
            fig.savefig(args.output_file)

    if not args.quiet:
        plt.show()


if __name__ == "__main__":
    main()
