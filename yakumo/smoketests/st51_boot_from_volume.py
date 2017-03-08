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
"""Compute API Test (Booting from Volume)"""


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

    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

    LOG.info("Create Volume #1")
    name = get_random_str('volume')
    with c.volume.create(name=name, source=image, size=1) as v:

        LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])

        test("Volume #1 is created", v is not None)

        LOG.debug("wait for created")
        v.wait_for_finished()

        test("Volume #1 name is " + name, v.name == name)
        test("Volume #1 is available", v.status == 'available')
        test("Volume #1 source is the image", v.source_image == image)

        LOG.info("Create Server #1 with Volume #1")
        name = get_random_str('server')
        with c.server.create(name=name,
                             networks=[network],
                             disks=[{'source': v}],
                             flavor=flavor,
                             key_pair=key_pair) as s:

            LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

            LOG.debug("wait for created")
            s.wait_for_finished()
            test("Server #1 name is " + name, s.name == name)
            test("Server #1 is active", s.status == 'ACTIVE')
            v.reload()
            test("Volume #1 is in-use", v.status == 'in-use')

            LOG.info("wait for guest OS booted")
            for i in range(30):
                time.sleep(10)
                cl = s.get_console_log(lines=20)
                if 'login:' in cl:
                    test("Guest OS is ready", True)
                    break
            else:
                test("Guest OS is ready", False)

            LOG.info("Stop Server #1")
            s.stop()
            LOG.debug("wait for stopped")
            s.wait_for_finished()
            test("Server #1 is stopped", s.status == 'SHUTOFF')

            LOG.info("Start Server #1")
            s.start()
            LOG.debug("wait for started")
            s.wait_for_finished()
            test("Server #1 is active", s.status == 'ACTIVE')

        test("Server #1 is deleted", s not in c.server.list())

        v.reload()
        test("Volume #1 is available", v.status == 'available')

    test("Volume #1 is deleted", v not in c.volume.list())


if __name__ == '__main__':
    c = utils.get_client()
    k = c.key_pair.find_one(name=KEY_PAIR_NAME)
    f = c.flavor.find_one(name=FLAVOR_NAME)
    i = c.image.find_one(name=IMAGE_NAME)
    n = c.network.find_one(name=NETWORK_NAME)

    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    main(c, key_pair=k, flavor=f, image=i, network=n)
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

    show_test_summary()
