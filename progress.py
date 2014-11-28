#!/usr/bin/python
# progress.py
"""progress bar utilities"""

from progressbar import ProgressBar, Widget, SimpleProgress, Bar, Percentage, Counter, UnknownLength
from io import SEEK_END
from itertools import islice


# ----- Widgets -----

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


# ----- Bars -----

def entwine(iterable, seperator):
    for element in iterable:
        yield seperator
        yield element

def intersperse(iterable, seperator):
    return islice(entwine(iterable, seperator), 1, None)

class OrderlyProgress(ProgressBar):
    """Base class for custom tailored progress bars. Separates its widgets by spaces."""
    progress = SimpleProgress
    def bar(self):
        return BracketBar(), self.progress()
    def __init__(self, maxval=UnknownLength, widgets=(), progress=SimpleProgress):
        super().__init__(widgets=tuple(intersperse(widgets + self.bar(), ' ')), maxval=maxval)
        self.start()
    def step(self):
        self.update(self.currval + 1)

class LabeledProgress(OrderlyProgress):
    """Prepends a label in front of the bar and fixes all text
    so that multiple bars atop of each other still look neat."""
    progress = FixedProgress
    def __init__(self, name, widgets=(), *args, **kwargs):
        super().__init__(widgets=(FixedLabel(name), ) + widgets, *args, **kwargs)

class FileProgress(OrderlyProgress):
    """Progresses the reading status of a file."""
    progress = Percentage
    def __init__(self, file, *args, **kwargs):
        if file.seekable():
            position = file.tell()
            super().__init__(maxval=file.seek(0, SEEK_END) + 1, *args, **kwargs)
            file.seek(position)
            self.step = lambda: self.update(file.buffer.tell())
        else:
            self.bar = lambda: (Counter('%i entries processed'), )
            super().__init__(*args, **kwargs)
