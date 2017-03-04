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
Resource class and its manager for floating IPs in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('floating_network', 'floating_network_id',
     mapper.Resource('neutron.network')),
    ('floating_ip', 'floating_ip_address', mapper.Noop),
    ('fixed_ip', 'fixed_ip_address', mapper.Noop),
    ('router', 'router_id', mapper.Resource('neutron.router')),
    ('port', 'port_id', mapper.Resource('neutron.port')),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for floating IPs in Networking V2 API"""

    def update(self, floating_ip=UNDEF, port=UNDEF):
        """
        Update a floting IP address

        @keyword floating_ip: Floating IP address
        @type floating_ip: str
        @keyword port: Port
        @type port: yakumo.neutron.v2.port
        @rtype: None
        """
        super(Resource, self).update(
            floating_ip=floating_ip,
            port=port
        )

    def associate(self, port=None):
        """
        Associate a floting IP address with a port

        @keyword port: Port
        @type port: yakumo.neutron.v2.port
        @rtype: None
        """
        super(Resource, self).update(port=port)

    def disassociate(self):
        """
        Disassociate a floting IP address

        @rtype: None
        """
        super(Resource, self).update(port=None)


class Manager(base.Manager):
    """Manager class for floating IPs in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'floatingip'
    _json_resources_key = 'floatingips'
    _url_resource_path = '/v2.0/floatingips'

    def create(self, project=UNDEF, floating_network=UNDEF,
               fixed_ip=UNDEF, floating_ip=UNDEF, port=UNDEF):
        """
        Aquire a floating IP address

        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword floating_network: Network
        @type floating_network: yakumo.neutron.v2.network.Resource
        @keyword fixed_ip: Fixed IP address to map
        @type fixed_ip: str
        @keyword port: Port
        @type port: yakumo.neutron.v2.port
        @return: Mapped Floating IP address
        @rtype: yakumo.neutron.v2.floating_ip.Resource
        """
        return super(Manager, self).create(
            project=project,
            floating_network=floating_network,
            fixed_ip=fixed_ip,
            floating_ip=floating_ip,
            port=port
        )
