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
Resource class and its manager for quotas in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('project', 'tenant_id', mapper.Resource('project')),
    ('subnet', 'subnet', mapper.Noop),
    ('ikepolicy', 'ikepolicy', mapper.Noop),
    ('subnetpool', 'subnetpool', mapper.Noop),
    ('network', 'network', mapper.Noop),
    ('ipsec_site_connection', 'ipsec_site_connection', mapper.Noop),
    ('floatingip', 'floatingip', mapper.Noop),
    ('ipsecpolicy', 'ipsecpolicy', mapper.Noop),
    ('security_group_rule', 'security_group_rule', mapper.Noop),
    ('vpnservice', 'vpnservice', mapper.Noop),
    ('security_group', 'security_group', mapper.Noop),
    ('router', 'router', mapper.Noop),
    ('port', 'po', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for quotas in Networking V2 API"""

    def update(self, subnet=UNDEF, ikepolicy=UNDEF, subnetpool=UNDEF,
               network=UNDEF, ipsec_site_connection=UNDEF, floatingip=UNDEF,
               ipsecpolicy=UNDEF, security_group_rule=UNDEF, vpnservice=UNDEF,
               security_group=UNDEF, router=UNDEF, port=UNDEF):
        """
        Update properties of a quota

        @keyword subnet: Maximum number of subnets
        @type subnet: int
        @keyword ikepolicy: Maximum number of IKE policies
        @type ikepolicy: int
        @keyword subnetpool: Maximum number of subnet pools
        @type subnetpool: int
        @keyword network: Maximum number of networks
        @type network: int
        @keyword ipsec_site_connection: Maximum number of IPSec site
        connections
        @type ipsec_site_connection: int
        @keyword floatingip: Maximum number of floating IPs
        @type floatingip: int
        @keyword ipsecpolicy: Maximum number of IPSec policies
        @type ipsecpolicy: int
        @keyword security_group_rule: Maximum number of security group rules
        @type security_group_rule: int
        @keyword vpnservice: Maximum number of VPN services
        @type vpnservice: int
        @keyword security_group: Maximum number of security groups
        @type security_group: int
        @keyword router: Maximum number of routers
        @type router: int
        @keyword port: Maximum number of ports
        @type port: int
        """
        super(Resource, self).update(
            subnet=subnet,
            ikepolicy=ikepolicy,
            subnetpool=subnetpool,
            network=network,
            ipsec_site_connection=ipsec_site_connection,
            floatingip=floatingip,
            ipsecpolicy=ipsecpolicy,
            security_group_rule=security_group_rule,
            vpnservice=vpnservice,
            security_group=security_group,
            router=router,
            port=port)

    def delete(self):
        try:
            self._http.delete(self._url_resource_path, self.project)
        except:
            return None


class Manager(base.Manager):
    """Manager class for quotas in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create"]
    _id_attr = 'project'
    _json_resource_key = 'quota'
    _json_resources_key = 'quotas'
    _url_resource_path = '/v2.0/quotas'

    def get(self, project):
        try:
            id = project._id
            ret = self._http.get(self._url_resource_path, id)
            json_params = ret.get(self._json_resource_key)
            json_params['tenant_id'] = id
            attrs = self._json2attr(json_params)
            return self.resource_class(self, **attrs)
        except:
            return None
