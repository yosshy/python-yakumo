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

from contextlib import contextmanager
import copy

from yakumo import Client
from yakumo.smoketest import *
from yakumo import utils

from yakumo.smoketests import *


CIDR1 = '192.168.35.0/24'
CIDR2 = '192.168.36.0/24'
GATEWAY_IP1 = '192.168.35.254'
GATEWAY_IP2 = '192.168.36.254'

IMAGE_FILE = 'images/cirros-0.3.5-x86_64-disk.img'
CONTAINER_FORMAT = 'bare'
DISK_FORMAT = 'qcow2'
FLAVOR_NAME = 'm1.small'
AZ_NAME = 'nova'


def main(c):

    for t in KEYSTONE_TESTS:
        try:
            LOG.info("%s: Started", t.__doc__)
            t.main(c)
            LOG.info("%s: Finished successfully", t.__doc__)
        except Exception as e:
            LOG.exception("%s: Error occured: %s", t.__doc__, e)

    project_name = get_random_str('test')
    user_name = get_random_str('test')
    password = get_random_str('pass')

    config = copy.copy(c._session.config)
    config['auth']['project_name'] = project_name
    config['auth']['username'] = user_name
    config['auth']['password'] = password
    r = c.role.find_one(name='_member_')

    if config['identity_api_version'] == '2.0':
        with c.project.create(name=project_name,
                              description='test project',
                              is_enabled=True) as p:
            with c.user.create(name=user_name,
                               username='test user',
                               password=password,
                               project=p,
                               is_enabled=True) as u:
                p.grant_roles(users=u, roles=r)
                c2 = Client(**config)
                tenant_tests(c, c2)

            test("User #1 is deleted", u not in c.user.list())
        test("Project #1 is deleted", p not in c.project.list())

    elif config['identity_api_version'] == '3':
        d = c.domain.find_one(name=config['project_domain_name'])
        with c.project.create(name=project_name,
                              description='test project',
                              domain=d,
                              is_enabled=True) as p:
            with c.user.create(name=user_name,
                               password=password,
                               domain=d,
                               is_enabled=True) as u:
                p.grant_roles(users=u, roles=r)
                c2 = Client(**config)
                tenant_tests(c, c2)

            test("User #1 is deleted", u not in c.user.list())
        test("Project #1 is deleted", p not in c.project.list())


def tenant_tests(c, c2):

    for t in GLANCE_TESTS + NEUTRON_TESTS + CINDER_TESTS:
        try:
            LOG.info("%s: Started", t.__doc__)
            if t.__name__.endswith('admin'):
                t.main(c)
            else:
                t.main(c2)
            LOG.info("%s: Finished successfully", t.__doc__)
        except Exception as e:
            LOG.exception("%s: Error occured: %s", t.__doc__, e)

    with c2.network.create(name=get_random_str('network'),
                           is_shared=False) as n1, \
        c2.network.create(name=get_random_str('network'),
                          is_shared=False) as n2:

        with c2.subnet.create(name=get_random_str('subnet'),
                              network=n1,
                              ip_version=4,
                              cidr=CIDR1,
                              gateway_ip=GATEWAY_IP1,
                              is_dhcp_enabled=True) as sn1, \
            c2.subnet.create(name=get_random_str('subnet'),
                             network=n2,
                             ip_version=4,
                             cidr=CIDR2,
                             gateway_ip=GATEWAY_IP2,
                             is_dhcp_enabled=True) as sn2:

            with c2.router.create(name=get_random_str('router')) as r1, \
                c2.router.create(name=get_random_str('router')) as r2, \
                c2.key_pair.create(name=get_random_str('keypair')) as k, \
                c2.image.create(name=get_random_str('image'),
                                file=IMAGE_FILE,
                                container_format=CONTAINER_FORMAT,
                                disk_format=DISK_FORMAT) as i:

                    r1.add_interface(subnet=sn1)
                    r2.add_interface(subnet=sn2)

                    f = c2.flavor.find_one(name=FLAVOR_NAME)
                    az = c2.availability_zone.get_empty(AZ_NAME)

                    for t in NOVA_TESTS:
                        try:
                            LOG.info("%s: Started", t.__doc__)
                            if t.__name__.endswith('admin'):
                                t.main(
                                    c, image=i, flavor=f, key_pair=k,
                                    network=n1, network2=n2,
                                    availability_zone=az)
                            else:
                                t.main(
                                    c2, image=i, flavor=f, key_pair=k,
                                    network=n1, network2=n2,
                                    availability_zone=az)
                            LOG.info("%s: Finished successfully", t.__doc__)
                        except Exception as e:
                            LOG.exception("%s: Error occured: %s",
                                          t.__doc__, e)

                    r1.remove_interface(subnet=sn1)
                    r2.remove_interface(subnet=sn2)

            test("Router #1 is deleted", r1 not in c2.router.list())
            test("Router #2 is deleted", r2 not in c2.router.list())
            test("Key Pair #1 is deleted", k not in c2.key_pair.list())
            test("Image #1 is deleted", i not in c2.image.list())

        test("Subnet #1 is deleted", sn1 not in c2.subnet.list())
        test("Subnet #2 is deleted", sn2 not in c2.subnet.list())

    test("Network #1 is deleted", n1 not in c2.network.list())
    test("Network #2 is deleted", n2 not in c2.network.list())

if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list networks: %s", [_.name for _ in c.network.list()])
    LOG.debug("list subnets: %s", [_.name for _ in c.subnet.list()])
    LOG.debug("list routers: %s", [_.name for _ in c.router.list()])
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    LOG.debug("list key pairs: %s", [_.name for _ in c.key_pair.list()])
    LOG.debug("list images: %s", [_.name for _ in c.image.list()])
    main(c)
    LOG.debug("list networks: %s", [_.name for _ in c.network.list()])
    LOG.debug("list subnets: %s", [_.name for _ in c.subnet.list()])
    LOG.debug("list routers: %s", [_.name for _ in c.router.list()])
    LOG.debug("list servers: %s", [_.name for _ in c.server.list()])
    LOG.debug("list key pairs: %s", [_.name for _ in c.key_pair.list()])
    LOG.debug("list images: %s", [_.name for _ in c.image.list()])
    show_test_summary()
