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
Resource class and its manager for roles in Identity V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for roles on Identity V2 API"""


class Manager(base.Manager):
    """manager class for roles on Identity V2 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'role'
    _json_resources_key = 'roles'
    _url_resource_path = '/OS-KSADM/roles'

    def create(self, name=UNDEF, description=UNDEF):
        """
        Register a role

        @keyword name: Role name
        @type name: str
        @keyword description: Description
        @type description: str
        @return: Created role
        @rtype: yakumo.keystone.v2.role.Resource
        """
        return super(Manager, self).create(name=name, description=description)
