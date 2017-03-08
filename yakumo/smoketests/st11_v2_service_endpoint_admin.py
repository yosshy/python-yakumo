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
"""Identity API v2 Test (Services/Endpoints)"""


import hashlib
import os
import tempfile

from yakumo.smoketest import *
from yakumo import utils


def main(c):

    # check Identity API version
    if c._session.config[u'identity_api_version'] != '2.0':
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

        LOG.info("Create Endpoints")
        name = get_random_str('endpoint')
        region_name = get_random_str('region')
        public_url = 'http://%s/v1/public' % name
        internal_url = 'http://%s/v1/internal' % name
        admin_url = 'http://%s/v1/admin' % name
        with c.endpoint.create(public_url=public_url,
                               internal_url=internal_url,
                               admin_url=admin_url,
                               region=region_name,
                               service=s,
                               is_enabled=False) as e:

            test("Endpoints #1: service is %s" % s.name, e.service == s)
            test("Endpoints #1: region name is %s" % region_name,
                 e.region == region_name)
            test("Endpoints #1: public_url is %s" % public_url,
                 e.public_url == public_url)
            test("Endpoints #1: internal_url is %s" % internal_url,
                 e.internal_url == internal_url)
            test("Endpoints #1: admin_url is %s" % admin_url,
                 e.admin_url == admin_url)
            test("Endpoints #1: is disabled", not e.is_enabled)

    LOG.debug("list service: %s", [_.name for _ in c.service.list()])
    LOG.debug("list endpoints: %s", c.endpoint.list())
    show_test_summary()


if __name__ == '__main__':
    main(utils.get_client())
