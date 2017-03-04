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
Resource class and its manager for volumes on Block Storage V1 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('extra_specs', 'extra_specs', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for volumes on Block Storage V1 API"""


class Manager(base.Manager):
    """manager class for roles on Block Storage V1 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'volume_type'
    _json_resources_key = 'volume_types'
    _hidden_methods = ["update"]
    _url_resource_list_path = '/types'
    _url_resource_path = '/types'

    def create(self, name=UNDEF, extra_specs=UNDEF):
        """
        Register a volume type

        @keyword name: Volume type name
        @type name: str
        @keyword extra_specs: Metadata (key=value)
        @type extra_specs: dict
        @return: Created volume type
        @rtype: yakumo.cinder.v1.volume_type.Resource
        """
        return super(Manager, self).create(name=name, extra_specs=extra_specs)
