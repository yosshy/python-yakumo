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
Resource class and its manager for LB backend members in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('pool', 'pool_id', mapper.Resource('neutron.lb.pool')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('protocol_port', 'protocol_port', mapper.Noop),
    ('weight', 'weight', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('address', 'address', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for LB backend members in Networking V2 API"""

    def update(self, is_enabled=UNDEF):
        """
        Update a LB member for a pool

        @keyword is_enabled: Member is enabled
        @type is_enabled: bool
        @rtype: None
        """
        pool = self.parent_resource
        super(Resource, self).update(pool=pool, is_enabled=is_enabled)


class Manager(base.SubManager):
    """Manager class for LB backend members in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'member'
    _json_resources_key = 'members'
    _url_resource_path = '/v2.0/lb/members'

    def create(self, address=UNDEF, port=UNDEF, weight=UNDEF,
               is_enabled=UNDEF):
        """
        Create a LB member for a pool

        @keyword address: IP address (required)
        @type address: str
        @keyword port: Port (required)
        @type port: str
        @keyword weight: Member weight
        @type weight: int
        @keyword is_enabled: Whether the member is enabled
        @type is_enabled: bool
        @return: Created member
        @rtype: yakumo.neutron.v2.lb.member.Resource
        """
        pool = self.parent_resource
        return super(Manager, self).create(pool=pool,
                                           address=address,
                                           port=port,
                                           weight=weight,
                                           is_enabled=is_enabled)

    def _find_gen(self, **kwargs):
        kwargs['pool'] = self.parent_resource
        return super(Manager, self)._find_gen(**kwargs)
