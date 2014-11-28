#!/usr/bin/python
# export.py
"""Exports playlists to plain text files - which are indeed m3u8-Playlists."""

from utils import MedialibProgram
from sys import stdout, stderr
from progress import LabeledProgress

class Export(MedialibProgram):
    def __init__(self):
        super().__init__(epilog="""Only collections of the type idlist can be exported. If you
                do not know what this means, you probably do only have exportable playlists.""")
        self.add_argument("playlists", metavar="playlist", nargs="*", help="""Select playlists
                for export. When no playlist is selected, all of them will be exported.""")
        self.add_argument("-o", "--out", default='{name}.m3u8', help="""
                Write to a given file. For multiple playlists, this is treated as a pattern wherein
                {name} will be replaced by the name of the playlist. Defaults to {name}.m3u8.""")
        self.add_argument("-s", "--stdout", action='store_const', dest='out', const="-", help="""
                Write to a stdout instead of a file. This has the exact same effect as specifing an
                output filename of -. Note that this will append multiple playlists into one.""")

    def exec(self, db, playlists, out, **kwargs):
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
                    print(playlist + " is not a list of songs", file=stderr)
            playlists = ids
        if out == "-":
            def process(playlist):
                export(stdout)
        else:
            def process(playlist):
                with open(out.format(name=playlist), 'w') as file:
                    export(file)
        for playlist, id in playlists.items():
            nsongs = db.execute("SELECT COUNT(mid) FROM CollectionIdlists WHERE collid='{}';"
                    .format(id)).fetchone()[0]
            if nsongs < 1:
                print(playlist + " is empty", file=stderr)
            else:
                pbar = LabeledProgress(playlist, maxval=nsongs)
                def export(target):
                    for row in db.execute(
                            "SELECT value, position "
                            "FROM CollectionIdlists JOIN Media on id=mid "
                            "WHERE key='url' AND collid='{}' "
                            "ORDER BY position ASC".format(id)):
                        print(row["value"], file=target)
                        pbar.update(row["position"])
                process(playlist)
                pbar.finish()


if __name__ == '__main__':
    Export().run()
