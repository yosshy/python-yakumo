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
"""Identity API v3 Test (Roles/Projects/Groups/Users)"""


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
                         is_enabled=False) as d:

        test("Doamin #1: name is %s" % name, d.name == name)
        test("Domain #1: description is 'domain 1'",
             d.description == 'domain 1')
        test("Domain #1: is disabled", not d.is_enabled)

        LOG.info("Update domain properties")

        name = get_random_str('domain')
        d.update(name=name, description='domain 1-1', is_enabled=True)

        test("Doamin #1: name is %s" % name, d.name == name)
        test("Domain #1: description is 'domain 1-1'",
             d.description == 'domain 1-1')
        test("Domain #1: is enabled", d.is_enabled)

        LOG.info("Create Role #1")
        name = get_random_str('role')
        with c.role.create(name=name) as r:

            test("Role #1: name is %s" % name, r.name == name)

            LOG.info("Create Project #1")
            name = get_random_str('project')
            with c.project.create(name=name,
                                  description='project 1',
                                  domain=d,
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

                LOG.info("Create Group #1")
                name = get_random_str('group')
                password = get_random_str('pass')
                with c.group.create(name=name,
                                    description='group 1',
                                    domain=d) as g:

                    test("Group #1: name is %s" % name, g.name == name)
                    test("Group #1: description is 'group 1'",
                         g.description == 'group 1')
                    test("Group #1: is in Domain #1", g.domain == d)

                    LOG.info("Update group properties")

                    name = get_random_str('group')
                    password = get_random_str('pass')
                    g.update(name=name, description='group 1-1')

                    test("Group #1: name is %s" % name, g.name == name)
                    test("Group #1: description is 'group 1-1'",
                         g.description == 'group 1-1')

                    test("Group #1: no Role #1 for Project #1",
                         p.check_roles(groups=g, roles=r) == [False])

                    LOG.info("Grant Role #1 to Group #1 for Project #1")
                    p.grant_roles(groups=g, roles=r)

                    test("Group #1: Role #1 for Project #1",
                         p.check_roles(groups=g, roles=r) == [True])

                    LOG.info("Revoke Role #1 from Group #1 for Project #1")
                    p.revoke_roles(groups=g, roles=r)

                    test("Group #1: no Role #1 for Project #1",
                         p.check_roles(groups=g, roles=r) == [False])

                    test("Group #1: no Role #1 for Domain #1",
                         d.check_roles(groups=g, roles=r) == [False])

                    LOG.info("Grant Role #1 to Group #1 for Domain #1")
                    d.grant_roles(groups=g, roles=r)

                    test("Group #1: Role #1 for Domain #1",
                         d.check_roles(groups=g, roles=r) == [True])

                    LOG.info("Revoke Role #1 from Group #1 for Domain #1")
                    d.revoke_roles(groups=g, roles=r)

                    test("Group #1: no Role #1 for Domain #1",
                         d.check_roles(groups=g, roles=r) == [False])

                    LOG.info("Create User #1")
                    name = get_random_str('user')
                    password = get_random_str('pass')
                    with c.user.create(name=name,
                                       email='user@example.com',
                                       password=password,
                                       domain=d,
                                       is_enabled=False) as u:

                        test("User #1: name is %s" % name, u.name == name)
                        test("User #1: email is 'user@example.com'",
                             u.email == 'user@example.com')
                        test("User #1: is in Domain #1", u.domain == d)
                        test("User #1: is disabled", not u.is_enabled)

                        LOG.info("Update user properties")

                        name = get_random_str('user')
                        password = get_random_str('pass')
                        u.update(name=name,
                                 email='user@example.net',
                                 password=password,
                                 is_enabled=True)

                        test("User #1: name is %s" % name, u.name == name)
                        test("User #1: email is 'user@example.net'",
                             u.email == 'user@example.net')
                        test("User #1: is enabled", u.is_enabled)

                        test("Group #1: no User #1 for Project #1",
                             p.check_roles(users=u, roles=r) == [False])

                        LOG.info("Grant Role #1 to User #1 for Project #1")
                        p.grant_roles(users=u, roles=r)

                        test("Group #1: User #1 for Project #1",
                             p.check_roles(users=u, roles=r) == [True])

                        LOG.info("Revoke Role #1 from User #1 for Project #1")
                        p.revoke_roles(users=u, roles=r)

                        test("Group #1: no User #1 for Project #1",
                             p.check_roles(users=u, roles=r) == [False])

                        test("Group #1: no User #1 for Domain #1",
                             d.check_roles(users=u, roles=r) == [False])

                        LOG.info("Grant Role #1 to User #1 for Domain #1")
                        d.grant_roles(users=u, roles=r)

                        test("Group #1: User #1 for Domain #1",
                             d.check_roles(users=u, roles=r) == [True])

                        LOG.info("Revoke Role #1 from User #1 for Domain #1")
                        d.revoke_roles(users=u, roles=r)

                        test("Group #1: no User #1 for Domain #1",
                             d.check_roles(users=u, roles=r) == [False])

        LOG.debug("Domain #1: disabled to delete")
        d.update(is_enabled=False)


if __name__ == '__main__':
    c = utils.get_client()

    LOG.debug("list domains: %s", [_.name for _ in c.domain.list()])
    LOG.debug("list roles: %s", [_.name for _ in c.role.list()])
    LOG.debug("list projects: %s", [_.name for _ in c.project.list()])
    LOG.debug("list groups: %s", [_.name for _ in c.group.list()])
    LOG.debug("list users: %s", [_.name for _ in c.user.list()])
    main(c)
    LOG.debug("list domains: %s", [_.name for _ in c.domain.list()])
    LOG.debug("list roles: %s", [_.name for _ in c.role.list()])
    LOG.debug("list projects: %s", [_.name for _ in c.project.list()])
    LOG.debug("list groups: %s", [_.name for _ in c.group.list()])
    LOG.debug("list users: %s", [_.name for _ in c.user.list()])

    show_test_summary()
