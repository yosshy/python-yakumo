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
"""Identity API v2 Test (Roles/Projects/Users)"""


import hashlib
import os
import tempfile
from yakumo.smoketest import *
from yakumo import utils


def main(c):

    # check Identity API version
    if c._session.config[u'identity_api_version'] != '2.0':
        return

    LOG.info("Create Role #1")
    name = get_random_str('role')
    with c.role.create(name=name, description='role 1') as r:

        test("Role #1: name is %s" % name, r.name == name)
        test("Role #1: description is 'role 1'", r.description == 'role 1')

        LOG.info("Create a project")
        name = get_random_str('project')
        with c.project.create(name=name,
                              description='project 1',
                              is_enabled=False) as p:

            test("Project #1: name is %s" % name, p.name == name)
            test("Project #1: description is 'project 1'",
                 p.description == 'project 1')
            test("Project #1: is disabled", not p.is_enabled)

            LOG.info("Update project properties")

            name = get_random_str('project')
            p.update(name=name, description='project 1-1', is_enabled=True)

            test("Project #1: name is %s" % name, p.name == name)
            test("Project #1: description is 'project 1-1'",
                 p.description == 'project 1-1')
            test("Project #1: is enabled", p.is_enabled)

            LOG.info("Create a user")
            name = get_random_str('user')
            password = get_random_str('pass')
            with c.user.create(name=name,
                               username='user 1',
                               password=password,
                               project=p,
                               is_enabled=False) as u:

                test("User #1: name is %s" % name, u.name == name)
                test("User #1: username is 'user 1'", u.username == 'user 1')
                test("User #1: is disabled", not u.is_enabled)
                test("User #1: is in project", not u.is_enabled)

                LOG.info("Update user properties")

                name = get_random_str('user')
                password = get_random_str('pass')
                u.update(name=name,
                         username='user 1-1',
                         password=password,
                         is_enabled=True)

                test("User #1: name is %s" % name, u.name == name)
                test("User #1: username is 'user 1-1'",
                     u.username == 'user 1-1')
                test("User #1: is enabled", u.is_enabled)

                LOG.info("Grant Role #1 to User #1 for Project #1")
                p.grant_roles(users=u, roles=r)

                LOG.info("Revoke Role #1 from User #1 for Project #1")
                p.revoke_roles(users=u, roles=r)


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list roles: %s", [_.name for _ in c.role.list()])
    LOG.debug("list projects: %s", [_.name for _ in c.project.list()])
    LOG.debug("list users: %s", [_.name for _ in c.user.list()])
    main(c)
    LOG.debug("list roles: %s", [_.name for _ in c.role.list()])
    LOG.debug("list projects: %s", [_.name for _ in c.project.list()])
    LOG.debug("list users: %s", [_.name for _ in c.user.list()])

    show_test_summary()
