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
Resource class and its manager for availability zones in Compute API v2
"""

from yakumo import base
from yakumo import mapper
from yakumo import exception


ATTRIBUTE_MAPPING = [
    ('name', 'zoneName', mapper.Noop),
    ('status', 'zoneState', mapper.Noop),
    ('hosts', 'hosts', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for availability zones in Compute API v2"""


class Manager(base.Manager):
    """Manager class for availability zones in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "update"]
    _id_attr = 'name'
    _json_resource_key = 'availabilityZoneInfo'
    _json_resources_key = 'availabilityZoneInfo'
    _url_resource_path = '/os-availability-zone'
    _url_resource_list_path = '/os-availability-zone/detail'

    def get(self, name):
        try:
            return self.find_one(name=name)
        except exception.Forbidden:
            return self.get_empty(name)
