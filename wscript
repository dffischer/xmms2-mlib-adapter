#! /usr/bin/env python

APPNAME = "xmms2 media library adapters"

from collections import OrderedDict
from manpager.markup import bold

def options(ctx):
    ctx.load('manpyger')

def configure(ctx):
    ctx.load('manpyger')
    ctx.check_python_version()
    ctx.check_python_module('progressbar')

def build(ctx):
    ctx(features="py", root="xmmsmlibadapter")
    binaries = ("xmms2-lib-backup", "xmms2-lib-restore",
            "xmms2-playlist-import", "xmms2-playlist-export")
    for binary in binaries:
        ctx(features="entrypynt",
                starter="xmmsmlibadapter." + binary.rpartition('-')[2], target=binary,
                extra=OrderedDict((
                    ("SEE ALSO", ', '.join(
                        bold(ref) + "(1)" for ref in binaries if ref is not binary)),
                    ("AUTHORS", """The xmms2 media library adapters were initially
                    developed by XZS <d.f.fischer@web.de>.\n\n\nThe code lives on
                    github <http://github.com/dffischer/xmms2-mlib-adapters>."""))))
