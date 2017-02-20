# Copyright 2014-2017 by Akira Yoshiyama <akirayoshiyama@gmail.com>.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Miscellaneous functions/decorators
"""

import copy
import functools
import inspect


def join_path(*args):
    return '/'.join([str(x) for x in args if x is not None])


def get_json_body(base, **params):
    data = {}
    if not params:
        return {base: None}
    for key, value in params.items():
        if value is not None:
            data[key] = value
    if not data:
        data = None
    return {base: data}


def str2bool(value):
    if value == u'true':
        return True
    if value == u'false':
        return False


def bool2str(value):
    if value is True:
        return u'true'
    if value is False:
        return u'false'


def gen_chunk(file):
    with open(file, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            yield chunk
