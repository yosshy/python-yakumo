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
Resource class and its manager for roles in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for roles on Identity V3 API"""

    def update(self, name=UNDEF):
        """
        Update the name of a role

        @keyword name: Role name
        @type name: str
        @rtype: None
        """
        super(Resource, self).update(name=name)


class Manager(base.Manager):
    """manager class for roles on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'role'
    _json_resources_key = 'roles'
    _update_method = 'patch'
    _url_resource_path = '/roles'

    def create(self, name=UNDEF):
        """
        Register a role

        @keyword name: Role name
        @type name: str
        @return: Created role
        @rtype: yakumo.keystone.v3.role.Resource
        """
        return super(Manager, self).create(name=name)
