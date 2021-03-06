# xmms2-mlib-adapter

These tools transfer data between xmms2 media libraries. They operate directly on the library instead of connecting to xmms2 as a client. That means that they are able to [rescue data from broken libraries](rescue.md) or merge data from multiple databases into one. They can also be used to simply backup your data in an easy to read text format.

For further information, call them with the parameter `-h`.


## Installation

You can use the modules right away, or install them using [waf](https://code.google.com/p/waf/). If you already have waf installed with your distribution, you can just `waf configure install`. If you do not have waf installed, execute

```bash
wget -O waf http://ftp.waf.io/pub/release/waf-1.8.6
chmod 755 waf
./waf configure install
```

Archlinux users have [a package in the AUR](https://aur.archlinux.org/packages/python-xmms2-mlib-adapter-git/). To use the [PKGBUILD](PKGBUILD) as it is kept in this repository, [the makepkg-template for git](https://github.com/dffischer/git-makepkg-template) has to be installed.


## XMMS Version

These programs work with the sqlite3 database format used by xmms2 up until version 0. DrO_o. This is [the stable  version](https://github.com/XMMS2/xmms2-stable) by the time this was written. It will not work with [the s4 format](https://github.com/XMMS2/s4) used since DrParnassus, yet unreleased but already available through [the xmms2-devel repository](https://github.com/XMMS2/xmms2-devel).

You can check your version by executing `xmms2 server stats`

Porting to s4 would mean a complete rewrite, as there are no python bindings for s4 available at the moment.
