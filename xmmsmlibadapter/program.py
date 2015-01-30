#!/usr/bin/python
# program.py
"""Utilities to create programs that transfer data between xmms2 media libraries and files."""

from argparse import ArgumentParser, FileType
from sys import modules, stderr
from os.path import expanduser
from sqlite3 import connect, Row


# ----- basic execution flow -----

class CLProgram(ArgumentParser):
    """Command-line program"""

    def __init__(self, short=None, *args, **kwargs):
        super().__init__(description=modules['__main__'].__doc__, *args, **kwargs)
        if short:
            self.short = short

    def run(self, exec=None):
        if exec:
            self.exec = exec
        self.process(**vars(self.parse_args()))

    def process(self, **kwargs):
        self.exec(**kwargs)

    @staticmethod
    def warn(item, message):
        print("\033[K\r", item, ': ', message, sep='', file=stderr)


# ----- media database handling -----

class Prefix(object):
    """prefix to append and remove from strings"""

    def __init__(self, str):
        self.str = str

    def prepend(self, str):
        return self.str + str

    def remove(self, str):
        if str.startswith(self.str):
            return str[len(self.str):]
        else:
            raise ValueError("prefix lacking")

    def __bool__(self):
        return bool(self.str)

class MedialibProgram(CLProgram):
    """Program working with xmms2 media libraries."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("-l", "--library", default=expanduser("~/.config/xmms2/medialib.db"),
                help="Use a given library instead of %(default)s.")
        self.add_argument("-p", "--prefix", type=Prefix, default="file://", help="""
                Prefix for song URLs to assume present in the library but ommitted in
                files. It will be stripped while exporting omitting entries without
                and added when needed while importing. Defaults to '%(default)s'.""")

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


# ----- working with files -----

class SingleFileProgram(CLProgram):
    """Program working with one file or standard streams."""

    def __init__(self, mode, filedesc, ext="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("file", metavar="file" + ext, nargs="?",
                type=FileType(mode), default="-", help=filedesc)

    def process(self, file, **kwargs):
        with file:
            super().process(file=file, **kwargs)

class MultiFileProgram(CLProgram):
    """Program working with multiple files or standard stream."""

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

