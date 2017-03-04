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
Resource class and its manager for LB virtual IPs in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('protocol', 'protocol', mapper.Noop),
    ('address', 'address', mapper.Noop),
    ('protocol_port', 'protocol_port', mapper.Noop),
    ('connection_limit', 'connection_limit', mapper.Noop),
    ('pool', 'pool_id', mapper.Resource('neutron.lb.pool')),
    ('subnet', 'subnet_id', mapper.Resource('neutron.subnet')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('port', 'port_id', mapper.Resource('neutron.port')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('is_session_persistent', 'session_persistence', mapper.Noop),
    ('status', 'status', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for LB virtual IPs in Networking V2 API"""

    def update(self, name=UNDEF, description=UNDEF, session_persistence=UNDEF,
               connection_limit=UNDEF, is_enabled=UNDEF):
        """
        Update a VIP for a LB pool

        @keyword name: VIP name (str)
        @type name: str
        @keyword description: VIP description (str)
        @type description: str
        @keyword is_session_persistent: Whether session is persistent
        @type is_session_persistent: bool
        @keyword connection_limit: Maximum connection number
        @type connection_limit: int
        @keyword is_enabled: Whether the VIP is enabled
        @type is_enabled: bool
        @rtype: None
        """
        pool = self.parent_resource
        super(Resource, self).update(
            name=name,
            description=description,
            pool=pool,
            session_persistence=session_persistence,
            connection_limit=connection_limit,
            is_enabled=is_enabled)


class Manager(base.SubManager):
    """Manager class for LB virtual IPs in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'vip'
    _json_resources_key = 'vips'
    _url_resource_path = '/v2.0/lb/vips'

    def create(self, name=UNDEF, description=UNDEF, subnet=UNDEF,
               address=UNDEF, protocol=UNDEF, protocol_port=UNDEF,
               session_persistence=UNDEF, connection_limit=UNDEF,
               is_enabled=UNDEF):
        """
        Create a VIP for a LB pool

        @keyword name: VIP name
        :param name: str
        @keyword description: VIP description
        :param description: str
        @keyword subnet: Subnet object (required)
        :param subnet: yakumo.neutron.v2.subnet.Resource
        @keyword address: Address
        :param address: str
        @keyword protocol: Protocol; 'TCP', 'HTTP', or 'HTTPS' (required)
        :param protocol: str
        @keyword protocol_port: Port number
        :param protocol_port: int
        @keyword pool: LB pool
        :param pool: yakumo.neutron.v2.lb_pool.Resource
        @keyword is_session_persistent: Whether the session is persistent
        :param is_session_persistent: bool
        @keyword connection_limit: Maximum connection number
        :param connection_limit: int
        @keyword is_enabled: Whether the VIP is enabled
        :param is_enabled: bool
        @return: Created VIP
        @rtype: yakumo.neutron.v2.lb.vip.Resource
        """
        pool = self.parent_resource
        return super(Manager, self).create(
            name=name,
            description=description,
            subnet=subnet,
            address=address,
            protocol=protocol,
            protocol_port=protocol_port,
            pool=pool,
            session_persistence=session_persistence,
            connection_limit=connection_limit,
            is_enabled=is_enabled)

    def _find_gen(self, **kwargs):
        kwargs['pool'] = self.parent_resource
        return super(Manager, self)._find_gen(**kwargs)
