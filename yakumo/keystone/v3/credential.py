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
Resource class and its manager for credentials in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('type', 'type', mapper.Noop),
    ('blob', 'blob', mapper.JSON),
    ('user', 'user_id', mapper.Resource('keystone.user')),
    ('project', 'project_id', mapper.Resource('keystone.project')),
]


class Resource(base.Resource):
    """resource class for credentials on Identity V3 API"""

    def update(self, type=UNDEF, blob=UNDEF, user=UNDEF, project=UNDEF):
        """
        Update properties of a credential

        @keyword type: Credential type
        @type type: str
        @keyword blob: Blob
        @type blob: str
        @keyword user: User
        @type user: yakumo.keystone.v3.user.Resource
        @keyword project: Project
        @type project: yakumo.keystone.v3.project.Resource
        @rtype: None
        """
        super(Resource, self).update(
            type=type,
            blob=blob,
            user=user,
            project=project)


class Manager(base.Manager):
    """manager class for credentials on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'credential'
    _json_resources_key = 'credentials'
    _update_method = 'patch'
    _url_resource_path = '/credentials'

    def create(self, type=UNDEF, blob=UNDEF, user=UNDEF, project=UNDEF):
        """
        Register a credential

        @keyword type: Credential type
        @type type: str
        @keyword blob: Blob
        @type blob: str
        @keyword user: User
        @type user: yakumo.keystone.v3.user.Resource
        @keyword project: Project
        @type project: yakumo.keystone.v3.project.Resource
        @return: Created credential
        @rtype: yakumo.keystone.v3.creadential.Resource
        """
        return super(Manager, self).create(
            type=type,
            blob=blob,
            user=user,
            project=project)
