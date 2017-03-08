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
"""Networking API Test (Security Groups)"""


from yakumo.smoketest import *
from yakumo import utils


CIDR = '192.168.35.0/24'
GATEWAY_IP = '192.168.35.254'
FIXED_IP = '192.168.35.100'


def main(c):

    LOG.info("Create Security Group #1")
    name = get_random_str('security_group')
    with c.security_group.create(name=name,
                                 description='securty group 1') as sg:

        LOG.debug("list security groups: %s",
                  [_.name for _ in c.security_group.list()])

        test("Security Group #1 name is " + name, sg.name == name)

        LOG.debug("list rules: %s",
                  [(_.direction, _.port_range_min, _.protocol)
                   for _ in sg.rules.list()])

        LOG.info("Create Rule #1")
        with sg.rules.create(direction='ingress',
                             ethertype='IPv4',
                             port_range_min=22,
                             port_range_max=22,
                             protocol='tcp',
                             remote_ip_prefix='0.0.0.0/0') as sgr:

            LOG.debug("list rules: %s",
                      [(_.direction, _.port_range_min, _.protocol)
                       for _ in sg.rules.list()])

            test("Security Group #1 has 3 rules", len(sg.rules.list()) == 3)

            test("Rule #1 direction", sgr.direction == 'ingress')
            test("Rule #1 ethertype", sgr.ethertype == 'IPv4')
            test("Rule #1 port_range_min", sgr.port_range_min == 22)
            test("Rule #1 port_range_max", sgr.port_range_max == 22)
            test("Rule #1 protocol", sgr.protocol == 'tcp')
            test("Rule #1 remote_ip_prefix",
                 sgr.remote_ip_prefix == '0.0.0.0/0')

        test("Rule #1 is gone", sgr not in sg.rules.list())

        LOG.debug("list rules: %s",
                  [(_.direction, _.port_range_min, _.protocol)
                   for _ in sg.rules.list()])

    test("security_group #1 is gone", sg not in c.security_group.list())


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list security groups: %s",
              [_.name for _ in c.security_group.list()])
    main(c)
    LOG.debug("list security_groups: %s",
              [_.name for _ in c.security_group.list()])

    show_test_summary()
