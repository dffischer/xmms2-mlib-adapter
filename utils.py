#!/bin/python
# utils.py
"""Utilities to create programs that transfer data between xmms2 media libraries and files."""

from argparse import ArgumentParser, FileType
from sys import modules
from os.path import expanduser
from sqlite3 import connect, Row

class CLProgram(ArgumentParser):
    """Command-line program"""

    def __init__(self, *args, **kwargs):
        super().__init__(description=modules[__name__].__doc__, *args, **kwargs)

    def run(self, exec=None):
        if exec:
            self.exec = exec
        self.process(**vars(self.parse_args()))

    def process(self, **kwargs):
        self.exec(**kwargs)


class MedialibProgram(CLProgram):
    """Program working with xmms2 media libraries."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("-l", "--library", default=expanduser("~/.config/xmms2/medialib.db"),
                help="Use a given library instead of %(default)s.")

    def process(self, library, **kwargs):
        with connect(library) as db:
            db.row_factory = DictRow
            super().process(db=db, **kwargs)

class DictRow(Row):
    """makes the database Row more resemble a mapping type"""
    def get(self, index, default=None):
        try:
            return self[index]
        except KeyError:
            return default

class FileProgram(CLProgram):
    """Program working with files."""

class SingleFileProgram(FileProgram):
    """Program working with one file or standard streams."""

    def __init__(self, mode, filedesc, ext="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("file", metavar="file" + ext, nargs="?",
                type=FileType(mode), default="-", help=filedesc)

    def process(self, file, **kwargs):
        with file:
            super().process(file=file, **kwargs)

class MultiFileProgram(FileProgram):
    """Program working with multiple files or standard stream."""

    nargs='*'

    def __init__(self, mode, filedesc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        action=FileType(mode)
        self.add_argument(
                "files", metavar="file", nargs='*',
                type=action, default=[action("-")],
                help=filedesc)

    def process(self, files, **kwargs):
        for file in files:
            with file:
                super().process(file=file, **kwargs)

