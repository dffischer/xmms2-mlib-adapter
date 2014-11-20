#!/bin/python
# progress.py
"""progress bar utilities"""

from progressbar import ProgressBar
from io import SEEK_END

def start_progress(maxval, *widgets):
    return ProgressBar(widgets=widgets, maxval=maxval).start()

def progress_file(file, *widgets):
    position = file.tell()
    bar = start_progress(file.seek(0, SEEK_END), *widgets)
    file.seek(position)
    return bar
