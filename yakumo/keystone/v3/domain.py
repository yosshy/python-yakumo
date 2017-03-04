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

"""
Resource class and its manager for domains in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import exception
from yakumo import mapper

from .group import Resource as Group
from .role import Resource as Role
from .user import Resource as User


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('is_enabled', 'enabled', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for domains on Identity V3 API"""

    def update(self, name=UNDEF, description=UNDEF, is_enabled=UNDEF):
        """
        Update properties of a domain

        @keyword name: Domain name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the domain is enabled or not
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            is_enabled=is_enabled)

    def check_roles(self, users=None, groups=None, roles=None):
        """
        Check roles of users and/or groups for a project

        @keyword users: List of users
        @type users: [keystone.user.Resource]
        @keyword groups: List of groups
        @type groups: [keystone.group.Resource]
        @keyword roles: List of roles
        @type roles: [keystone.role.Resource]
        @return: Whether users/groups have roles
        @rtype: None
        """
        if users is None:
            users = []
        if isinstance(users, User):
            users = [users]
        if groups is None:
            groups = []
        if isinstance(groups, Group):
            groups = [groups]
        if roles is None:
            roles = []
        if isinstance(roles, Role):
            roles = [roles]

        ret = []
        for user in users:
            try:
                for role in roles:
                    self._http.head(self._url_resource_path, self._id,
                                    "users", user.get_id(),
                                    "roles", role.get_id())
                ret.append(True)
            except exception.NotFound:
                ret.append(False)
        for group in groups:
            try:
                for role in roles:
                    self._http.head(self._url_resource_path, self._id,
                                    "groups", group.get_id(),
                                    "roles", role.get_id())
                ret.append(True)
            except exception.NotFound:
                ret.append(False)
        return ret

    def grant_roles(self, users=None, groups=None, roles=None):
        """
        Grant roles to users and/or groups for a project

        @keyword users: List of users
        @type users: [keystone.user.Resource]
        @keyword groups: List of groups
        @type groups: [keystone.group.Resource]
        @keyword roles: List of roles
        @type roles: [keystone.role.Resource]
        @rtype: None
        """
        if users is None:
            users = []
        if isinstance(users, User):
            users = [users]
        if groups is None:
            groups = []
        if isinstance(groups, Group):
            groups = [groups]
        if roles is None:
            roles = []
        if isinstance(roles, Role):
            roles = [roles]
        for role in roles:
            for user in users:
                self._http.put(self._url_resource_path, self._id,
                               "users", user.get_id(),
                               "roles", role.get_id())
            for group in groups:
                self._http.put(self._url_resource_path, self._id,
                               "groups", group.get_id(),
                               "roles", role.get_id())

    def revoke_roles(self, users=None, groups=None, roles=None):
        """
        Revoke roles from users and/or groups for a project

        @keyword users: List of users
        @type users: [keystone.user.Resource]
        @keyword groups: List of groups
        @type groups: [keystone.group.Resource]
        @keyword roles: List of roles
        @type roles: [keystone.role.Resource]
        @rtype: None
        """
        if users is None:
            users = []
        if isinstance(users, User):
            users = [users]
        if groups is None:
            groups = []
        if isinstance(groups, Group):
            groups = [groups]
        if roles is None:
            roles = []
        if isinstance(roles, Role):
            roles = [roles]
        for role in roles:
            for user in users:
                self._http.delete(self._url_resource_path, self._id,
                                  "users", user.get_id(),
                                  "roles", role.get_id())
            for group in groups:
                self._http.delete(self._url_resource_path, self._id,
                                  "groups", group.get_id(),
                                  "roles", role.get_id())


class Manager(base.Manager):
    """manager class for domains on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'domain'
    _json_resources_key = 'domains'
    _update_method = 'patch'
    _url_resource_path = '/domains'

    def create(self, name=UNDEF, description=UNDEF, is_enabled=UNDEF):
        """
        Register a domain

        @keyword name: Domain name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the domain is enabled or not
        @type is_enabled: bool
        @return: Created domain
        @rtype: yakumo.keystone.v3.domain.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            is_enabled=is_enabled)
