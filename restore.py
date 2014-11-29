#!/usr/bin/python
# restore.py
"""Restores song statistics - timesplayed and laststarted
- from a csv file into an xmms2 media library."""

from fields import *
from csv import DictReader, DictWriter
from progress import FileProgress
from argparse import FileType
from contextlib import ExitStack
from functools import partial
from cache import Cache, null
from context import MaybeCallback

class Restore(MLibCSVAdapter):
    def __init__(self):
        super().__init__('r', "Read from a given file instead of the standard input.")
        file = Cache(FileType('w'))
        self.add_argument("-r", "--rejects", metavar="rejects.csv",
                nargs="?", type=file, const=null, help="""
                Songs that could not be found in the library will not be added
                anew. Use this option without any filename to suppress errors
                about them. If you also specify a file, the entries will be
                written there unchanged. - directs to the standard output.""")
        self.add_argument("-u", "--update", metavar="uptodate.csv",
                nargs="?", type=file, const=null, help="""
                Only update values that are greater than their counterparts
                in the library. Values already up-to-date or less will be
                ignored, unless a filename is given in which case they are
                written there unchanged. - directs to the standard output.""")

    def exec(self, db, file, rejects, update):
        with ExitStack() as stack:
            @Cache.filled({null: null})
            def prepare_writer(file):
                stack.push(file)
                writer = DictWriter(file, fields)
                writer.writeheader()
                return writer
            worker = (partial(Update, prepare_writer(update).writerow) if update else Insert)(db,
                    prepare_writer(rejects).writerow if rejects else
                    partial(self.reject, message="not in library"))

            pbar = FileProgress(file)
            for row in DictReader(file):
                worker.process(row)
                pbar.step()
            pbar.finish()

class Insert(object):
    """Inserts values into the database unconditionally."""

    query = idquery

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

class Update(Insert):
    """Only inserts newer values."""

    query = infoquery[:-1] + " AND url.value = '{}'" + infoquery[-1]

    def __init__(self, old_handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handle_old = old_handler

    def update(self, info, newvals):
        with MaybeCallback(super().update, info, newvals) as write:
            for field in values:
                if info[field] > int(newvals[field]):
                    return self.handle_old(newvals)
                elif info[field] < int(newvals[field]):
                    write.activate()

if __name__ == '__main__':
    Restore().run()
