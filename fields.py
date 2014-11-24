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
