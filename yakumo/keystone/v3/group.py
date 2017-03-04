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
Resource class and its manager for groups in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('domain', 'domain_id', mapper.Resource('keystone.domain')),
]


class Resource(base.Resource):
    """resource class for groups on Identity V3 API"""

    def update(self, name=UNDEF, description=UNDEF, domain=UNDEF):
        """
        Update properties of a group

        @keyword name: Group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword domain: Domain
        @type domain: yakumo.keystone.v3.domain.Resource
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            domain=domain)


class Manager(base.Manager):
    """manager class for groups on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'group'
    _json_resources_key = 'groups'
    _update_method = 'patch'
    _url_resource_path = '/groups'

    def create(self, name=UNDEF, description=UNDEF, domain=UNDEF):
        """
        Register a group

        @keyword name: Group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword domain: Domain
        @type domain: yakumo.keystone.v3.domain.Resource
        @return: Created group
        @rtype: yakumo.keystone.v3.group.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            domain=domain)
