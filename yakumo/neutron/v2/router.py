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
Resource class and its manager for routers in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


FIXED_IP_MAPPING = [
    ('ip_address', 'ip_address', mapper.Noop),
    ('subnet', 'subnet_id', mapper.Resource('subnet'))
]


EXTERNAL_GATEWAY_INFO_MAPPING = [
    ('network', 'network_id', mapper.Resource('network')),
    ('is_snat_enabled', 'enable_snat', mapper.Noop),
    ('external_fixed_ips', 'external_fixed_ips',
     mapper.List(mapper.Dict(FIXED_IP_MAPPING)))
]


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('routes', 'routes', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('external_gateway_info', 'external_gateway_info',
     mapper.Dict(EXTERNAL_GATEWAY_INFO_MAPPING)),
    ('is_distributed', 'distributed', mapper.Noop),
    ('is_ha', 'ha', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for routers in Networking V2 API"""

    def update(self, name=UNDEF, routes=UNDEF,
               external_gateway_info=UNDEF, is_enabled=UNDEF):
        """
        Update properties of a router

        @keyword name: Router name
        @type name: str
        @keyword routes: Routings
        @type routes: str
        @keyword external_gateway_info: External gateway infomation
        @type external_gateway_info: str
        @keyword is_enabled: Whether the router is enabled
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            router=router,
            external_gateway_info=external_gateway_info,
            is_enabled=is_enabled)

    def add_interface(self, subnet=None, port=None):
        """
        Add an interface for router

        Either subnet or port is required.

        @keyword subnet: Subnet
        @type subnet: yakumo.neutron.v2.subnet.Resource
        @keyword port: Port
        @type port: yakumo.neutron.v2.subnet.Resource
        @rtype: None
        """
        if port:
            self._http.put(self._url_resource_path, self._id,
                           'add_router_interface',
                           data=dict(port_id=port.get_id()))
        elif subnet:
            self._http.put(self._url_resource_path, self._id,
                           'add_router_interface',
                           data=dict(subnet_id=subnet.get_id()))

    def remove_interface(self, subnet=None, port=None):
        """
        Remove an interface for router

        Either subnet or port is required.

        @keyword subnet: Subnet
        @type subnet: yakumo.neutron.v2.subnet.Resource
        @keyword port: Port
        @type port: yakumo.neutron.v2.subnet.Resource
        @rtype: None
        """
        if port:
            self._http.put(self._url_resource_path, self._id,
                           'remove_router_interface',
                           data=dict(port_id=port.get_id()))
        elif subnet:
            self._http.put(self._url_resource_path, self._id,
                           'remove_router_interface',
                           data=dict(subnet_id=subnet.get_id()))


class Manager(base.Manager):
    """Manager class for routers in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'router'
    _json_resources_key = 'routers'
    _url_resource_path = '/v2.0/routers'

    def create(self, name=UNDEF, routes=UNDEF, is_enabled=UNDEF):
        """
        Create a router

        @keyword name: Router name
        @type name: str
        @keyword routes: Routings
        @type routes: str
        @keyword is_enabled: Whether the router is enabled
        @type is_enabled: bool
        @return: Created router
        @rtype: yakumo.neutron.v2.router.Resource
        """
        return super(Manager, self).create(name=name, routes=routes,
                                           is_enabled=is_enabled)
