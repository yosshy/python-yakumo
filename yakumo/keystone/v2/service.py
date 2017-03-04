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
Resource class and its manager for services in Identity V2 API
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
    """resource class for services on Identity V2 API"""


class Manager(base.Manager):
    """manager class for services on Identity V2 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'OS-KSADM:service'
    _json_resources_key = 'OS-KSADM:services'
    _url_resource_path = '/OS-KSADM/services'

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
        @type is_enabled: str
        @return: Created service
        @rtype: yakumo.keystone.v2.service.Resource
        """
        return super(Manager, self).create(
            name=name,
            type=type,
            description=description,
            is_enabled=is_enabled)
