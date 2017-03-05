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
"""Compute API Test (Server Metadata)"""


import time

from yakumo.smoketest import *
from yakumo import utils


KEY_PAIR_NAME = 'key1'
FLAVOR_NAME = 'm1.small'
IMAGE_NAME = 'cirros'
NETWORK_NAME = 'private'


def main(c, key_pair=None, flavor=None, image=None, network=None, **kwargs):

    LOG.debug("key pair: %s", key_pair)
    LOG.debug("flavor: %s", flavor)
    LOG.debug("image: %s", image)
    LOG.debug("network: %s", network)

    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    LOG.info("Metadata: %s", metadata)

    LOG.info("Create Server #1")
    name = get_random_str('server')
    with c.server.create(name=name,
                         networks=[network],
                         image=image,
                         flavor=flavor,
                         metadata=metadata,
                         key_pair=key_pair) as s:

        LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

        LOG.debug("wait for created")
        s.wait_for_finished()
        test("Server #1 name is " + name, s.name == name)
        test("Server #1 is active", s.status == 'ACTIVE')

        LOG.info("Metadata: %s", s.metadata)
        test("Metadata has %s" % metadata, s.metadata == metadata)

        m = {'foo2': 'bar4', 'foo3': 'bar3'}
        metadata.update(m)
        s.set_metadata(**m)
        LOG.info("Metadata: %s", s.metadata)
        test("Metadata has %s" % metadata, s.metadata == metadata)

        m = ['foo', 'foo2']
        for key in m:
            metadata.pop(key)
        s.unset_metadata(*m)
        LOG.info("Metadata: %s", s.metadata)
        test("Metadata has %s" % metadata, s.metadata == metadata)

    test("Server #1 is deleted", s not in c.server.list())


if __name__ == '__main__':
    c = utils.get_client()

    k = c.key_pair.find_one(name=KEY_PAIR_NAME)
    f = c.flavor.find_one(name=FLAVOR_NAME)
    i = c.image.find_one(name=IMAGE_NAME)
    n = c.network.find_one(name=NETWORK_NAME)

    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    main(c, key_pair=k, flavor=f, image=i, network=n)
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

    show_test_summary()
