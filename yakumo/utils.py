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

import argparse
import os
import rlcompleter
import re
import sys

import os_client_config
import yakumo


ENVIRONMENT_VARIABLES = {
    'os_cloud': 'OS_CLOUD',
    'os_cert': 'OS_CERT',
    'os_cacert': 'OS_CACERT',
    'os_region_name': 'OS_REGION_NAME',
    'os_interface': 'OS_INTERFACE',
    'os_key': 'OS_KEY',
    'os_auth_type': 'OS_AUTH_TYPE',
}


def get_client():
    kwargs = {dest: os.environ.get(env)
              for dest, env in ENVIRONMENT_VARIABLES.items()}
    parser = argparse.ArgumentParser()
    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)
    for opt in parser._actions:
        if opt.dest in ENVIRONMENT_VARIABLES:
            opt.metavar = ENVIRONMENT_VARIABLES[opt.dest]
    parser.set_defaults(timeout=None, insecure=False, **kwargs)
    options = parser.parse_args()
    return yakumo.Client(**options.__dict__)


def join_path(*args):
    return '/'.join([str(x).strip('/') for x in args if x is not None])


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


class Completer(rlcompleter.Completer):

    PATTERN = re.compile(r"(\w+(\.\w+)*)\.(\w*)")

    def attr_matches(self, text):
        """
        Derived from rlcompleter.Completer.attr_matches()
        """
        m = self.PATTERN.match(text)
        if not m:
            return []
        expr, attr = m.group(1, 3)
        try:
            thisobject = eval(expr, self.namespace)
        except Exception:
            return []

        # get the content of the object, except __builtins__
        words = dir(thisobject)
        if "__builtins__" in words:
            words.remove("__builtins__")

        if hasattr(thisobject, '__class__'):
            words.append('__class__')
            words.extend(rlcompleter.get_class_members(thisobject.__class__))
        matches = []
        n = len(attr)
        for word in words:
            if attr == '' and word[0] == '_':
                continue
            if word[:n] == attr and hasattr(thisobject, word):
                val = getattr(thisobject, word)
                word = self._callable_postfix(val, "%s.%s" % (expr, word))
                matches.append(word)
        return matches
