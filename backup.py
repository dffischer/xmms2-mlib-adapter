#!/usr/bin/python
# backup.py
"""Backs up song statistics - timesplayed and laststarted
- from an xmms2 media library to a csv file."""

from fields import key, values, fields, MLibCSVAdapter, infoquery
from csv import DictWriter
from progress import OrderlyProgress

def exec(db, file):
    out = DictWriter(file, fields, extrasaction='ignore')
    out.writeheader()
    pbar = OrderlyProgress(db.execute(
        "SELECT COUNT(DISTINCT id) FROM Media WHERE key='{}';".format(fields[1]))
        .fetchone()[0])
    for row in db.execute(infoquery):
        out.writerow(row)
        pbar.step()
    pbar.finish()

if __name__ == '__main__':
    MLibCSVAdapter('w', "Write to a given file instead of the standard output.").run(exec)
