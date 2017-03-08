#!/usr/bin/env python
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
"""Compute API Test (Key Pairs)"""


import os
import time

from yakumo.smoketest import *
from yakumo import utils


PUBLIC_KEY = os.environ.get('HOME', '') + "/.ssh/id_rsa.pub"


def main(c, **kwargs):

    LOG.info("Create Key Pair #1")
    name = get_random_str('keypair')
    private_key_file = "/tmp/%s.pem" % name
    with c.key_pair.create(name=name, private_key_file=private_key_file) as k1:

        LOG.debug("list key pairs: %s", [_.name for _ in c.key_pair.list()])

        test("Key Pair #1: name is " + name, k1.name == name)
        LOG.debug("public key: %s", k1.public_key)
        LOG.debug("private key: %s", k1.private_key)
        test("Key Pair #1: public key is provided", len(k1.public_key) > 0)
        test("Key Pair #1: private key is provided", len(k1.private_key) > 0)

        with open(private_key_file) as f:
            private_key = f.read()
            test("Key Pair #1: private key is saved",
                 private_key == k1.private_key)

    test("Key Pair #1 is deleted", k1 not in c.key_pair.list())

    LOG.info("Create Key Pair #2")
    name = get_random_str('keypair')
    with open(PUBLIC_KEY) as f:
        public_key = f.read()
        public_key.strip()

    with c.key_pair.create(name=name, public_key=public_key) as k2:
        LOG.debug("list key pairs: %s", [_.name for _ in c.key_pair.list()])

        test("Key Pair #2: name is " + name, k2.name == name)
        LOG.debug("public key: %s", k2.public_key)
        LOG.debug("private key: %s", k2.private_key)
        test("Key Pair #2: public key is the same",
             k2.public_key == public_key)
        test("Key Pair #2: private key is not provided",
             k2.private_key is None)

    test("Key Pair #2 is deleted", k2 not in c.key_pair.list())


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list key pairs: %s", [_.name for _ in c.key_pair.list()])
    main(c)
    LOG.debug("list key pairs: %s", [_.name for _ in c.key_pair.list()])

    show_test_summary()
