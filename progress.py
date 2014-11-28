#!/usr/bin/python
# progress.py
"""progress bar utilities"""

from progressbar import ProgressBar, Widget, SimpleProgress, Bar, Percentage
from io import SEEK_END

def start_progress(maxval, *widgets):
    return ProgressBar(widgets=intersperse(widgets, ' '), maxval=maxval).start()

def entwine(iterable, seperator):
    for element in iterable:
        yield seperator
        yield element

def intersperse(iterable, seperator):
    return tuple(entwine(iterable, seperator))[1:]

def progress_file(file, *widgets):
    position = file.tell()
    bar = start_progress(file.seek(0, SEEK_END), *(widgets + (BracketBar(), Percentage())))
    file.seek(position)
    return bar

class FixedWidth(Widget):
    def __init__(self, width=15, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
    def update(self, pbar):
        return super().update(pbar)[:self.width].rjust(self.width)

class FixedProgress(FixedWidth, SimpleProgress):
    pass

class Label(Widget):
    __slots__ = ('text',)
    def __init__(self, text):
        self.text = text
    def update(self, pbar):
        return self.text

def FixedLabel(text, width=20):
    return Label(text[:width-3] + '...' if len(text) > width else text.ljust(width))

def BracketBar(*args, **kwargs):
    return Bar(left='[', right=']', *args, **kwargs)
