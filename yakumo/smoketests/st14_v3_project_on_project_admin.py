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
"""Identity API v3 Test (Hierarchical Projects)"""


import hashlib
import os
import tempfile

from yakumo.smoketest import *
from yakumo import utils


def main(c):

    # check Identity API version
    if c._session.config[u'identity_api_version'] != '3':
        return

    LOG.info("Create Domain #1")
    name = get_random_str('domain')
    with c.domain.create(name=name,
                         description='domain 1',
                         is_enabled=True) as d:

        test("Doamin #1: name is %s" % name, d.name == name)

        LOG.info("Create Project #1")
        name = get_random_str('project')
        with c.project.create(name=name,
                              description='project 1',
                              domain=d,
                              is_enabled=True) as p1:

            test("Project #1: name is %s" % name, p1.name == name)

            LOG.info("Create Project #2")
            name = get_random_str('project')
            with c.project.create(name=name,
                                  description='project 2',
                                  domain=d,
                                  parent=p1,
                                  is_enabled=False) as p2:

                test("Project #2: name is %s" % name, p2.name == name)
                test("Project #2: description is 'project 2'",
                     p2.description == 'project 2')
                test("Project #2: is disabled", not p2.is_enabled)
                test("Project #2: parent is Project #2",
                     p2.parent == p1)

        LOG.debug("Domain #1: disabled to delete")
        d.update(is_enabled=False)


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list domains: %s", [_.name for _ in c.domain.list()])
    LOG.debug("list projects: %s", [_.name for _ in c.project.list()])
    main(c)
    LOG.debug("list domains: %s", [_.name for _ in c.domain.list()])
    LOG.debug("list projects: %s", [_.name for _ in c.project.list()])

    show_test_summary()
