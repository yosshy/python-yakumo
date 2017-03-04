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
Resource class and its manager for security group rules in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('direction', 'direction', mapper.Noop),
    ('ethertype', 'ethertype', mapper.Noop),
    ('remote_ip_prefix', 'remote_ip_prefix', mapper.Noop),
    ('port_range_max', 'port_range_max', mapper.Noop),
    ('port_range_min', 'port_range_min', mapper.Noop),
    ('protocol', 'protocol', mapper.Noop),
    ('security_group', 'security_group_id',
     mapper.Resource('neutron.security_group')),
    ('remote_group', 'remote_group_id',
     mapper.Resource('neutron.security_group')),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for security group rules in Networking V2 API"""


class Manager(base.SubManager):
    """Manager class for security group rules in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'security_group_rule'
    _json_resources_key = 'security_group_rules'
    _url_resource_path = '/v2.0/security-group-rules'

    def create(self, direction=UNDEF, ethertype=UNDEF,
               port_range_min=UNDEF, port_range_max=UNDEF,
               protocol=UNDEF, remote_group=UNDEF, remote_ip_prefix=UNDEF):
        """
        Register a rule of a security group

        @keyword direction: Direction (ingress or egress)
        @type direction: str
        @keyword ethertype: Ether type
        @typt ethertype: str
        @keyword port_range_min: Minimum number of the port range
        @type port_range_min: int
        @keyword port_range_max: Maximum number of the port range
        @type port_range_max: int
        @keyword protocol: Protocol (tcp, udp or icmp)
        @type protocol: str
        @keyword remote_group: Remote group
        @type remote_group:
        @keyword remote_ip_prefix: Remote IP address prefix
        @type remote_ip_prefix: str
        @return: Created rule
        @rtype: yakumo.neutron.v2.security_group_rule.Resource
        """
        security_group = self.parent_resource
        return super(Manager, self).create(direction=direction,
                                           ethertype=ethertype,
                                           security_group=security_group,
                                           port_range_min=port_range_min,
                                           port_range_max=port_range_max,
                                           protocol=protocol,
                                           remote_group=remote_group,
                                           remote_ip_prefix=remote_ip_prefix)

    def _find_gen(self, **kwargs):
        """
        Find a security group rule

        :param key=value: search condition
        """
        kwargs['security_group'] = self.parent_resource
        return super(Manager, self)._find_gen(**kwargs)
