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
from pprint import pprint
import sys

import os_client_config

import yakumo


def main():
    parser = argparse.ArgumentParser()
    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)

    parser.set_defaults(os_interface=None, os_auth_type=None,
                        timeout=None, insecure=False)
    options = parser.parse_args()
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
