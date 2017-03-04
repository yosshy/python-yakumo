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
Resource class and its manager for floating IPs in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('fixed_ip', 'fixed_ip', mapper.Noop),
    ('server', 'instance_id', mapper.Resource('nova.server')),
    ('ip', 'ip', mapper.Noop),
    ('pool', 'pool', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for floating IPs in Compute API v2"""

    def associate(self, server=None):
        """
        Associate a floating IP

        @keyword server: Server
        @type server: yakumo.nova.v2.server.Resource
        @rtype: None
        """
        self._http.post('/servers/%s/action' % server.get_id(),
                        data=utils.get_json_body(
                            'addFloatingIp', address=self.ip))

    def disassociate(self):
        """
        Disassociate a floating IP

        @rtype: None
        """
        self._http.post('/servers/%s/action' % self.server.id,
                        data=utils.get_json_body(
                            'removeFloatingIp', address=self.ip))

    def deallocate(self):
        """
        Deallocate a floating IP

        @rtype: None
        """
        super(Resource, self).delete()


class Manager(base.Manager):
    """Manager class for floating IPs in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "update", "delete"]
    _json_resource_key = 'floating_ip'
    _json_resources_key = 'floating_ips'
    _url_resource_path = '/os-floating-ips'

    def allocate(self, pool=UNDEF):
        """Allocate a new floating IP

        @keyword pool: Pool name
        @type pool: str
        @return: Allocated floating IP address
        @rtype: yakumo.nova.v2.floating_ip.Resource
        """
        return super(Manager, self).create(pool=pool)

    def list_pools(self):
        """
        List floating IP pools

        @return: Floating IP pool list
        @rtype: [str]
        """
        ret = self._http.get('/os-floating-ip-pools')
        return [x["name"] for x in ret.get("floating_ip_pools", [])]
