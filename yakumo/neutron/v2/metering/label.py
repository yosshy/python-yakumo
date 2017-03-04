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
Resource class and its manager for metering labels for Networking v2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for metering labels for Networking v2 API"""


class Manager(base.Manager):
    """Manager class for metering labels for Networking v2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'metering_label'
    _json_resources_key = 'metering_labels'
    _url_resource_path = '/v2.0/metering/metering-labels'

    def create(self, name=UNDEF, description=UNDEF):
        """
        Create a LB member for a pool

        :param name=: Label name (str)
        :param description=: Description (str)
        """
        return super(Manager, self).create(name=name,
                                           description=description)
