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


from yakumo.smoketest import *
from yakumo import utils


QUOTA_BYTES = 10 * 1024 ** 3  # 10GB
QUOTA_COUNT = 10


def main(c):

    LOG.info("Create an container")

    name = get_random_str('container')
    metadata = {'foo': 'bar', 'foo2': 'bar2'}
    with c.container.create(name=name,
                            quota_bytes=QUOTA_BYTES,
                            quota_count=QUOTA_COUNT,
                            metadata=metadata) as co:

        test("Container #1: name is " + name, co.name == name)
        test("Container #1: quota bytes is %s" % QUOTA_BYTES,
             co.quota_bytes == QUOTA_BYTES)
        test("Container #1: quota count is %s" % QUOTA_COUNT,
             co.quota_count == QUOTA_COUNT)

        LOG.info("Double quotas")
        co.update(quota_bytes=(QUOTA_BYTES * 2), quota_count=(QUOTA_COUNT * 2))
        test("Container #1: quota bytes is %s" % (QUOTA_BYTES * 2),
             co.quota_bytes == QUOTA_BYTES * 2)
        test("Container #1: quota count is %s" % (QUOTA_COUNT * 2),
             co.quota_count == QUOTA_COUNT * 2)

        LOG.info("Update metadata")
        LOG.debug("Initial metadata: %s", co.metadata)
        test("Metadata has %s" % metadata, co.metadata == metadata)

        m = {'foo2': 'bar4', 'foo3': 'bar3'}
        LOG.debug("Set metadata : %s", m)
        metadata.update(m)
        co.set_metadata(**m)
        LOG.debug("Updated metadata: %s", co.metadata)
        test("Metadata has %s" % metadata, co.metadata == metadata)

        m = ['foo', 'foo2']
        LOG.debug("Unset metadata : %s", m)
        for key in m:
            metadata.pop(key)
        co.unset_metadata(*m)
        LOG.debug("Updated metadata: %s", co.metadata)
        test("Metadata has %s" % metadata, co.metadata == metadata)


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list containers: %s", [_.name for _ in c.container.list()])
    main(c)
    LOG.debug("list containers: %s", [_.name for _ in c.container.list()])

    show_test_summary()
