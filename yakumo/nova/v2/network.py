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
Resource class and its manager for networks in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('bridge', 'bridge', mapper.Noop),
    ('bridge_interface', 'bridge_interface', mapper.Noop),
    ('broadcast', 'broadcast', mapper.Noop),
    ('cidr', 'cidr', mapper.Noop),
    ('cidr_v6', 'cidr_v6', mapper.Noop),
    ('dhcp_server', 'dhcp_server', mapper.Noop),
    ('dhcp_start', 'dhcp_start', mapper.Noop),
    ('dns1', 'dns1', mapper.Noop),
    ('dns2', 'dns2', mapper.Noop),
    ('gateway', 'gateway', mapper.Noop),
    ('gateway_v6', 'gateway_v6', mapper.Noop),
    ('host', 'host', mapper.Noop),
    ('name', 'label', mapper.Noop),
    ('mtu', 'mtu', mapper.Noop),
    ('netmask', 'netmask', mapper.Noop),
    ('netmask_v6', 'netmask_v6', mapper.Noop),
    ('priority', 'priority', mapper.Noop),
    ('rxtx_base', 'rxtx_base', mapper.Noop),
    ('vlan', 'vlan', mapper.Noop),
    ('vpn_private_address', 'vpn_private_address', mapper.Noop),
    ('vpn_public_address', 'vpn_public_address', mapper.Noop),
    ('vpn_public_port', 'vpn_public_port', mapper.Noop),
    ('project', 'project_id', mapper.Resource('project')),
    ('created_at', 'created_at', mapper.DateTime),
    ('deleted_at', 'deleted_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('is_deleted', 'deleted', mapper.Noop),
    ('is_dhcp_enabled', 'enable_dhcp', mapper.Noop),
    ('is_injected', 'injected', mapper.Noop),
    ('is_address_shared', 'share_address', mapper.Noop),
    ('is_multi_host', 'multi_host', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for networks in Compute API v2"""

    def associate(self):
        """
        Associate a network

        @rtype: None
        """
        self._http.post(self._url_resource_path, 'add',
                        data=dict(id=self._id))

    def disassociate(self):
        """
        Disassociate a network

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=dict(disassociate=None))

    def associate_host(self, host=None):
        """
        Associate a host to a network

        @keyword host: UUID of a host (required)
        @type host: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=dict(associate_host=host))

    def disassociate_host(self, host=None):
        """
        Disassociate a host to a network

        @keyword host: UUID of a host (required)
        @type host: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=dict(disassociate_host=host))

    def disassociate_project(self, project=None):
        """
        Disassociate a host to a network

        @keyword project: Project
        @type project: yakumo.project.Resource
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=dict(disassociate_project=project.get_id()))


class Manager(base.Manager):
    """Manager class for networks in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'network'
    _json_resources_key = 'networks'
    _url_resource_path = '/os-networks'

    def create(self, bridge=UNDEF, bridge_interface=UNDEF, broadcast=UNDEF,
               cidr=UNDEF, cidr_v6=UNDEF, dhcp_server=UNDEF, dhcp_start=UNDEF,
               dns1=UNDEF, dns2=UNDEF, is_dhcp_enabled=UNDEF, gateway=UNDEF,
               gateway_v6=UNDEF, host=UNDEF, is_injected=UNDEF, name=UNDEF,
               mtu=UNDEF, is_multi_host=UNDEF, is_address_shared=UNDEF,
               netmask=UNDEF, netmask_v6=UNDEF, priority=UNDEF, project=UNDEF,
               rxtx_base=UNDEF, updated_at=UNDEF, vlan=UNDEF,
               vpn_private_address=UNDEF, vpn_public_address=UNDEF,
               vpn_public_port=UNDEF):
        """
        Create a network

        @keyword bridge: VIFs on this network are connected to this bridge
        @type bridge: str
        @keyword bridge_interface: The bridge is connected to this interface
        @type bridge_interface: str
        @keyword broadcast: The broadcast address
        @type broadcast: str
        @keyword cidr: IPv4 subnet
        @type cidr: str
        @keyword cidr_v6: IPv6 subnet
        @type cidr_v6: str
        @keyword dhcp_server: DHCP server address
        @type dhcp_server: str
        @keyword dhcp_start: DHCP starting address
        @type dhcp_start: str
        @keyword dns1: First DNS
        @type dns1: str
        @keyword dns2: Second DNS
        @type dns2: str
        @keyword is_dhcp_enabled: enable DHCP
        @type is_dhcp_enabled: str
        @keyword is_injected: Injected flag
        @type is_injected: str
        @keyword is_multi_host: Multi host
        @type is_multi_host: str
        @keyword is_address_shared: Share Address
        @type is_address_shared: str
        @keyword gateway: IPv4 gateway
        @type gateway: str
        @keyword gateway_v6: IPv6 gateway
        @type gateway_v6: str
        @keyword host: Network host
        @type host: str
        @keyword mtu: MTU
        @type mtu: int
        @keyword name: Network label
        @type name: str
        @keyword netmask: IPv4 netmask
        @type netmask: str
        @keyword netmask_v6: IPv6 netmask
        @type netmask_v6: str
        @keyword priority: Network priority
        @type priority: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword rxtx_base: RXTX base factor value for the network
        @type rxtx_base: str
        @keyword vlan: VLAN ID
        @type vlan: int
        @keyword vpn_private_address: VPN private address
        @type vpn_private_address: str
        @keyword vpn_public_address: VPN public address
        @type vpn_public_address: str
        @keyword vpn_public_port: VPN public port
        @type vpn_public_port: int
        @return: Created network
        @rtype: yakumo.nova.v2.network.Resource
        """
        return super(Manager, self).create(
            bridge=bridge,
            bridge_interface=bridge_interface,
            broadcast=broadcast,
            cidr=cidr,
            cidr_v6=cidr_v6,
            dhcp_server=dhcp_server,
            dhcp_start=dhcp_start,
            dns1=dns1,
            dns2=dns2,
            gateway=gateway,
            gateway_v6=gateway_v6,
            host=host,
            name=name,
            mtu=mtu,
            is_dhcp_enabled=is_dhcp_enabled,
            is_injected=is_injected,
            is_multi_host=is_multi_host,
            is_address_shared=is_address_shared,
            netmask=netmask,
            netmask_v6=netmask_v6,
            priority=priority,
            project=project,
            rxtx_base=rxtx_base,
            vlan=vlan,
            vpn_private_address=vpn_private_address,
            vpn_public_address=vpn_public_address,
            vpn_public_port=vpn_public_port)
