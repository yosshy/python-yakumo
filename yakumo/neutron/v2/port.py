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
Resource class and its manager for ports in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


FIXED_IP_MAPPING = [
    ('ip_address', 'ip_address', mapper.Noop),
    ('subnet', 'subnet_id', mapper.Resource('neutron.subnet')),
]


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('network', 'network_id', mapper.Resource('neutron.network')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('device', 'device_id', mapper.Noop),
    ('device_owner', 'device_owner', mapper.Noop),
    ('allowed_address_pairs', 'allowed_address_pairs', mapper.Noop),
    ('mac_address', 'mac_address', mapper.Noop),
    ('fixed_ips', 'fixed_ips', mapper.List(mapper.Dict(FIXED_IP_MAPPING))),
    ('security_groups', 'security_groups', mapper.Noop),
    ('is_enabled', 'admin_state_up', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for ports in Networking V2 API"""

    def update(self, name=UNDEF, network=UNDEF, project=UNDEF, device=UNDEF,
               device_owner=UNDEF, allowed_address_pairs=UNDEF,
               mac_address=UNDEF, fixed_ips=UNDEF, security_groups=UNDEF,
               is_enabled=UNDEF):
        """
        update properties of a port

        @keyword name: Port name
        @type name: str
        @keyword network: Network
        @type network: yakumo.neutron.v2.network.Resource
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword device: Attached device (server, router, floating IP, ...)
        @type device: Resource object
        @keyword device_owner: Device owner
        @type device_owner: str
        @keyword allowed_address_pairs: Allowed address pairs
        @type allowed_address_pairs: str
        @keyword mac_address: MAC address
        @type mac_address: str
        @keyword fixed_ips: List of dictionary with fixed IP and subnet
        @type fixed_ips: [{'ip_address': str,
                           'subnet': yakumo.subnet.Resource}]
        @keyword security_groups: Security groups
        @type security_groups: str
        @keyword is_enabled: Whether the port is enabled
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            network=network,
            project=project,
            device=device,
            device_owner=device_owner,
            allowed_address_pairs=allowed_address_pairs,
            mac_address=mac_address,
            fixed_ips=fixed_ips,
            security_groups=security_groups,
            is_enabled=is_enabled)


class Manager(base.Manager):
    """Manager class for ports in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'port'
    _json_resources_key = 'ports'
    _url_resource_path = '/v2.0/ports'

    def _attr2json(self, attrs):
        if isinstance(attrs['device'], base.Resource):
            attrs['device'] = attrs['device'].get_id()
        return super(Manager, self)._attr2json(attrs)

    def _json2attr(self, json_params):
        ret = super(Manager, self)._json2attr(json_params)
        owner = json_params.get('device_owner')
        device = ret['device']
        if owner in ('compute:nova', 'compute:None'):
            ret['device'] = self._client.server.get_empty(device)
        elif owner == 'network:router_interface':
            ret['device'] = self._client.router.get_empty(device)
        return ret

    def create(self, name=UNDEF, network=UNDEF, project=UNDEF, device=UNDEF,
               device_owner=UNDEF, allowed_address_pairs=UNDEF,
               mac_address=UNDEF, fixed_ips=UNDEF, security_groups=UNDEF,
               is_enabled=UNDEF):
        """
        Create a port

        @keyword name: Port name
        @type name: str
        @keyword network: Network
        @type network: yakumo.neutron.v2.network.Resource
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword device: Attached device (server, router, floating IP, ...)
        @type device: Resource object
        @keyword device_owner: Device owner
        @type device_owner: str
        @keyword allowed_address_pairs: Allowed address pairs
        @type allowed_address_pairs: str
        @keyword mac_address: MAC address
        @type mac_address: str
        @keyword fixed_ips: Fixed IP addresses
        @type fixed_ips: str
        @keyword security_groups: Security groups
        @type security_groups: str
        @keyword is_enabled: Whether the port is enabled
        @type is_enabled: bool
        @return: Created port
        @rtype: yakumo.neutron.v2.port.Resource
        """
        return super(Manager, self).create(
            name=name,
            network=network,
            project=project,
            device=device,
            device_owner=device_owner,
            allowed_address_pairs=allowed_address_pairs,
            mac_address=mac_address,
            fixed_ips=fixed_ips,
            security_groups=security_groups,
            is_enabled=is_enabled)
