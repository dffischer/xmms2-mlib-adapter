"""useful context managers to postpone optional execution"""

class Finalize(object):
    """A Context Manager that executes a given callback on exit."""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.func(*self.args, **self.kwargs)

class Optional(object):
    """The underlying exit procedure will only be executed when activated explicitly."""
    active = False

    def activate(self):
        self.active = True

    def __exit__(self, *args):
        if self.active:
            super().__exit__(*args)

class MaybeCallback(Optional, Finalize):
    pass

