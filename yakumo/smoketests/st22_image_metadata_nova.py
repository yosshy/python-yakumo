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
"""Image API Test (Image Metadata)"""


import hashlib
import os
import tempfile

from yakumo.smoketest import *
from yakumo import utils


def main(c):

    LOG.debug("list images: %s", [_.name for _ in c.image.list()])

    SOURCE_IMAGE = './images/cirros-0.3.5-x86_64-disk.img'

    LOG.info("Create an image")

    name = get_random_str('image')
    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    with c.image.create(name=name,
                        file=SOURCE_IMAGE,
                        container_format='bare',
                        disk_format='qcow2',
                        tags=['tag1'],
                        **metadata) as i:
        LOG.debug("wait for created")
        i.wait_for_finished()

        test("Image name", i.name == name)
        test("Image is active", i.status == 'active')

        LOG.info("Update image metadata via nova API")
        ni = c.nova.image.find_one(name=name)
        test("Image name", ni.name == name)

        LOG.debug("Initial metadata: %s", ni.metadata)
        test("Metadata has %s" % metadata, ni.metadata == metadata)

        m = {'foo2': 'bar4', 'foo3': 'bar3'}
        LOG.debug("Set metadata : %s", m)
        metadata.update(m)
        ni.set_metadata(**m)
        LOG.debug("Updated metadata: %s", ni.metadata)
        test("Metadata has %s" % metadata, ni.metadata == metadata)

        m = ['foo', 'foo2']
        LOG.debug("Unset metadata : %s", m)
        for key in m:
            metadata.pop(key)
        ni.unset_metadata(*m)
        LOG.debug("Updated metadata: %s", ni.metadata)
        test("Metadata has %s" % metadata, ni.metadata == metadata)

    LOG.debug("list images: %s", [_.name for _ in c.image.list()])
    show_test_summary()


if __name__ == '__main__':
    main(utils.get_client())
