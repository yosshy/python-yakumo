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
Resource class and its manager for LB Pools in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils
from . import member
from . import vip


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('lb_method', 'lb_method', mapper.Noop),
    ('protocol', 'protocol', mapper.Noop),
    ('subnet', 'subnet_id', mapper.Resource('neutron.subnet')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('health_monitors', 'health_monitors',
     mapper.List(mapper.Resource('neutron.lb.health_monitor'))),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('status', 'status', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for LB Pools in Networking V2 API"""

    _sub_manager_list = {
        'member': member.Manager,
        'vip': vip.Manager
    }

    def update(self, name=UNDEF, lb_method=UNDEF):
        """
        Update properties of a load balancer pool

        @keyword name: Pool name (str)
        @type name: Pool name (str)
        @keyword lb_method: Load balance method (str)
        ('ROUND_ROBIN', 'LEAST_CONNECTIONS' or 'SOURCE_IP')
        @type lb_method: Load balance method (str)
        @rtype: None
        """
        super(Resource, self).update(name=name, lb_method=lb_method)

    def add_health_monitor(self, health_monitor=None):
        """
        Add a health monitor to a pool

        @keyword health_monitor: Health monitor
        @type health_monitor: yakumo.neutron.v2.lb.health_monitor.Resource
        @rtype: None
        """
        self._http.post(self._url_resource_path, "health_monitors",
                        data=dict(health_monitor=health_monitor.id))

    def remove_health_monitor(self, health_monitor=None):
        """
        Remove a health monitor from a pool

        @keyword health_monitor: Health monitor
        @type health_monitor: yakumo.neutron.v2.lb.health_monitor.Resource
        @rtype: None
        """
        self._http.delete(self._url_resource_path, "health_monitors",
                          health_monitor.id)


class Manager(base.Manager):
    """Manager class for LB Pools in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'pool'
    _json_resources_key = 'pools'
    _url_resource_path = '/v2.0/lb/pools'

    def create(self, name=UNDEF, description=UNDEF, lb_method=UNDEF,
               protocol=UNDEF, subnet=UNDEF, is_enabled=UNDEF):
        """
        Create a load balancer pool

        @keyword name: Pool name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword lb_method: Load balancing method
        ('ROUND_ROBIN', 'LEAST_CONNECTIONS' or 'SOURCE_IP')
        @type lb_method: str
        @keyword protocol: 'TCP', 'HTTP' or 'HTTPS'
        @type protocol: str
        @keyword subnet: Subnet
        @type subnet: yakumo.neutron.v2.subnet.Resource
        @keyword is_enabled: Whether the pool is enabled
        @type is_enabled: bool
        @return: Created pool
        @rtype: yakumo.neutron.v2.lb.pool.Resource
        """
        return super(Manager, self).create(name=name,
                                           description=description,
                                           lb_method=lb_method,
                                           protocol=protocol,
                                           subnet=subnet,
                                           is_enabled=is_enabled)
