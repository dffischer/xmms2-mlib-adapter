#!/usr/bin/python
# import.py
"""Imports m3u-Playlists - textfiles with one song path per line - into xmms2."""

from .program import MedialibProgram, MultiFileProgram
from os.path import basename, splitext
from .progress import FileProgress, LabeledProgress
from .fields import idquery

class MultifileProgress(FileProgress, LabeledProgress):
    pass

class Import(MedialibProgram, MultiFileProgram):
    def __init__(self):
        super().__init__('r', """Lists the files to import playlists from. When no file or
                - is given, data is expected from the standard input.""", "import xmms2 playlists",
                epilog="""When a path cannot be found, it is searched without the prefix
                subsequently. So this program can import playlists composed of paths with
                and without prefix mixed. Contrary \fBxmms2-playlist-export\fP refuses to
                generate such, instead rejecting every path that does not start with the
                specified prefix. To generate a mixed export, do not use the -p option when
                exporting, but instead pipe the resulting m3u through "sed 's/^prefix//' to
                remove it only when present, silently ignoring songs lacking the prefix.""")
        self.add_argument("-n", "--name", metavar="name", default="{name}", help=
                "Select a name for the imported playlists. To name multiple imported lists, "
                "the templates {file}, {name} and {ext} will be replaced with the full filename, "
                "the same stripped from its extension and the extension only, respectively.")

    def exec(self, db, prefix, file, name):
        name = self.format_name(name, file)
        pbar = MultifileProgress(file, name)
        id = db.execute("INSERT INTO CollectionOperators (type) VALUES (9);").lastrowid
        db.execute("INSERT INTO CollectionLabels VALUES ({id}, 1, '{name}');".format(
            id=id, name=name))
        db.execute("INSERT INTO CollectionAttributes VALUES ({}, 'position', -1);".format(id))
        def inform(key):
            return db.execute(idquery(key)).fetchone()
        for position, url in enumerate(file):
            url = url.strip()
            info = inform(prefix.prepend(url)) or inform(url)
            if info:
                db.execute("INSERT INTO CollectionIdlists VALUES ({}, {}, {});"
                        .format(id, position, info["id"]))
            else:
                self.warn(url, "not found in library")
            pbar.step()
        pbar.finish()

    @staticmethod
    def format_name(name, file):
        filename = basename(file.name)
        list, ext = splitext(filename)
        return name.format(file=filename, name=list, ext=ext[1:])


if __name__ == '__main__':
    Import().run()
