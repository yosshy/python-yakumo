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
Resource class and its manager for users in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('password', 'password', mapper.Noop),
    ('email', 'email', mapper.Noop),
    ('project', 'default_project_id', mapper.Resource('keystone.project')),
    ('domain', 'domain_id', mapper.Resource('keystone.domain')),
    ('is_enabled', 'enabled', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for users on Identity V3 API"""

    def update(self, name=UNDEF, password=UNDEF, email=UNDEF, project=UNDEF,
               domain=UNDEF, is_enabled=UNDEF):
        """
        Update properties of a user

        @keyword name: User name
        @type name: str
        @keyword password: Password
        @type password: str
        @keyword email: E-mail address
        @type email: str
        @keyword project: Project
        @type project: yakumo.keystone.v3.project.Resource
        @keyword domain: Domain
        @type domain: yakumo.keystone.v3.domain.Resource
        @keyword is_enabled: Whether the user is enabled or not
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            password=password,
            email=email,
            project=project,
            domain=domain,
            is_enabled=is_enabled)


class Manager(base.Manager):
    """manager class for users on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'user'
    _json_resources_key = 'users'
    _update_method = 'patch'
    _url_resource_path = '/users'

    def create(self, name=UNDEF, password=UNDEF, email=UNDEF, project=UNDEF,
               domain=UNDEF, is_enabled=UNDEF):
        """
        Register a user

        @keyword name: User name
        @type name: str
        @keyword password: Password
        @type password: str
        @keyword email: E-mail address
        @type email: str
        @keyword project: Project
        @type project: yakumo.keystone.v3.project.Resource
        @keyword domain: Domain
        @type domain: yakumo.keystone.v3.domain.Resource
        @keyword is_enabled: Whether the user is enabled or not
        @type is_enabled: bool
        @return: Created user
        @rtype: yakumo.keystone.v3.user.Resource
        """
        return super(Manager, self).create(
            name=name,
            password=password,
            email=email,
            project=project,
            domain=domain,
            is_enabled=is_enabled)
