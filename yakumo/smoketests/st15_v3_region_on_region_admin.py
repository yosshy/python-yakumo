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
"""Identity API v3 Test (Hierarchical Regions)"""


import hashlib
import os
import tempfile

from yakumo.smoketest import *
from yakumo import utils


def main(c):

    # check Identity API version
    if c._session.config[u'identity_api_version'] != '3':
        return

    LOG.debug("list regions: %s", c.region.list())

    LOG.info("Create Region #1")
    region_id = get_random_str('region')
    with c.region.create(id=region_id, description='region 1') as r1:

        test("Region #1: id is %s" % region_id, r1.id == region_id)

        LOG.info("Create Region #1")
        region_id = get_random_str('region')
        with c.region.create(id=region_id,
                             parent=r1,
                             description='region 2') as r2:

            test("Region #2: id is %s" % region_id, r2.id == region_id)
            test("Region #2: description is 'region 2'",
                 r2.description == 'region 2')
            test("Region #2: parent is #1", r2.parent == r1)

            LOG.info("Update Region #2")

            r2.update(parent=None)
            test("Region #2: no parent", r2.parent is None)

    LOG.debug("list regions: %s", c.region.list())
    show_test_summary()


if __name__ == '__main__':
    main(utils.get_client())
