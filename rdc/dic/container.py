# -*- coding: utf-8 -*-
#
# Author: Romain Dorgueil <romain@dorgueil.net>
# Copyright: © 2011-2013 SARL Romain Dorgueil Conseil
#

from rdc.dic.reference import Reference
from rdc.dic.scope import Scope, CachedScope


class Container(object):
    def __init__(self):
        self.refs = {}
        self.parameters = {}
        self.scopes = {
            'prototype': Scope(),
            'container': CachedScope(),
            }

    def define(self, name, factory, *args, **kwargs):
        if name in self.refs:
            raise KeyError('Service container already have a definition for "{0}".'.format(name))

        scope_name = kwargs.pop('scope', 'container')
        scope = self.scopes[scope_name]
        calls = kwargs.pop('calls', None)
        self.refs[name] = scope.define(name, factory, args, kwargs, calls)
        self.refs[name]._repr = repr(factory)
        self.refs[name]._scope = scope_name
        return self.refs[name]

    def definition(self, prefix, *args, **kwargs):
        def decorator(factory):
            return self.define('.'.join(filter(None, [prefix, factory.__name__])), factory, *args, **kwargs)
        return decorator

    def set_parameter(self, name, value):
        if name in self.refs:
            raise KeyError('Service container already have a definition for "{0}".'.format(name))

        self.parameters[name] = value
        self.refs[name] = Reference(self.parameters.get, name)
        self.refs[name]._repr = repr(value)
        return self.refs[name]

    def set_parameters(self, parameters):
        return [self.set_parameter(name, value) for name, value in parameters.iteritems()]

    def ref(self, name):
        return self.refs[name]

    def get(self, name):
        return self.ref(name)()
