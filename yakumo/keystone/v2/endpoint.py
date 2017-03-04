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
Resource class and its manager for endpoints in Identity V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import exception


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('public_url', 'publicurl', mapper.Noop),
    ('internal_url', 'internalurl', mapper.Noop),
    ('admin_url', 'adminurl', mapper.Noop),
    ('region', 'region', mapper.Noop),
    ('is_enabled', 'enabled', mapper.Noop),
    ('service', 'service_id', mapper.Resource('keystone.service')),
]


class Resource(base.Resource):
    """resource class for endpoints on Identity V2 API"""


class Manager(base.Manager):
    """manager class for endpoints on Identity V2 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'endpoint'
    _json_resources_key = 'endpoints'
    _url_resource_path = '/endpoints'

    def create(self, public_url=UNDEF, internal_url=UNDEF, admin_url=UNDEF,
               region=UNDEF, is_enabled=UNDEF, service=UNDEF):
        """
        Register endpoints for a service

        @keyword public_url: URL of the public endpoint
        @type public_url: str
        @keyword internal_url: URL of the internal endpoint
        @type internal_url: str
        @keyword admin_url: URL of the admin endpoint
        @type admin_url: str
        @keyword region: Region name
        @type region: str
        @keyword is_enabled: Whether the endpoints are enabled or not
        @type is_enabled: bool
        @keyword service: Service
        @type service: yakumo.keystone.v2.service.Resource
        @return: Created endpoint
        @rtype: yakumo.keystone.v2.endpoint.Resource
        """
        return super(Manager, self).create(
            public_url=public_url,
            internal_url=internal_url,
            admin_url=admin_url,
            region=region,
            is_enabled=is_enabled,
            service=service)

    def get(self, id):
        try:
            ret = self.find_one(id=id)
            if ret is None:
                raise exception.NotFound
            return ret
        except exception.Forbidden:
            return self.get_empty(id)
