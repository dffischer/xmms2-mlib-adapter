#!/bin/python
# backup.py
"""Backs up song statistics - timesplayed and laststarted
- from an xmms2 media library to a csv file."""

from fields import *
from csv import DictWriter
from itertools import starmap, repeat

def mapformat(format, *args):
    return map(format.format, *args)

def exec(db, file):
    out = DictWriter(file, fields, extrasaction='ignore')
    out.writeheader()
    for row in db.execute("SELECT {fields} FROM {tables} WHERE {join} AND {keys}".format(
        fields=", ".join(starmap("{0}.{1} as {0}".format, types.items())),
        tables=", ".join(mapformat("Media {}", fields)),
        keys=" AND ".join(mapformat("{0}.key = '{0}'", fields)),
        join=" AND ".join(mapformat("{}.id = {}.id", repeat(key), values))
    )):
        out.writerow(row)

if __name__ == '__main__':
    MLibCSVAdapter('w', "Write to a given file instead of the standard output.").run(exec)
