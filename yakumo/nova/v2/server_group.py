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
Resource class and its manager for server groups in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('policies', 'policies', mapper.Noop),
    ('members', 'members', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for server groups in Compute API v2"""


class Manager(base.Manager):
    """Manager class for server groups in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'server_group'
    _json_resources_key = 'server_groups'
    _url_resource_path = '/os-server-groups'

    def create(self, name=UNDEF, policies=UNDEF):
        """
        Create a server group

        @keyword name: name of server group
        @type name: str
        @keyword policies: list of policy names
        @type policies: [str]
        @return: Created server group
        @rtype: yakumo.nova.v2.server_group.Resource
        """
        return super(Manager, self).create(name=name,
                                           policies=policies)
