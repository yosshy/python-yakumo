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
Resource class and its manager for security group default rules in
Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('cidr', 'ip_range', mapper.Noop),
    ('lower_port', 'from_port', mapper.Noop),
    ('upper_port', 'to_port', mapper.Noop),
    ('protocol', 'ip_protocol', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for security group default rules in Compute API v2"""


class Manager(base.Manager):
    """Manager class for security group default rules in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'security_group_default_rule'
    _json_resources_key = 'security_group_default_rules'
    _url_resource_path = '/os-security-group-default-rules'

    def create(self, cidr=UNDEF, lower_port=UNDEF, upper_port=UNDEF,
               protocol=UNDEF):
        """
        Create a security group

        @keyword cidr: IP range (e.q. '0.0.0.0/0', required)
        @type cidr: str
        @keyword lower_port: lower number of destination port
        @type lower_port: int
        @keyword upper_port: upper number of destination port
        @type upper_port: int
        @keyword protocol: protocol name ('tcp', 'udp', or 'icmp')
        @type protocol: str
        @return: Created security group
        @rtype: yakumo.nova.v2.security_group_default_rule.Resource
        """
        return super(Manager, self).create(cidr=cidr,
                                           lower_port=lower_port,
                                           upper_port=upper_port,
                                           protocol=protocol)
