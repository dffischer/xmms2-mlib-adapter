# Library Rescue

Xmms2 crashed or even your whole machine froze while some data was written to the library and left it unreadable. You usually notice this when after the next startup, there is just one playlist with the default demo song. You may now think all data is lost forever. But falter not. There may be rescue. The following steps describe how you can possibly regenerate large parts of the data.

All following code snippets assume that the adapters [are already installed](README.md#Installation).


## Locating the corrupt library

First, we need to go to the place where xmms2 stores its media library. This is normally `~/.config/xmms2`. Some distribution start xmms2 as a dedicated user. Then, the directory is located in the home directory of that user. Its name is most probably noted in a configuration file like `/etc/conf.d/xmms2.conf`. Open a terminal and go there.

```bash
$ cd ~/.conf/xmms2
$ ls
bindata  clients  medialib.db  medialib.db.old  shutdown.d  startup.d  xmms2.conf
```

If there is a file called `medialib.db.old`, you are lucky. This is the damaged library that xmms2 was unable to read. It created a new one (`medialib.db`) and retained the old one there.


## Cleaning the corrupt library

We now have to clean the corrupt library from any errors. This means sacrificing damaged entries for the sake of making the database readable again. First, we export the database to SQL statements.

```bash
$ sqlite3 medialib.db ".dump" > dump
$ nano dump
```

Now, we open the file in any text editor and skim through it. Looking about the file, you also get an impression of how much data was still readable. The data of roughly all the songs that show up here can be fully recovered. All lost entires show up as error messages. Even if you are unfamiliar with SQL, you should be able to tell the lines apart by the \*\*\*. Remove all of them, then save the file. Next, we compose a new library for the healthy entries left over.

```bash
$ sqlite3 -init dump medialib.db.new ".quit"
```

But we cannot give this database to xmms2 yet, as it may have partial entries that the player will overwrite or cannot even handle. Instead, we will have xmms2 create a new database and then move song statistics over.


## Creating and filling a new library

Start up xmms2 and give it a few moments to scan your song collection. You can also direct it to folders or files to include. Make sure to include every song that was in the old library.

```bash
$ xmms2 list  # start the daemon. It should scan your Music folder automatically. Give it a moment.
$ xmms2 server import /path/to/more/music
$ xmms2 search '*'  # Does this show up all your songs yet? If yes, you are good to go on.
```


## Adding information from the old library

Lastly, we will take the song statistics from the old library to update the one just created. We do not want xmms2 to interfere while we are messing with its library, so turn it off before we start.

```bash
$ xmms2 server shutdown  
```

Now, we use the adapters to transfer data.

```
xmms2-lib-backup -l medialib.db.new | xmms2-lib-python -l medialib.db
```

If any errors show up, they most probably indicate that there was a song in the old library that you forgot to import in the last step. You can just go back there and add it, but do not forget to shut down xmms2 before executing the adapters again. Make at least sure that all songs contained in any playlists are present, as we will move these over next.

```bash
$ mkdir playlists
$ cd playlists
$ xmms2-playlist-export -l ../medialib.db.new
$ xmms2-playlist-import -l ../medialib.db *.m3u8
$ cd ..
```


## Finished

To check whether everything went fine, you may start up xmms2 again and ask it for the ten songs most played. Hopefully, you should recognize them very well. 

```bash
$ xmms2 search -o -timesplayed -l title,album,artist '*' | tail -n+3 | head | sed 's/ \+/ /g'
```

Last, we can clean away the corrupt library and all intermediates.

```bash
$ rm medialib.db.old medialib.db.new dump playlists
```
