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
Resource class and its manager for VPN IPSec site connections in
Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('peer_address', 'peer_address', mapper.Noop),
    ('peer_id', 'peer_id', mapper.Noop),
    ('local_ep_group_id', 'local_ep_group_id', mapper.Noop),
    ('peer_ep_group_id', 'peer_ep_group_id', mapper.Noop),
    ('peer_cidrs', 'peer_cidrs', mapper.Noop),
    ('route_mode', 'route_mode', mapper.Noop),
    ('mtu', 'mtu', mapper.Noop),
    ('auth_mode', 'auth_mode', mapper.Noop),
    ('psk', 'psk', mapper.Noop),
    ('initiator', 'initiator', mapper.Noop),
    ('ikepolicy', 'ikepolicy_id',
     mapper.Resource('neutron.vpn.ikepolicy')),
    ('ipsecpolicy', 'ipsecpolicy_id',
     mapper.Resource('neutron.vpn.ipsecpolicy')),
    ('vpnservice', 'vpnservice_id',
     mapper.Resource('neutron.vpn.vpnservice')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('dpd', 'dpd', mapper.Noop),
    ('action', 'action', mapper.Noop),
    ('interval', 'interval', mapper.Noop),
    ('timeout', 'timeout', mapper.Noop),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('status', 'status', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for VPN IPSec site connections in Networking V2 API"""

    def update(self, name=UNDEF, description=UNDEF,
               peer_address=UNDEF, peer_id=UNDEF,
               local_ep_group_id=UNDEF, peer_ep_group_id=UNDEF,
               peer_cidrs=UNDEF, mtu=UNDEF, psk=UNDEF, initiator=UNDEF,
               dpd=UNDEF, action=UNDEF, interval=UNDEF, timeout=UNDEF,
               is_enabled=UNDEF):

        """
        Update properties of an IPSec site connection

        @keyword name: IPSec site connection name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword peer_address: Peer address
        @type peer_address: str
        @keyword peer_id: Peer ID
        @type peer_id: str
        @keyword local_ep_group_id: Local EP group ID
        @type local_ep_group_id: str
        @keyword peer_ep_group_id: Peer EP group ID
        @type peer_ep_group_id: str
        @keyword peer_cidrs: Peer CIDRs
        @type peer_cidrs: str
        @keyword mtu: MTU
        @type mtu: int
        @keyword psk: PSK
        @type psk: str
        @keyword initiator: Initiator
        @type initiator: str
        @keyword dpd: DPD
        @type dpd: str
        @keyword action: Action
        @type action: str
        @keyword interval: Interval
        @type interval: str
        @keyword timeout: Timeout
        @type timeout: int
        @keyword is_enabled: Whether the connection is enabled
        @type is_enabled: bool
        @rtype: None
        """
        return super(Resource, self).create(
            name=name,
            description=description,
            peer_address=peer_address,
            peer_id=peer_id,
            local_ep_group_id=local_ep_group_id,
            peer_ep_group_id=peer_ep_group_id,
            peer_cidrs=peer_cidrs,
            mtu=mtu,
            psk=psk,
            initiator=initiator,
            dpd=dpd,
            action=action,
            interval=interval,
            timeout=timeout,
            is_enabled=is_enabled
        )


class Manager(base.Manager):
    """Manager class for VPN IPSec site connections in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'ipsec_site_connection'
    _json_resources_key = 'ipsec_site_connections'
    _url_resource_path = '/v2.0/vpn/ipsec-site-connections'

    def create(self, name=UNDEF, description=UNDEF, peer_address=UNDEF,
               peer_id=UNDEF, local_ep_group_id=UNDEF,
               peer_ep_group_id=UNDEF, peer_cidrs=UNDEF,
               route_mode=UNDEF, mtu=UNDEF, auth_mode=UNDEF, psk=UNDEF,
               initiator=UNDEF, ikepolicy=UNDEF, ipsecpolicy=UNDEF,
               vpnservice=UNDEF, project=UNDEF, dpd=UNDEF, action=UNDEF,
               interval=UNDEF, timeout=UNDEF, is_enabled=UNDEF):

        """
        Create an IPSec site connection

        @keyword name: IPSec site connection name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword peer_address: Peer address
        @type peer_address: str
        @keyword peer_id: Peer ID
        @type peer_id: str
        @keyword local_ep_group_id: Local EP group ID
        @type local_ep_group_id: str
        @keyword peer_ep_group_id: Peer EP group ID
        @type peer_ep_group_id: str
        @keyword peer_cidrs: Peer CIDRs
        @type peer_cidrs: str
        @keyword route_mode: Route mode
        @type route_mode: str
        @keyword mtu: MTU
        @type mtu: int
        @keyword auth_mode: Auth mode
        @type auth_mode: str
        @keyword psk: PSK
        @type psk: str
        @keyword initiator: Initiator
        @type initiator: str
        @keyword ikepolicy: IKE policy
        @type ikepolicy: str
        @keyword ipsecpolicy: IPSec policy
        @type ipsecpolicy: str
        @keyword vpnservice: VPN service
        @type vpnservice: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword dpd: DPD
        @type dpd: str
        @keyword action: Action
        @type action: str
        @keyword interval: Interval
        @type interval: str
        @keyword timeout: Timeout
        @type timeout: int
        @keyword is_enabled: Whether the connection is enabled
        @type is_enabled: bool
        @return: Created connection
        @rtype: yakumo.neutron.v2.vpn.ipsec_site_connection.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            peer_address=peer_address,
            peer_id=peer_id,
            local_ep_group_id=local_ep_group_id,
            peer_ep_group_id=peer_ep_group_id,
            peer_cidrs=peer_cidrs,
            route_mode=route_mode,
            mtu=mtu,
            auth_mode=auth_mode,
            psk=psk,
            initiator=initiator,
            ikepolicy=ikepolicy,
            ipsecpolicy=ipsecpolicy,
            vpnservice=vpnservice,
            project=project,
            dpd=dpd,
            action=action,
            interval=interval,
            timeout=timeout,
            is_enabled=is_enabled
        )
