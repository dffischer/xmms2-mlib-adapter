#!/usr/bin/python
# import.py
"""Imports m3u-Playlists - textfiles with one song path per line - into xmms2."""

from utils import MedialibProgram, MultiFileProgram
from os.path import basename, splitext
from progress import progress_file, FixedLabel, BracketBar
from progressbar import Percentage

class Import(MedialibProgram, MultiFileProgram):
    def __init__(self):
        super().__init__('r', """
                Lists the files to import playlists from. When no file or
                - is given, data is expected from the standard input.""")
        self.add_argument("-n", "--name", metavar="name", default="{name}", help=
                "Select a name for the imported playlists. To name multiple imported lists, "
                "the templates {file}, {name} and {ext} will be replaced with the full filename, "
                "the same stripped from its extension and the extension only, respectively.")

    def exec(self, db, file, name):
        name = self.format_name(name, file)
        pbar = progress_file(file, FixedLabel(name), BracketBar(), Percentage())
        id = db.execute("INSERT INTO CollectionOperators (type) VALUES (9);").lastrowid
        db.execute("INSERT INTO CollectionLabels VALUES ({id}, 1, '{name}');".format(
            id=id, name=name))
        db.execute("INSERT INTO CollectionAttributes VALUES ({}, 'position', -1);".format(id))
        for position, url in enumerate(file):
            db.execute("""INSERT INTO CollectionIdlists VALUES ({id}, {position},
                (SELECT id FROM Media WHERE key='url' AND value='{url}'));"""
                .format(id=id, position=position, url=url.strip()))
            pbar.update(file.buffer.tell())
        pbar.finish()

    @staticmethod
    def format_name(name, file):
        filename = basename(file.name)
        list, ext = splitext(filename)
        return name.format(file=filename, name=list, ext=ext[1:])


if __name__ == '__main__':
    Import().run()
