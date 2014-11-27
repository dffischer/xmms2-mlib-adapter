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

    def exec(self, db, file, rejects):
        with ExitStack() as stack:
            def prepare_writer(file):
                stack.push(file)
                writer = DictWriter(file, fields)
                writer.writeheader()
                return writer
            if rejects:
                handle_missing = prepare_writer(rejects).writerow
            else:
                def handle_missing(row):
                    print("\033[K\r{} is not in library".format(row[key]), file=stderr)

            pbar = progress_file(file, BracketBar(), Percentage())
            for row in DictReader(file):
                id = db.execute("SELECT id FROM Media WHERE key='{}' AND value='{}'"
                        .format(key, row[key])).fetchone()
                if id:
                    id = id[0]
                    for field in values:
                        db.execute(
                                "UPDATE Media SET value='{value}', intval={value} "
                                "WHERE key='{field}' AND id={id}"
                                .format(value=row[field], field=field, id=id))
                else:
                    handle_missing(row)
                pbar.update(file.buffer.tell())
            pbar.finish()

if __name__ == '__main__':
    Restore().run()
