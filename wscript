#! /usr/bin/env python

def options(ctx):
    ctx.load('manpyger')

def configure(ctx):
    ctx.load('manpyger')
    ctx.check_python_version()
    ctx.check_python_module('progressbar')

def build(ctx):
    ctx(features="py entrypynt", root="xmmsmlibadapter", main="backup restore import export",
            target="xmms2-lib-backup xmms2-lib-restore xmms2-playlist-import xmms2-playlist-export")
