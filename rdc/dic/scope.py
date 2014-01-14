# -*- coding: utf-8 -*-
#
# Copyright 2012-2014 Romain Dorgueil
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rdc.dic.reference import Reference


class Scope(object):
    """
    Service scope that returns  a new instance for a given service each time get(service_name) is called.
    """

    def __init__(self, container=None):
        self.container = container
        self.definitions = {}

    def define(self, name, factory, args=None, kwargs=None, calls=None):
        """Create definition and return a callable getter."""
        self.definitions[name] = (factory, args, kwargs, calls, )
        return self.ref(name)

    def build(self, name):
        """Create an instance."""
        # get definition
        factory, args, kwargs, calls = self.definitions[name]
        # defaults and dereferencing
        args, kwargs = map(Reference.dereference, args or ()), dict((_k, Reference.dereference(_v)) for _k, _v in (kwargs or {}).iteritems())
        # build
        return Reference.dereference(factory)(*args, **kwargs)

    def ref(self, name):
        return Reference(self.build, name)


class CachedScope(Scope):
    """
    Service scope that returns the same instance for a given service each time get(service_name) is called.
    """

    def __init__(self, container=None):
        super(CachedScope, self).__init__(container)
        self.services = {}

    def get(self, name):
        """Get in scope or build."""
        if not name in self.services:
            self.services[name] = self.build(name)
        return self.services[name]

    def ref(self, name):
        return Reference(self.get, name)
