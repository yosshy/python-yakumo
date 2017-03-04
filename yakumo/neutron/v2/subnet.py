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
Resource class and its manager for subnets in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('network', 'network_id', mapper.Resource('neutron.network')),
    ('gateway_ip', 'gateway_ip', mapper.Noop),
    ('dns_nameservers', 'dns_nameservers', mapper.Noop),
    ('host_route', 'host_route', mapper.Noop),
    ('ip_version', 'ip_version', mapper.Noop),
    ('cidr', 'cidr', mapper.Noop),
    ('is_dhcp_enabled', 'enable_dhcp', mapper.Noop),
    ('ipv6_ra_mode', 'ipv6_ra_mode', mapper.Noop),
    ('ipv6_address_mode', 'ipv6_address_mode', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for subnets in Networking V2 API"""

    def update(self, name=UNDEF, allocation_pools=UNDEF, gateway_ip=UNDEF,
               is_dhcp_enabled=UNDEF, dns_nameservers=UNDEF,
               host_routes=UNDEF):
        """
        Update properties of a subnet
        @keyword name: Subnet name
        @type name: str
        @keyword allocation_pools: Allocation pools
        @type allocation_pools: str
        @keyword gateway_ip: Gateway IP address
        @type gateway_ip: str
        @keyword is_dhcp_enabled: Whether DHCP is enabled
        @type is_dhcp_enabled: bool
        @keyword dns_nameservers: DNS nameservers
        @type dns_nameservers: str
        @keyword host_routes: Host routes
        @type host_routes: str
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            allocation_pools=allocation_pools,
            gateway_ip=gateway_ip,
            is_dhcp_enabled=is_dhcp_enabled,
            dns_nameservers=dns_nameservers,
            host_routes=host_routes)


class Manager(base.Manager):
    """Manager class for subnets in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'subnet'
    _json_resources_key = 'subnets'
    _url_resource_path = '/v2.0/subnets'

    def create(self, name=UNDEF, network=UNDEF, project=UNDEF,
               allocation_pools=UNDEF, gateway_ip=UNDEF, ip_version=UNDEF,
               cidr=UNDEF, is_dhcp_enabled=UNDEF, dns_nameservers=UNDEF,
               host_routes=UNDEF, ipv6_ra_mode=UNDEF, ipv6_address_mode=UNDEF):
        """
        Create a subnet

        @keyword name: Subnet name
        @type name: str
        @keyword network: Network
        @type network: yakumo.neutron.v2.network.Resource
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword allocation_pools: Allocation pools
        @type allocation_pools: str
        @keyword gateway_ip: Gateway IP address
        @type gateway_ip: str
        @keyword ip_version: IP version
        @type ip_version: int
        @keyword cidr: CIDR
        @type cidr: str
        @keyword is_dhcp_enabled: Whether DHCP is enabled
        @type is_dhcp_enabled: bool
        @keyword dns_nameservers: DNS nameservers
        @type dns_nameservers: str
        @keyword host_routes: Host routes
        @type host_routes: str
        @keyword ipv6_ra_mode: IPv6 RA mode
        @type ipv6_ra_mode: str
        @keyword ipv6_address_mode: IPv6 address mode
        @type ipv6_address_mode: str
        @return: Created subnet
        @rtype: yakumo.neutron.v2.subnet.Resource
        """
        return super(Manager, self).create(
            name=name,
            network=network,
            project=project,
            allocation_pools=allocation_pools,
            gateway_ip=gateway_ip,
            ip_version=ip_version, cidr=cidr,
            is_dhcp_enabled=is_dhcp_enabled,
            dns_nameservers=dns_nameservers,
            host_routes=host_routes,
            ipv6_ra_mode=ipv6_ra_mode,
            ipv6_address_mode=ipv6_address_mode)
