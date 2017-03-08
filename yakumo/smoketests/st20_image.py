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
"""Image API Test (Images)"""


import hashlib
import os
import tempfile

from yakumo.smoketest import *
from yakumo import utils


def get_md5(file):
    m = hashlib.md5()
    with open(file) as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            m.update(chunk)
    return m.hexdigest()


def main(c):

    SOURCE_IMAGE = './images/cirros-0.3.5-x86_64-disk.img'

    LOG.info("Create an image")

    name = get_random_str('image')
    with c.image.create(name=name,
                        file=SOURCE_IMAGE,
                        container_format='bare',
                        disk_format='qcow2',
                        tags=['tag1'],
                        os_type='linux') as m:
        LOG.debug("wait for created")
        m.wait_for_finished()

        test("Image name", m.name == name)
        test("Image size", m.size == os.stat(SOURCE_IMAGE).st_size)
        test("Image checksum", m.checksum == get_md5(SOURCE_IMAGE))
        test("Image is active", m.status == 'active')
        test("Image is private", not m.is_public)
        test("Container format is bare", m.container_format == 'bare')
        test("Disk format is qcow2", m.disk_format == 'qcow2')
        test("Extended attribute (os_type)", m.os_type == 'linux')
        test("Invalid attribute returns None", m.foo is None)

        LOG.info("Update image properties")

        name = get_random_str('image')
        m.update(name=name, os_type='windows')

        test("Image name", m.name == name)
        test("Extended attribute (os_type)", m.os_type == 'windows')

        with tempfile.NamedTemporaryFile() as f:

            LOG.info("Download image into a temporary file: %s", f.name)
            m.download(file=f.name)

            test("Downloaded image size", m.size == os.stat(f.name).st_size)
            test("Downloaded image checksum", m.checksum == get_md5(f.name))

        LOG.info("Deactivate an image")
        m.deactivate()

        test("Image is deactivated", m.status == 'deactivated')

        LOG.info("Activate an image")
        m.activate()

        test("Image is active", m.status == 'active')

        test("Image tags: tag1", m.tags == ['tag1'])

        LOG.info("Add a tag to a image")
        m.add_tag('tag2')

        test("Image tags: tag1, tag2", set(m.tags) == set(['tag1', 'tag2']))

        LOG.info("Remove a tag to a image")
        m.remove_tag('tag1')

        test("Image tags: tag2", m.tags == ['tag2'])


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list images: %s", [_.name for _ in c.image.list()])
    main(c)
    LOG.debug("list images: %s", [_.name for _ in c.image.list()])

    show_test_summary()
