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
"""Block Storage API Test (Volume Types)"""


from yakumo.smoketest import *
from yakumo import utils


def main(c):

    LOG.info("Create Volume Type #1")
    name = get_random_str('volume')
    i = c.image.find_one(name='cirros')
    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    with c.volume_type.create(name=name,
                              description='volume type 1',
                              metadata=metadata,
                              is_public=False) as vt1:

        test("Volume Type #1 is created", vt1 is not None)
        test("Volume Type #1 name is " + name, vt1.name == name)

        # properties

        name = get_random_str('volume')
        vt1.update(name=name)

        test("Volume Type #1 has a new name", vt1.name == name)

        # metadata operation

        LOG.debug("Set/unset metadata")

        LOG.debug("Initial metadata: %s", vt1.metadata)
        test("Metadata has %s" % metadata, vt1.metadata == metadata)

        m = {'foo2': 'bar4', 'foo3': 'bar3'}
        LOG.debug("Set metadata : %s", m)
        metadata.update(m)
        vt1.set_metadata(**m)
        LOG.debug("Updated metadata: %s", vt1.metadata)
        test("Metadata has %s" % metadata, vt1.metadata == metadata)

        m = ['foo', 'foo2']
        LOG.debug("Unset metadata : %s", m)
        for key in m:
            metadata.pop(key)
        vt1.unset_metadata(*m)
        LOG.debug("Updated metadata: %s", vt1.metadata)
        test("Metadata has %s" % metadata, vt1.metadata == metadata)

        # Volume

        LOG.info("Create Volume #1")
        name = get_random_str('volume')
        with c.volume.create(name=name,
                             volume_type=vt1,
                             size=1) as v1:
            test("Volume #1 is created", v1 is not None)

            LOG.debug("wait for created")
            v1.wait_for_finished()

            LOG.debug("Volume #1: %s", v1.get_attrs())
            test("Volume #1 name is " + name, v1.name == name)
            test("Volume type is " + vt1.name, v1.volume_type == vt1)

        test("Volume #1 is deleted", v1 not in c.volume.list())

    test("Volume Type #1 is deleted", vt1 not in c.volume.list())


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list volume types: %s", [_.name for _ in c.volume_type.list()])
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list QoS: %s", [_.name for _ in c.volume_type_qos.list()])
    main(c)
    LOG.debug("list volume types: %s", [_.name for _ in c.volume_type.list()])
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list QoS: %s", [_.name for _ in c.volume_type_qos.list()])

    show_test_summary()
