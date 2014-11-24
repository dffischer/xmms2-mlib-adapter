#!/usr/bin/python
# restore.py
"""Restores song statistics - timesplayed and laststarted
- from a csv file into an xmms2 media library."""

from fields import *
from csv import DictReader
from progress import progress_file, BracketBar
from progressbar import Percentage

class Restore(MLibCSVAdapter):
    def __init__(self):
        super().__init__('r', "Read from a given file instead of the standard input.")

    def exec(self, db, file):
        pbar = progress_file(file, BracketBar(), Percentage())
        for row in DictReader(file):
            id = db.execute("SELECT id FROM Media WHERE key='{}' AND value='{}'"
                    .format(key, row[key])).fetchone()[0]
            for field in values:
                db.execute(
                        "UPDATE Media SET value='{value}', intval={value} WHERE key='{field}' AND id={id}"
                        .format(value=row[field], field=field, id=id))
            pbar.update(file.buffer.tell())
        pbar.finish()

if __name__ == '__main__':
    Restore().run()
