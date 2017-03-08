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
"""Compute API Test (Servers)"""


import time

from yakumo.smoketest import *
from yakumo import utils


KEY_PAIR_NAME = 'key1'
FLAVOR_NAME = 'm1.small'
IMAGE_NAME = 'cirros'
NETWORK_NAME = 'private'
AZ_NAME = 'nova'


def main(c, key_pair=None, flavor=None, image=None, network=None,
         availability_zone=None, **kwargs):

    LOG.debug("key pair: %s", key_pair)
    LOG.debug("flavor: %s", flavor)
    LOG.debug("image: %s", image)
    LOG.debug("network: %s", network)
    LOG.debug("availability zone: %s", availability_zone)

    LOG.info("Create Server #1")
    name = get_random_str('server')
    with c.server.create(name=name,
                         networks=[network],
                         image=image,
                         flavor=flavor,
                         availability_zone=availability_zone,
                         key_pair=key_pair) as s:

        LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

        LOG.debug("wait for created")
        s.wait_for_finished()
        test("Server #1 name is " + name, s.name == name)
        test("Server #1 is active", s.status == 'ACTIVE')
        test("Server #1 az is " + availability_zone.name,
             s.availability_zone == availability_zone)

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

        LOG.info("Force reboot Server #1")
        s.reboot(force=True)
        LOG.debug("wait for started")
        s.wait_for_finished()
        test("Server #1 is active", s.status == 'ACTIVE')

        LOG.info("Suspend Server #1")
        s.suspend()
        LOG.debug("wait for suspended")
        s.wait_for_finished()
        test("Server #1 is suspended", s.status == 'SUSPENDED')

        LOG.info("Resume Server #1")
        s.resume()
        LOG.debug("wait for resumed")
        s.wait_for_finished()
        test("Server #1 is active", s.status == 'ACTIVE')

        LOG.info("Pause Server #1")
        s.pause()
        LOG.debug("wait for paused")
        s.wait_for_finished()
        test("Server #1 is paused", s.status == 'PAUSED')

        LOG.info("Unpause Server #1")
        s.unpause()
        LOG.debug("wait for unpaused")
        s.wait_for_finished()
        test("Server is active", s.status == 'ACTIVE')

        LOG.info("Lock Server #1")
        s.lock()
        LOG.debug("wait for locked")
        s.wait_for_finished()
        test("Server #1 is active", s.status == 'ACTIVE')

        LOG.info("Stop Server #1 locked (will be failed)")
        try:
            s.stop()
            s.wait_for_finished()
        except:
            pass
        test("Server #1 is active", s.status == 'ACTIVE')

        LOG.info("Unlock Server #1")
        s.unlock()
        LOG.debug("wait for unlocked")
        s.wait_for_finished()

        LOG.info("Stop Server #1 unlocked (will be succeeded)")
        try:
            s.stop()
            s.wait_for_finished()
        except:
            pass
        test("Server #1 is stopped", s.status == 'SHUTOFF')

        LOG.info("Show Server #1 action: %s",
                 [_['action'] for _ in s.get_actions()])

    test("Server #1 is deleted", s not in c.server.list())


if __name__ == '__main__':
    c = utils.get_client()
    k = c.key_pair.find_one(name=KEY_PAIR_NAME)
    f = c.flavor.find_one(name=FLAVOR_NAME)
    i = c.image.find_one(name=IMAGE_NAME)
    n = c.network.find_one(name=NETWORK_NAME)
    az = c.availability_zone.get_empty(AZ_NAME)

    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    main(c, key_pair=k, flavor=f, image=i, network=n, availability_zone=az)
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

    show_test_summary()
