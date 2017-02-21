#!/usr/bin/python
#
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


import argparse
from contextlib import contextmanager
import logging
import os.path
import random
import sys

import os_client_config

from yakumo import Client, utils


__all__ = ('c', 'LOG', 'cleaner', 'get_random_str', 'test',
           'show_test_summary')

SOURCE = "abcdefghijklmnopqrstuvwxyz" \
         "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
         "0123456789"

TEST_LOGS = []

parser = argparse.ArgumentParser()
cloud_config = os_client_config.OpenStackConfig()
cloud_config.register_argparse_arguments(parser, sys.argv)
options = parser.parse_args()
c = Client(**options.__dict__)

LOG = logging.getLogger(os.path.basename(sys.argv[0]))
LOG.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
ch.setFormatter(formatter)
LOG.addHandler(ch)


@contextmanager
def cleaner(resource):
    try:
        yield resource
    except Exception as e:
        LOG.warning("Error occured: %s", e)
        TEST_LOGS.append((str(e), False))
    finally:
        if hasattr(resource, 'name'):
            LOG.info("Delete %s", resource.name)
        else:
            LOG.info("Delete %s", resource.get_id())
        resource.delete()
        LOG.debug("waiting for deleted")
        resource.wait_for_finished()


def get_random_str(prefix="test"):
    return prefix + "-" + "".join(random.sample(SOURCE, 10))


def test(label, condition):
    TEST_LOGS.append((label, condition))
    if condition:
        LOG.debug("%s ... OK", label)
    else:
        LOG.debug("%s ... NG", label)


def show_test_summary():
    _ok = 0
    _ng = 0
    for label, condition in TEST_LOGS:
        if condition:
            _ok += 1
        else:
            _ng += 1
    LOG.info("Test results: OK=%s, NG=%s" % (_ok, _ng))
    for label, condition in TEST_LOGS:
        if not condition:
            LOG.debug("NG: %s" % label)
