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

from functools import partial


class Reference(partial):
    def __init__(self, func, *args, **keywords):
        self._repr = None
        self._scope = None
        super(Reference, self).__init__(func, *args, **keywords)

    @classmethod
    def dereference(cls, ref_or_val):
        while isinstance(ref_or_val, Reference):
            ref_or_val = ref_or_val()
        return ref_or_val

    def __repr__(self):
        if self._repr is not None:
            r = self._repr
        else:
            r = super(Reference, self).__repr__()

        if self._scope is not None:
            return '{0} ({1})'.format(r, self._scope)
        else:
            return r



