#!/usr/bin/python
#
# Copyright 2014,2015 by Akira Yoshiyama <akirayoshiyama@gmail.com>.
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


import argparse
import os
from pprint import pprint
import sys

import os_client_config
import pbr

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


def main():
    kwargs = {dest: os.environ.get(env)
              for dest, env in ENVIRONMENT_VARIABLES.items()}
    parser = argparse.ArgumentParser()
    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)
    for opt in parser._actions:
        if opt.dest in ENVIRONMENT_VARIABLES:
            opt.metavar = ENVIRONMENT_VARIABLES[opt.dest]
    parser.set_defaults(timeout=None, insecure=False, **kwargs)
    parser.add_argument('--version', help='Print version and exit',
                        action='store_true')
    parser.add_argument('--verbose', help='Verbose output',
                        action='store_true')

    options = parser.parse_args()
    if options.version:
        print(pbr.version.VersionInfo('yakumo'))
        sys.exit(0)

    c = yakumo.Client(**options.__dict__)

    local_vars = locals()
    local_vars['pprint'] = pprint
    try:
        import bpython
        bpython.embed(locals_=local_vars)
    except ImportError:
        try:
            import code
            import readline
            readline.parse_and_bind("tab:complete")
        except ImportError:
            pass
        code.interact(None, None, local_vars)

if __name__ == '__main__':
    main()
