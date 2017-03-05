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


import time

from yakumo.smoketest import *


k = c.key_pair.find_one()
LOG.debug("key pair: %s", k)

f = c.flavor.find_one(name='m1.small')
LOG.debug("flavor: %s", f)

i = c.image.find_one(name='cirros')
LOG.debug("image: %s", i)

n = c.network.find_one(name='private')
LOG.debug("network: %s", n)

az = c.availability_zone.get_empty('nova')
LOG.debug("availability zone: %s", az)

LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

metadata = {'foo': 'bar', 'foo2': 'bar2'}
LOG.info("Metadata: %s", metadata)

LOG.info("Create Server #1")
name = get_random_str('server')
with c.server.create(name=name,
                     networks=[n],
                     image=i,
                     flavor=f,
                     availability_zone=az,
                     metadata=metadata,
                     key_pair=k) as s:

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

LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
show_test_summary()
