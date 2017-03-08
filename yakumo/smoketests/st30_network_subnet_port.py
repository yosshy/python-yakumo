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
"""Networking API Test (Networks/Subnets/Ports)"""


from yakumo.smoketest import *
from yakumo import utils


CIDR = '192.168.35.0/24'
GATEWAY_IP = '192.168.35.254'
FIXED_IP = '192.168.35.100'


def main(c):

    LOG.debug("list networks: %s", [_.name for _ in c.network.list()])
    LOG.debug("list subnets: %s", [_.name for _ in c.subnet.list()])

    LOG.info("Create Network #1")
    name = get_random_str('network')
    with c.network.create(name=name, is_shared=False) as n:

        LOG.debug("list networks: %s", [_.name for _ in c.network.list()])

        LOG.debug("wait for created")
        n.wait_for_finished()
        test("Network #1 name is " + name, n.name == name)
        test("Network #1 is active", n.status == 'ACTIVE')

        LOG.info("Create Subnet #1")
        name = get_random_str('subnet')
        with c.subnet.create(name=name,
                             network=n,
                             ip_version=4,
                             cidr=CIDR,
                             gateway_ip=GATEWAY_IP,
                             is_dhcp_enabled=True) as s:

            LOG.debug("list subnets: %s", [_.name for _ in c.subnet.list()])

            test("Subnet #1 name is " + name, s.name == name)

            LOG.info("Create Port #1")
            name = get_random_str('port')
            with c.port.create(name=name, network=n) as p1:

                LOG.debug("list ports: %s", [_.name for _ in c.port.list()])

                test("Port #1 name is " + name, p1.name == name)

            test("Port #1 is gone", p1 not in c.port.list())

            LOG.info("Create Port #2")
            name = get_random_str('port')
            with c.port.create(name=name,
                               fixed_ips=[{
                                   'ip_address': FIXED_IP,
                                   'subnet': s}],
                               network=n) as p2:

                LOG.debug("list ports: %s", [_.name for _ in c.port.list()])

                test("Port #2 name is " + name, p2.name == name)
                test("Port #2 has specified IP address",
                     FIXED_IP in [_['ip_address'] for _ in p2.fixed_ips])

            test("Port #2 is gone", p2 not in c.port.list())

        test("Subnet #1 is gone", s not in c.subnet.list())

    test("Network #1 is gone", n not in c.network.list())

    LOG.debug("list networks: %s", [_.name for _ in c.network.list()])
    LOG.debug("list subnets: %s", [_.name for _ in c.subnet.list()])

    show_test_summary()


if __name__ == '__main__':
    main(utils.get_client())
