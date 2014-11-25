#!/usr/bin/python
# fields.py
"""Fields and their types to backup and restore."""

key = "url"
values = {"timesplayed", "laststarted"}
fields = tuple([key] + sorted(values))

from utils import MedialibProgram, SingleFileProgram
class MLibCSVAdapter(MedialibProgram, SingleFileProgram):
    def __init__(self, mode, filedesc):
        super().__init__(mode, filedesc, ext=".csv")


from itertools import starmap, repeat

def mapformat(format, *args):
    return map(format.format, *args)

infoquery = "SELECT {key}.id as id, {key}.value as {key}, {values} FROM {tables} " \
        "WHERE {join} AND {keys};".format(
                key=key,
                values=", ".join(mapformat("{0}.intval as {0}", values)),
                tables=", ".join(mapformat("Media {}", fields)),
                keys=" AND ".join(mapformat("{0}.key = '{0}'", fields)),
                join=" AND ".join(mapformat("{}.id = {}.id", repeat(key), values)))
