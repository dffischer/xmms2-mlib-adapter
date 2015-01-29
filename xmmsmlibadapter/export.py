#!/usr/bin/python
# export.py
"""Exports playlists to plain text files - which are indeed m3u8-Playlists."""

from .program import MedialibProgram
from .fields import key
from .progress import LabeledProgress
from argparse import FileType
from functools import partial
from contextlib import ExitStack
from .cache import Cache

class Export(MedialibProgram):
    def __init__(self):
        super().__init__(epilog="""Only collections of the type idlist can be exported. If you
                do not know what this means, you probably do only have exportable playlists.""")
        self.add_argument("playlists", metavar="playlist", nargs="*", help="""Select playlists
                for export. When no playlist is selected, all of them will be exported.""")
        self.add_argument("-o", "--out", metavar="outfile.m3u", default='{name}.m3u8', help="""
                Write to a given file. As multiple playlists are likely to be processed,
                this is treated as a pattern wherein {name} will be replaced by the name
                of the playlist. Defaults to %(default)s. - directs to the standard
                output. Note that this will append multiple playlists into one.""")

    def exec(self, db, prefix, playlists, out, **kwargs):
        if not playlists:
            playlists = {row["name"]: row["id"] for row in db.execute(
                "SELECT id, name "
                "FROM CollectionOperators JOIN CollectionLabels ON id=collid "
                "WHERE type = 9;")}
        else:
            ids = {row["name"]: row["id"] for row in db.execute(
                "SELECT id, name "
                "FROM CollectionOperators JOIN CollectionLabels ON id=collid "
                "WHERE type = 9 AND name IN ({});"
            .format(str(playlists).strip('[]')))}
            for playlist in playlists:
                if playlist not in ids:
                    self.warn(playlist, "not a list of songs")
            playlists = ids
        with ExitStack() as stack:
            open = Cache(partial(
                lambda open, filename: stack.push(open(filename)),
                FileType('w')))
            for playlist, id in playlists.items():
                nsongs = db.execute("SELECT COUNT(mid) FROM CollectionIdlists WHERE collid='{}';"
                        .format(id)).fetchone()[0]
                if nsongs < 1:
                    self.warn(playlist, "empty")
                else:
                    target = open(out.format(name=playlist))
                    pbar = LabeledProgress(playlist, maxval=nsongs)
                    for row in db.execute(
                            "SELECT value as {key}, position "
                            "FROM CollectionIdlists JOIN Media on id=mid "
                            "WHERE key='{key}' AND collid='{id}' "
                            "ORDER BY position ASC".format(key=key, id=id)):
                        try:
                            print(prefix.remove(row[key]), file=target)
                        except ValueError:
                            self.reject(row, "lacking prefix")
                        pbar.update(row["position"])
                    pbar.finish()


if __name__ == '__main__':
    Export().run()
