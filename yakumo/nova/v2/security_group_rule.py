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
Resource class and its manager for security group rules in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('remote_ip_prefix', 'ip_range', mapper.Noop),
    ('port_range_min', 'from_port', mapper.Noop),
    ('port_range_max', 'to_port', mapper.Noop),
    ('protocol', 'ip_protocol', mapper.Noop),
    ('group', 'group', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for security group rules in Compute API v2"""

    def delete(self):
        """
        Delete a security group rule

        @rtype: None
        """
        super(Resource, self).delete()
        self._reload_rules()


class Manager(base.SubManager):
    """Manager class for security group rules in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'security_group_rule'
    _json_resources_key = 'security_group_rules'
    _url_resource_path = '/os-security-group-rules'

    def __init__(self, parent_resource, *args, **kwargs):
        super(Manager, self).__init__(parent_resource, *args, **kwargs)
        if self.parent_resource._rules:
            self._rules = [self.resource_class(self, **self._json2attr(x))
                           for x in self.parent_resource._rules]
        else:
            self._rules = []

    def _reload_rules(self):
        self.parent_resource.get()
        if self.parent_resource._rules:
            self._rules = [self.resource_class(self, **self._json2attr(x))
                           for x in self.parent_resource._rules]
        else:
            self._rules = []

    def create(self, remote_ip_prefix=UNDEF, port_range_min=UNDEF,
               port_range_max=UNDEF, protocol=UNDEF, group=UNDEF,
               project=UNDEF):
        """
        Create a security group rule

        @keyword remote_ip_prefix: IP range (e.q. '0.0.0.0/0', required)
        @type remote_ip_prefix: str
        @keyword port_range_min: lower number of destination port
        @type port_range_min: int
        @keyword port_range_max: upper number of destination port
        @type port_range_max: int
        @keyword protocol: protocol name ('tcp', 'udp', or 'icmp')
        @type protocol: str
        @keyword group: List of a project and a security group name
        @type group: [(yakumo.project.Resource, str)]
        @keyword project: Project
        @type project: yakumo.project.Resource
        @return: Created security group rule
        @rtype: yakumo.nova.v2.security_group_rule.Resource
        """
        ret = super(Manager, self).create(remote_ip_prefix=remote_ip_prefix,
                                          port_range_min=port_range_min,
                                          port_range_max=port_range_max,
                                          protocol=protocol,
                                          group=group,
                                          project=project)
        self._reload_rules()
        return ret

    def get(self, id):
        """
        Get a security group rule

        @keyword id: Security group rule ID
        @type id: str
        @return: Created security group rule
        @rtype: yakumo.nova.v2.security_group_rule.Resource
        """
        for rule in self._rules:
            if rule.id == id:
                return rule

    def _find_gen(self, **kwargs):
        """
        Find a security group rule

        :param key=value: search condition
        """
        for sg_rule in self._rules:
            for k, v in kwargs.items():
                if getattr(sg_rule, k, None) != v:
                    break
            else:
                yield sg_rule
