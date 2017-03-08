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
"""Block Storage API Test (Volumes/Snapshots)"""


from yakumo.smoketest import *
from yakumo import utils


IMAGE_NAME = 'cirros'


def main(c, image=None):

    LOG.debug("image: %s", image)

    LOG.info("Create Volume #1")
    name = get_random_str('volume')
    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    with c.volume.create(name=name,
                         description="volume 1",
                         source=image,
                         metadata=metadata,
                         size=1) as v1:

        test("Volume #1 is created", v1 is not None)

        LOG.debug("wait for created")
        v1.wait_for_finished()

        test("Volume #1 name is " + name, v1.name == name)
        test("Volume #1 is available", v1.status == 'available')
        test("Volume #1 source is the image", v1.source_image == image)

        LOG.debug("Initial metadata: %s", v1.metadata)
        test("Metadata has %s" % metadata, v1.metadata == metadata)

        m = {'foo2': 'bar4', 'foo3': 'bar3'}
        LOG.debug("Set metadata : %s", m)
        metadata.update(m)
        v1.set_metadata(**m)
        LOG.debug("Updated metadata: %s", v1.metadata)
        test("Metadata has %s" % metadata, v1.metadata == metadata)

        m = ['foo', 'foo2']
        LOG.debug("Unset metadata : %s", m)
        for key in m:
            metadata.pop(key)
        v1.unset_metadata(*m)
        LOG.debug("Updated metadata: %s", v1.metadata)
        test("Metadata has %s" % metadata, v1.metadata == metadata)

        LOG.info("Create Snapshot #1 from Volume #1")
        name = get_random_str('snapshot')
        metadata = {'foo': 'bar', 'foo2': 'bar2'}
        with c.volume_snapshot.create(name=name,
                                      description="snapshot 1",
                                      metadata=metadata,
                                      force=True,
                                      source=v1) as s:

            test("Snapshot #1 is created", s is not None)

            LOG.debug("wait for created")
            s.wait_for_finished()

            test("Snapshot #1 name is " + name, s.name == name)
            test("Snapshot #1 is available", s.status == 'available')
            test("Snapshot #1 source is Volume #1", s.source == v1)

            LOG.debug("Initial metadata: %s", s.metadata)
            test("Metadata has %s" % metadata, s.metadata == metadata)

            m = {'foo2': 'bar4', 'foo3': 'bar3'}
            LOG.debug("Set metadata : %s", m)
            metadata.update(m)
            s.set_metadata(**m)
            LOG.debug("Updated metadata: %s", s.metadata)
            test("Metadata has %s" % metadata, s.metadata == metadata)

            m = ['foo', 'foo2']
            LOG.debug("Unset metadata : %s", m)
            for key in m:
                metadata.pop(key)
            s.unset_metadata(*m)
            LOG.debug("Updated metadata: %s", s.metadata)
            test("Metadata has %s" % metadata, s.metadata == metadata)

            LOG.info("Create Volume #2 from Snapshot #1")
            name = get_random_str('volume')
            with c.volume.create(name=name,
                                 description="volume 2",
                                 source=s) as v2:

                test("Volume #2 is created", v2 is not None)

                LOG.debug("wait for created")
                v2.wait_for_finished()

                test("Volume #2 name is " + name, v2.name == name)
                test("Volume #2 is available", v2.status == 'available')
                test("Volume #2 source is Snapshot #1",
                     v2.source_snapshot == s)

            test("Volume #2 is deleted", v2 not in c.volume.list())

        test("Snapshot #1 is deleted", s not in c.volume.list())

        LOG.info("Create Volume #3 from Volume #1")
        name = get_random_str('volume')
        with c.volume.create(name=name,
                             description="volume 3", source=v1) as v3:

            test("Volume #3 is created", v3 is not None)

            LOG.debug("wait for created")
            v3.wait_for_finished()

            test("Volume #3 name is " + name, v3.name == name)
            test("Volume #3 is available", v3.status == 'available')
            test("Volume #3 source is Volume #1", v3.source_volume == v1)

        test("Volume #3 is deleted", v3 not in c.volume.list())

    test("Volume #1 is deleted", v1 not in c.volume.list())


if __name__ == '__main__':
    c = utils.get_client()
    i = c.image.find_one(name=IMAGE_NAME)

    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list snapshots: %s", [_.name for _ in c.volume_snapshot.list()])
    main(c, image=i)
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list snapshots: %s", [_.name for _ in c.volume_snapshot.list()])

    show_test_summary()
