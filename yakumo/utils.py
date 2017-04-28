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
