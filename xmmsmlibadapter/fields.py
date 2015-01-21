#!/usr/bin/python
# fields.py
"""Fields and their types to backup and restore."""

key = "url"
values = {"timesplayed", "laststarted"}
fields = tuple([key] + sorted(values))


from utils import MedialibProgram, SingleFileProgram, CLProgram

class MLibCSVAdapter(MedialibProgram, SingleFileProgram):
    def __init__(self, mode, filedesc):
        super().__init__(mode, filedesc, ext=".csv")

    @staticmethod
    def reject(row, message):
        CLProgram.warn(row[key], message)
MedialibProgram.reject = staticmethod(MLibCSVAdapter.reject)


from itertools import starmap, repeat

def sql_compose(separator, format, *args):
    return separator.join(map(format.format, *args))

infoquery = "SELECT {key}.id as id, {key}.value as {key}, {values} FROM {tables} " \
        "WHERE {join} AND {keys};".format(
                key=key,
                values=sql_compose(", ", "{0}.intval as {0}", values),
                tables=sql_compose(", ", "Media {}", fields),
                keys=sql_compose(" AND ", "{0}.key = '{0}'", fields),
                join=sql_compose(" AND ", "{}.id = {}.id", repeat(key), values))
idquery = "SELECT id FROM Media WHERE key='{}' AND value='{{}}'".format(key).format
