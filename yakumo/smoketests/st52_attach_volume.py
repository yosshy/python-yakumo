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
"""Compute API Test (Attaching Volumes)"""


import time
import re
import yaml

from yakumo.smoketest import *
from yakumo import utils


USER_DATA = r'''#!/bin/sh
i=0
while [ $i -lt 30 ]; do
sleep 5
echo "BeginSysRepo"

CPU=`lscpu | awk '/^CPU.s/ { print $2 }`
echo "vcpus: $CPU"
RAM=`free -m | awk '/^Mem:/ { print $2 }`
echo "ram: $RAM"

echo "disks:"
lsblk -d -n -b | awk '{ print "  " $1 ": { size: " $4 ", type: " $6 " }" }'

echo "nics:"
ip a | sed -re "s/^([0-9])/\n\1/" | awk 'BEGIN { RS="" }
/^[0-9]: eth/ { gsub(":", "", $2);
print "  " $2 ": { mac: \"" $11"\", ip: " $15 " }" }'

echo "EndSysRepo"
done
exit 0
'''


REPORT_PATTERN = re.compile(r'''BeginSysRepo\n(.*?)EndSysRepo''',
                            re.MULTILINE | re.DOTALL)

KEY_PAIR_NAME = 'key1'
FLAVOR_NAME = 'm1.small'
IMAGE_NAME = 'cirros'
NETWORK_NAME = 'private'


def main(c, key_pair=None, flavor=None, image=None, network=None, **kwargs):

    LOG.debug("key pair: %s", key_pair)
    LOG.debug("flavor: %s", flavor)
    LOG.debug("image: %s", image)
    LOG.debug("network: %s", network)

    LOG.info("Create Volume #1")
    name = get_random_str('volume')
    with c.volume.create(name=name, size=1) as v:

        LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])

        test("Volume #1 is created", v is not None)

        LOG.debug("wait for created")
        v.wait_for_finished()

        test("Volume #1 name is " + name, v.name == name)
        test("Volume #1 is available", v.status == 'available')

        LOG.info("Create Server #1")
        name = get_random_str('server')
        with c.server.create(name=name,
                             networks=[network],
                             image=image,
                             flavor=flavor,
                             key_pair=key_pair,
                             user_data=USER_DATA) as s:

            LOG.debug("list servers: %s", [_.name for _ in c.server.list()])

            LOG.debug("wait for created")
            s.wait_for_finished()
            test("Server #1 name is " + name, s.name == name)
            test("Server #1 is active", s.status == 'ACTIVE')

            def get_guest_stat(cl):
                match = REPORT_PATTERN.search(cl)
                if match is None:
                    return
                return yaml.load(match.group(1))

            for i in range(30):
                time.sleep(10)
                cl = s.get_console_log(lines=20)
                if get_guest_stat(cl):
                    break
                if 'login:' in cl:
                    raise Exception()
            else:
                raise Exception()

            stat = get_guest_stat(cl)
            LOG.debug("vcpus: %s", stat['vcpus'])
            LOG.debug("ram: %s", stat['ram'])
            LOG.debug("nics: %s", stat['nics'])
            LOG.debug("disks: %s", stat['disks'])

            disks = len(stat['disks'])
            test("/dev/vdb not found", 'vdb' not in stat['disks'])

            LOG.info("Attach Volume #1")
            va = s.volume.attach(volume=v)
            v.wait_for_finished()

            test("Volume #1 is in-use", v.status == 'in-use')

            for i in range(30):
                time.sleep(10)
                cl = s.get_console_log(lines=20)
                stat = get_guest_stat(cl)

                if len(stat['disks']) != disks:
                    break

            test("/dev/vdb exists", 'vdb' in stat['disks'])
            test("Volume #1 is /dev/vdb",
                 v.size == (stat['disks']['vdb']['size'] / 1024 ** 3))

            disks = len(stat['disks'])

            LOG.info("Detach Volume #1")
            va.detach()
            v.wait_for_finished()

            test("Volume #1 is available", v.status == 'available')

            for i in range(30):
                time.sleep(10)
                cl = s.get_console_log(lines=20)
                stat = get_guest_stat(cl)

                if len(stat['disks']) != disks:
                    break
            test("/dev/vdb is gone", 'vdb' not in stat['disks'])

        test("Server #1 is deleted", s not in c.server.list())

    test("Volume #1 is deleted", v not in c.volume.list())


if __name__ == '__main__':
    c = utils.get_client()
    k = c.key_pair.find_one(name=KEY_PAIR_NAME)
    f = c.flavor.find_one(name=FLAVOR_NAME)
    i = c.image.find_one(name=IMAGE_NAME)
    n = c.network.find_one(name=NETWORK_NAME)

    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])
    main(c, key_pair=k, flavor=f, image=i, network=n)
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    LOG.debug("list volumes: %s", [_.name for _ in c.volume.list()])

    show_test_summary()
