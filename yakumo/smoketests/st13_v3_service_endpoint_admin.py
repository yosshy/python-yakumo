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
"""Identity API v3 Test (Services/Endpoints)"""


import hashlib
import os
import tempfile

from yakumo.smoketest import *
from yakumo import utils


def main(c):

    # check Identity API version
    if c._session.config[u'identity_api_version'] != '3':
        return

    LOG.debug("list services: %s", [_.name for _ in c.service.list()])
    LOG.debug("list endpoints: %s", c.endpoint.list())

    LOG.info("Create Service #1")
    name = get_random_str('service')
    with c.service.create(name=name,
                          type='type1',
                          description='service 1',
                          is_enabled=False) as s:

        test("Service #1: name is %s" % name, s.name == name)
        test("Service #1: type is 'type1'", s.type == 'type1')
        test("Service #1: description is 'service 1'",
             s.description == 'service 1')
        test("Service #1: is disabled", not s.is_enabled)

        LOG.info("Update service properties")
        name = get_random_str('service')
        s.update(name=name, type='type2', description='service 2',
                 is_enabled=True)

        test("Service #1: name is %s" % name, s.name == name)
        test("Service #1: type is 'type1'", s.type == 'type2')
        test("Service #1: description is 'service 2'",
             s.description == 'service 2')
        test("Service #1: is enabled", s.is_enabled)

        LOG.info("Create Region #1")
        region_id = get_random_str('region')
        with c.region.create(id=region_id, description='region 1') as r:

            test("Region #1: id is %s" % region_id, r.id == region_id)
            test("Region #1: description is 'region 1'",
                 r.description == 'region 1')

            LOG.info("Update region properties")
            r.update(description='region 2')

            test("Region #1: description is 'region 2'",
                 r.description == 'region 2')

            LOG.info("Create Endpoints")
            name = get_random_str('endpoint')
            url = 'http://%s/v1/public' % name
            with c.endpoint.create(url=url,
                                   interface='public',
                                   region=r,
                                   service=s) as e:

                test("Endpoints #1: service is %s" % s.name, e.service == s)
                test("Endpoints #1: region  is %s" % r.id, e.region == r)
                test("Endpoints #1: url is %s" % url, e.url == url)
                test("Endpoints #1: interface is public",
                     e.interface == 'public')

                LOG.info("Update endpoint properties")
                name = get_random_str('endpoint')
                url = 'http://%s/v1/internal' % name
                e.update(url=url, interface='internal')

                test("Endpoints #1: url is %s" % url, e.url == url)
                test("Endpoints #1: interface is internal",
                     e.interface == 'internal')

    LOG.debug("list service: %s", [_.name for _ in c.service.list()])
    LOG.debug("list endpoints: %s", c.endpoint.list())
    show_test_summary()


if __name__ == '__main__':
    main(utils.get_client())
