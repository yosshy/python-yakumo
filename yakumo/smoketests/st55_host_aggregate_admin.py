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
"""Compute API Test (Host Aggregates)"""


import time

from yakumo.smoketest import *
from yakumo import utils


def main(c, **kwargs):

    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    LOG.info("Metadata: %s", metadata)

    hosts = [_.host for _ in c.nova.service.find(binary='nova-compute')]

    LOG.info("Create Aggregate #1")
    name = get_random_str('aggregate')
    with c.aggregate.create(name=name,
                            availability_zone='foo',
                            metadata=metadata) as a:

        LOG.debug("list aggregates: %s", [_.name for _ in c.aggregate.list()])

        test("Aggregate #1 name is " + name, a.name == name)
        test("Aggregate #1 is availability_zone",
             a.availability_zone == 'foo')

        LOG.debug("Initial metadata: %s", a.metadata)
        test("Metadata has %s" % metadata, a.metadata == metadata)

        m = {'foo2': 'bar4', 'foo3': 'bar3'}
        LOG.debug("Set metadata : %s", m)
        metadata.update(m)
        a.set_metadata(**m)
        LOG.debug("Updated metadata: %s", a.metadata)
        test("Metadata has %s" % metadata, a.metadata == metadata)

        m = ['foo', 'foo2']
        LOG.debug("Unset metadata : %s", m)
        for key in m:
            metadata.pop(key)
        a.unset_metadata(*m)
        LOG.debug("Updated metadata: %s", a.metadata)
        test("Metadata has %s" % metadata, a.metadata == metadata)

        LOG.debug("Initial hosts: %s", a.hosts)

        LOG.debug("Register hosts: %s", hosts)
        a.add_hosts(*hosts)
        LOG.debug("Updated hosts: %s", a.hosts)
        test("Aggregate has hosts: %s" % hosts, a.hosts == hosts)

        LOG.debug("Unregister hosts: %s", hosts)
        a.remove_hosts(*hosts)
        LOG.debug("Updated hosts: %s", a.hosts)
        test("Aggregate has no hosts", a.hosts == [])

    test("Aggregate #1 is deleted", a not in c.server.list())


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list aggregates: %s", [_.name for _ in c.aggregate.list()])
    main(c)
    LOG.debug("list aggregates: %s", [_.name for _ in c.aggregate.list()])

    show_test_summary()
