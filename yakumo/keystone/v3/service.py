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
Resource class and its manager for services in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('type', 'type', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('is_enabled', 'enabled', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for services on Identity V3 API"""

    def update(self, name=UNDEF, type=UNDEF, description=UNDEF,
               is_enabled=UNDEF):
        """
        Update properties of a service

        @keyword name: Service name
        @type name: str
        @keyword type: Service type
        @type type: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the service is enabled or not
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            type=type,
            description=description,
            is_enabled=is_enabled)


class Manager(base.Manager):
    """manager class for services on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'service'
    _json_resources_key = 'services'
    _update_method = 'patch'
    _url_resource_path = '/services'

    def create(self, name=UNDEF, type=UNDEF, description=UNDEF,
               is_enabled=UNDEF):
        """
        Register a service

        @keyword name: Service name
        @type name: str
        @keyword type: Service type
        @type type: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the service is enabled or not
        @type is_enabled: bool
        @return: Created service
        @rtype: yakumo.keystone.v3.service.Resource
        """
        return super(Manager, self).create(
            name=name,
            type=type,
            description=description,
            is_enabled=is_enabled)
