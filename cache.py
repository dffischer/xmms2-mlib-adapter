"""caching decorator and utilities"""

from functools import partial

class Cache(object):
    def __init__(self, func, cache={}):
        self.func = func
        self.cache = cache
    def __call__(self, key):
        try:
            return self.cache[key]
        except KeyError:
            value = self.func(key)
            self.cache[key] = value
            return value
    @classmethod
    def filled(cls, cache):
        return partial(cls, cache=cache)

null = type('Null', (object, ), {
    '__call__': lambda *k, **kw: None,
    '__getattribute__': lambda self, _: self,
    '__doc__': "unique lazy object that does nothing and only knows itself"
})()

