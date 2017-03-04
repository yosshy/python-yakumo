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
Resource class and its manager for LBaaS load balancers in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('listeners', 'listeners',
     mapper.List(mapper.Resource('neutron.lbaas.listener'))),
    ('vip_address', 'vip_address', mapper.Noop),
    ('subnet', 'vip_subnet_id', mapper.Resource('neutron.subnet')),
    ('operating_status', 'operating_status', mapper.Noop),
    ('provisioning_status', 'provisioning_status', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for LBaaS load balancers in Networking V2 API"""

    def update(self, name=UNDEF, description=UNDEF, is_enabled=UNDEF):
        """
        Update properties of a LBaaS listener

        @keyword name: Listener name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword is_enabled: Whether the listener is enabled
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            is_enabled=is_enabled)


class Manager(base.Manager):
    """Manager class for LBaaS load balancers in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'loadbalancer'
    _json_resources_key = 'loadbalancers'
    _url_resource_path = '/v2.0/lbaas/loadbalancers'

    def create(self, name=UNDEF, description=UNDEF, project=UNDEF,
               vip_subnet=UNDEF, vip_address=UNDEF, is_enabled=UNDEF,
               provider=UNDEF):
        """
        Create a LBaaS listener

        @keyword name: Listener name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword vip_subnet: VIP subnet
        @type vip_subnet: str
        @keyword vip_address: VIP address
        @type vip_address: str
        @keyword provider: Provider
        @type provider: str
        @keyword is_enabled: Whether the listener is enabled
        @type is_enabled: bool
        @return: Created listener
        @rtype: yakumo.neutron.v2.lbaas.load_balancer.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            project=project,
            vip_subnet=vip_subnet,
            vip_address=vip_address,
            is_enabled=is_enabled,
            provider=provider)
