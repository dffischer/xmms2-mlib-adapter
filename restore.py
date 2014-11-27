#!/usr/bin/python
# restore.py
"""Restores song statistics - timesplayed and laststarted
- from a csv file into an xmms2 media library."""

from fields import *
from csv import DictReader, DictWriter
from progress import progress_file, BracketBar
from progressbar import Percentage
from sys import stderr
from argparse import FileType
from contextlib import ExitStack
from functools import partial

null = type('Null', (object, ), {
    '__call__': lambda *k, **kw: None,
    '__getattribute__': lambda self, _: self,
    '__doc__': "Lazy object that does nothing and only knows itself"
})()

class Restore(MLibCSVAdapter):
    def __init__(self):
        super().__init__('r', "Read from a given file instead of the standard input.")
        file = FileType('w')
        self.add_argument("-r", "--rejects", metavar="rejects.csv",
                nargs="?", type=file, const=null, help="""
                Songs that could not be found in the library will not be added
                anew. Use this option without any filename to suppress errors
                about them. If you also specify a file, the entries will be
                written there unchanged. - directs to the standard output.""")

    @staticmethod
    def error(message, row):
        print("\033[K\r", row[key], ': ', message, sep='', file=stderr)

    def exec(self, db, file, rejects):
        with ExitStack() as stack:
            def prepare_writer(file):
                stack.push(file)
                writer = DictWriter(file, fields)
                writer.writeheader()
                return writer
            worker = Insert(db, prepare_writer(rejects).writerow if rejects else
                    partial(self.error, "not in library"))

            pbar = progress_file(file, BracketBar(), Percentage())
            for row in DictReader(file):
                worker.process(row)
                pbar.update(file.buffer.tell())
            pbar.finish()

class Insert(object):
    """Inserts values into the database unconditionally."""

    query = "SELECT id FROM Media WHERE key='{}' AND value='{{}}'".format(key)

    def __init__(self, db, missing_handler):
        self.db = db
        self.handle_missing = missing_handler

    def process(self, row):
        info = self.db.execute(self.query.format(row[key])).fetchone()
        if info:
            self.update(info, row)
        else:
            self.handle_missing(row)

    def update(self, info, newvals):
        for field in values:
            self.db.execute(
                    "UPDATE Media SET value='{value}', intval={value} "
                    "WHERE key='{field}' AND id={id}"
                    .format(value=newvals[field], field=field, id=info["id"]))

if __name__ == '__main__':
    Restore().run()
