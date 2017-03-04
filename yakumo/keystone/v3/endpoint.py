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
Resource class and its manager for endpoints in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('interface', 'interface', mapper.Noop),
    ('url', 'url', mapper.Noop),
    ('region', 'region_id', mapper.Resource('keystone.region')),
    ('service', 'service_id', mapper.Resource('keystone.service')),
]


class Resource(base.Resource):
    """resource class for endpoints on Identity V3 API"""

    def update(self, name=UNDEF, description=UNDEF, interface=UNDEF, url=UNDEF,
               region=UNDEF, service=UNDEF):
        """
        Update properties of an endpoint

        @keyword name: Endpoint name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword interface: Interface type (public, internal or admin)
        @type interface: str
        @keyword url: URL
        @type url: str
        @keyword region: Region
        @type region: yakumo.keystone.v3.region.Resource
        @keyword service: Service
        @type service: yakumo.keystone.v3.service.Resource
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            interface=interface,
            url=url,
            region=region,
            service=service)


class Manager(base.Manager):
    """manager class for endpoints on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'endpoint'
    _json_resources_key = 'endpoints'
    _update_method = 'patch'
    _url_resource_path = '/endpoints'

    def create(self, name=UNDEF, description=UNDEF, interface=UNDEF, url=UNDEF,
               region=UNDEF, service=UNDEF):
        """
        Register an endpoint

        @keyword name: Endpoint name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword interface: Interface type (public, internal or admin)
        @type interface: str
        @keyword url: URL
        @type url: str
        @keyword region: Region
        @type region: yakumo.keystone.v3.region.Resource
        @keyword service: Service
        @type service: yakumo.keystone.v3.service.Resource
        @return: Created endpoint
        @rtype: yakumo.keystone.v3.endpoint.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            interface=interface,
            url=url,
            region=region,
            service=service)
