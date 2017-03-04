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
Resource class and its manager for floating IP bulks in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('ip', 'address', mapper.Noop),
    ('ip_range', 'ip_range', mapper.Noop),
    ('server', 'instance_uuid', mapper.Resource('nova.server')),
    ('interface', 'interface', mapper.Noop),
    ('project', 'project_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for floating IP bulks in Compute API v2"""


class Manager(base.Manager):
    """Manager class for floating IP bulks in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _id_attr = 'ip'
    _json_resource_key = 'floating_ip_info'
    _json_resources_key = 'floating_ip_info'
    _url_resource_path = '/os-floating-ips-bulk'

    def find_gen(self, host=None):
        """
        Bulk-get floating IPs

        :param host=: hostname (str)
        """
        ret = self._http.get(self._url_resource_path, host)
        for x in ret.get('floating_ip_info'):
            attrs = self._json2attr(x)
            yield self.resource_class(self, **attrs)

    def create(self, pool=UNDEF, ip_range=UNDEF, interface=UNDEF):
        """
        Bulk-create floating IPs

        @keyword pool: Pool name (str, required)
        @type pool: Pool name (str, required)
        @keyword ip_range: CIDR like '192.168.1.0/24' (str, required)
        @type ip_range: CIDR like '192.168.1.0/24' (str, required)
        @keyword interface: Interface name like 'eth0' (str)
        @type interface: Interface name like 'eth0' (str)
        @rtype: None
        """
        self._http.post(self._url_resource_path,
                        data=utils.get_json_body(
                            "floating_ips_bulk_create",
                            ip_range=ip_range,
                            pool=pool,
                            interface=interface))

    def delete(self, ip_range=None):
        """
        Bulk-create floating IPs

        @keyword ip_range: CIDR like '192.168.1.0/24' (required)
        @type ip_range: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, 'delete',
                       data=dict(ip_range=ip_range))
