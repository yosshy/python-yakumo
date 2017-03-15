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
"""Container API Test (Container Metadata)"""


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


CONTENT_TYPE = "application/octet-stream"
CONTENT_TYPE2 = "application/qcow2"
TRANS_ID_EXTRA = "extra"
FILE = "images/cirros-0.3.5-x86_64-disk.img"
MD5 = get_md5(FILE)
SIZE = os.stat(FILE).st_size


def main(c):

    LOG.info("Create an container")

    name = get_random_str('container')
    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    with c.container.create(name=name) as co:

        name = get_random_str('object')
        with co.object.create(name=name,
                              content_type=CONTENT_TYPE,
                              file=FILE,
                              metadata=metadata) as o:
            LOG.debug("list objects: %s",
                      [_.name for _ in co.object.list()])

            test("Object #1: name is " + name, o.name == name)
            test("Object #1: content type is %s" % CONTENT_TYPE,
                 o.content_type == CONTENT_TYPE)
            test("Object #1: MD5 checksum is %s" % MD5,
                 o.etag == MD5)
            test("Object #1: size is %s" % SIZE,
                 o.size == SIZE)

            LOG.info("Update content type")
            o.update(content_type=CONTENT_TYPE2)
            test("Object #1: content type is %s" % CONTENT_TYPE2,
                 o.content_type == CONTENT_TYPE2)

            LOG.info("Update metadata")
            LOG.debug("Initial metadata: %s", o.metadata)
            test("Metadata has %s" % metadata, o.metadata == metadata)

            m = {'foo2': 'bar4', 'foo3': 'bar3'}
            LOG.debug("Set metadata : %s", m)
            metadata.update(m)
            o.set_metadata(**m)
            LOG.debug("Updated metadata: %s", o.metadata)
            test("Metadata has %s" % metadata, o.metadata == metadata)

            m = ['foo', 'foo2']
            LOG.debug("Unset metadata : %s", m)
            for key in m:
                metadata.pop(key)
            o.unset_metadata(*m)
            LOG.debug("Updated metadata: %s", o.metadata)
            test("Metadata has %s" % metadata, o.metadata == metadata)

            LOG.info("Copy Object #1 as Object #2")
            name = get_random_str('object')
            with o.copy(container=co, name=name) as o2:
                LOG.debug("list objects: %s",
                          [_.name for _ in co.object.list()])

                test("Object #2: name is " + name, o2.name == name)
                test("Object #2: content type is %s" % CONTENT_TYPE2,
                     o.content_type == CONTENT_TYPE2)
                test("Object #2: MD5 checksum is %s" % MD5,
                     o2.etag == MD5)
                test("Object #2: size is %s" % SIZE,
                     o2.size == SIZE)
                test("Metadata has %s" % metadata, o2.metadata == metadata)

            LOG.debug("list objects: %s",
                      [_.name for _ in co.object.list()])
            test("Object #2 is gone", o2 not in co.object.list())

            LOG.info("Replace Object #1")
            o.replace(content_type=CONTENT_TYPE, file=FILE)

            # content_type won't applied on replace()
            test("Object #1: content type is %s" % CONTENT_TYPE2,
                 o.content_type == CONTENT_TYPE2)
            test("Object #1: MD5 checksum is %s" % MD5,
                 o.etag == MD5)
            test("Object #1: size is %s" % SIZE,
                 o.size == SIZE)

            with tempfile.NamedTemporaryFile() as f:

                LOG.info("Download an object into a temporary file: %s",
                         f.name)
                o.download(file=f.name)

                test("Downloaded image size",
                     os.stat(f.name).st_size == SIZE)
                test("Downloaded image checksum",
                     get_md5(f.name) == MD5)

        LOG.debug("list objects: %s",
                  [_.name for _ in co.object.list()])
        test("Object #1 is gone", o not in co.object.list())

    test("Container #1 is gone", co not in c.container.list())

if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list containers: %s", [_.name for _ in c.container.list()])
    main(c)
    LOG.debug("list containers: %s", [_.name for _ in c.container.list()])

    show_test_summary()
