# Copyright (C) 2011, Robert Johansson <robert@riken.jp>

TARGET=/home/rob/bin

all:
	echo "run make install"


install:
	install -m 755 enplot.py $(TARGET)/enplot
	install -m 644 libenplot.py $(TARGET)/libenplot.py
