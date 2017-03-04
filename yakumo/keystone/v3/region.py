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
Resource class and its manager for regions in Identity V3 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('parent', 'parent_region_id', mapper.Resource('keystone.region')),
]


class Resource(base.Resource):
    """resource class for regions on Identity V3 API"""

    def update(self, description=UNDEF, parent=UNDEF):
        """
        Update properties of a region

        @keyword description: Description
        @type description: str
        @keyword parent: Parent region
        @type parent: yakumo.keystone.v3.region.Resource
        @rtype: None
        """
        super(Resource, self).update(
            description=description,
            parent=parent)


class Manager(base.Manager):
    """manager class for regions on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'region'
    _json_resources_key = 'regions'
    _update_method = 'patch'
    _url_resource_path = '/regions'

    def create(self, id=UNDEF, description=UNDEF, parent=UNDEF):
        """
        Register a region

        @keyword id: ID
        @type id: str
        @keyword description: Description
        @type description: str
        @keyword parent: Parent region
        @type parent: yakumo.keystone.v3.region.Resource
        @return: Created region
        @rtype: yakumo.keystone.v3.region.Resource
        """
        return super(Manager, self).create(
            id=id,
            description=description,
            parent=parent)
