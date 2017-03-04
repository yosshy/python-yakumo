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
Resource class and its manager for VPN services in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('router', 'router_id', mapper.Resource('neutron.router')),
    ('subnet', 'subnet_id', mapper.Resource('neutron.subnet')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('status', 'status', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for VPN services in Networking V2 API"""

    def update(self, name=UNDEF, description=UNDEF, router=UNDEF,
               subnet=UNDEF, project=UNDEF, is_enabled=UNDEF):
        """
        Update properties of a VPN service

        @keyword name: VPN service name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Is vpn enabled
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            is_enabled=is_enabled)


class Manager(base.Manager):
    """Manager class for VPN services in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'vpnservice'
    _json_resources_key = 'vpnservices'
    _url_resource_path = '/v2.0/vpn/vpnservices'

    def create(self, name=UNDEF, description=UNDEF, router=UNDEF,
               subnet=UNDEF, project=UNDEF, is_enabled=UNDEF):
        """
        Create a VPN service

        @keyword name: VPN name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword router: Router object
        @type router: yakumo.neutron.v2.router.Resource
        @keyword subnet: Subnet object
        @type subnet: yakumo.neutron.v2.subnet.Resource
        @keyword project: Project object
        @type project: yakumo.project.Resource
        @keyword is_enabled: Whether the VPN service is enabled
        @type is_enabled: bool
        @return: Created VPN service
        @rtype: yakumo.neutron.v2.vpn.service.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            router=router,
            subnet=subnet,
            project=project,
            is_enabled=is_enabled)
