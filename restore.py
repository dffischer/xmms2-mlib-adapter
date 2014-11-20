#!/bin/python
# restore.py
"""Restores song statistics - timesplayed and laststarted
- from a csv file into an xmms2 media library."""

from fields import *
from csv import DictReader

updates = {
    'value': "UPDATE Media SET value='{value}' WHERE key='{field}' AND id={id}",
    'intval': "UPDATE Media SET value='{value}', intval={value} WHERE key='{field}' AND id={id}"
}

def exec(db, file):
    for row in DictReader(file):
        id = db.execute("SELECT id FROM Media WHERE key='{}' AND {}='{}'"
                .format(key, types[key], row[key])).fetchone()[0]
        for field in values:
            db.execute(updates[types[field]].format(value=row[field], field=field, id=id))

if __name__ == '__main__':
    MLibCSVAdapter('r', "Read from a given file instead of the standard input.").run(exec)
