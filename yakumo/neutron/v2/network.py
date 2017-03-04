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
Resource class and its manager for networks in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('subnets', 'subnets',
     mapper.List(mapper.Resource('neutron.subnet'))),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('is_shared', 'shared', mapper.Noop),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('is_external', 'router:external', mapper.Noop),
    ('is_secured', 'port_security_enabled', mapper.Noop),
    ('segments', 'segments', mapper.Noop),
    ('provider_physical_network', 'provider:physical_network',
     mapper.Noop),
    ('provider_network_type', 'provider:network_type', mapper.Noop),
    ('provider_segmentation_id', 'segmentation_id', mapper.Noop),
    ('vlan_transparent', 'vlan_transparent', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for networks in Networking V2 API"""

    _stable_state = ['ACTIVE', 'DOWN', 'INACTIVE', 'ERROR']

    def update(self, name=UNDEF, is_shared=UNDEF, is_enabled=UNDEF,
               is_external=UNDEF, is_port_security_enabled=UNDEF,
               segments=UNDEF, provider_physical_network=UNDEF,
               provider_network_type=UNDEF,
               provider_segmentation_id=UNDEF):
        """
        Update properties of a network

        @keyword name: Network name
        @type name: str
        @keyword is_shared: Whether the network is shared
        @type is_shared: bool
        @keyword is_enabled: Whether the network is enabled
        @type is_enabled: bool
        @keyword is_external: Wehter the network is external
        @type is_external: bool
        @keyword is_port_security_enabled: Whether the network is secured
        @type is_port_security_enabled: bool
        @keyword segments: Segments
        @type segments: str
        @keyword provider_physical_network: (Provider) physical network
        @type provider_physical_network: str
        @keyword provider_network_type: (Provider) network type
        @type provider_network_type: str
        @keyword provider_segmentation_id: (Provider) segmentation ID
        @type provider_segmentation_id: int
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            is_shared=is_shared,
            is_enabled=is_enabled,
            is_external=is_external,
            is_port_security_enabled=is_port_security_enabled,
            segments=segments,
            provider_physical_network=provider_physical_network,
            provider_network_type=provider_network_type,
            provider_segmentation_id=provider_segmentation_id)


class Manager(base.Manager):
    """Manager class for networks in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'network'
    _json_resources_key = 'networks'
    _url_resource_path = '/v2.0/networks'

    def create(self, name=UNDEF, project=UNDEF, is_shared=UNDEF,
               is_enabled=UNDEF, is_external=UNDEF,
               is_port_security_enabled=UNDEF, segments=UNDEF,
               provider_physical_network=UNDEF, provider_network_type=UNDEF,
               provider_segmentation_id=UNDEF, vlan_transparent=UNDEF):
        """
        Create a network

        @keyword name: Network name
        @type name: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword is_shared: Whether the network is shared
        @type is_shared: bool
        @keyword is_enabled: Whether the network is enabled
        @type is_enabled: bool
        @keyword is_external: Wehter the network is external
        @type is_external: bool
        @keyword is_port_security_enabled: Whether the network is secured
        @type is_port_security_enabled: bool
        @keyword segments: Segments
        @type segments: str
        @keyword provider_physical_network: (Provider) physical network
        @type provider_physical_network: str
        @keyword provider_network_type: (Provider) network type
        @type provider_network_type: str
        @keyword provider_segmentation_id: (Provider) segmentation ID
        @type provider_segmentation_id: int
        @keyword vlan_transparent: (Provider) VLAN transparent
        @type vlan_transparent: int
        @return: Created network
        @rtype: yakumo.neutron.v2.network.Resource
        """
        return super(Manager, self).create(
            name=name,
            is_shared=is_shared,
            project=project,
            is_enabled=is_enabled,
            is_external=is_external,
            is_port_security_enabled=is_port_security_enabled,
            segments=segments,
            provider_physical_network=provider_physical_network,
            provider_network_type=provider_network_type,
            provider_segmentation_id=provider_segmentation_id,
            vlan_transparent=vlan_transparent)
