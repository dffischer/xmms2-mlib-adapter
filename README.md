# xmms2-mlib-adapter

These tools transfer data between xmms2 media libraries. They operate directly on the library instead of connecting to xmms2 as a client. That means that they are able to rescue data from broken libraries or merge data from multiple databases into one. They can also be used to simply backup your data in an easy to read text format.

For further information, call them with the parameter `-h`.

## XMMS Version

These programs work with the sqlite3 database format used by xmms2 up until version 0. DrO_o. This is [the stable  version](https://github.com/XMMS2/xmms2-stable) by the time this was written. It will not work with [the s4 format](https://github.com/XMMS2/s4) used since DrParnassus, yet unreleased but already available through [the xmms2-devel repository](https://github.com/XMMS2/xmms2-devel).

You can check your version by executing `xmms2 server stats`

Porting to s4 would mean a complete rewrite, as there are no python bindings for s4 available at the moment.
