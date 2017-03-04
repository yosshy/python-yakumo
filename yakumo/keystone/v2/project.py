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
Resource class and its manager for projects in Identity V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('is_enabled', 'enabled', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for projects on Identity V2 API"""

    def update(self, name=UNDEF, description=UNDEF, is_enabled=UNDEF):
        """
        Update properties of a project

        @keyword name: Project name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the project is enabled or not
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            is_enabled=is_enabled)

    def grant_roles(self, users=None, roles=None):
        """
        Grant roles to users for a project

        @keyword users: List of users
        @type users: [keystone.user.Resource]
        @keyword roles: List of roles
        @type roles: [keystone.role.Resource]
        @rtype: None
        """
        if not isinstance(users, list):
            users = [users]
        if not isinstance(roles, list):
            roles = [roles]
        for role in roles:
            for user in users:
                self._http.put(self._url_resource_path, self._id,
                               "users", user.get_id(),
                               "roles/OS-KSADM", role.get_id())

    def revoke_roles(self, users=None, roles=None):
        """
        Revoke roles from users for a project

        @keyword users: List of users
        @type users: [keystone.user.Resource]
        @keyword roles: List of roles
        @type roles: [keystone.role.Resource]
        @rtype: None
        """
        if not isinstance(users, list):
            users = [users]
        if not isinstance(roles, list):
            roles = [roles]
        for role in roles:
            for user in users:
                self._http.delete(self._url_resource_path, self._id,
                                  "users", user.get_id(),
                                  "roles/OS-KSADM", role.get_id())


class Manager(base.Manager):
    """manager class for projects on Identity V2 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'tenant'
    _json_resources_key = 'tenants'
    _url_resource_path = '/tenants'

    def create(self, name=UNDEF, description=UNDEF, is_enabled=UNDEF):
        """
        Register a project

        @keyword name: Project name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the project is enabled or not
        @type is_enabled: bool
        @return: Created project
        @rtype: yakumo.keystone.v2.project.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            is_enabled=is_enabled)
