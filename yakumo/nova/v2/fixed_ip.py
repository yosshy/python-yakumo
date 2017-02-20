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
Resource class and its manager for fixed IPs in Compute API v2
"""

from yakumo import base
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('ip', '', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for fixed IPs in Compute API v2"""


class Manager(base.Manager):
    """Manager class for fixed IPs in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "list", "update"]
    _id_attr = 'ip'
    _json_resource_key = 'fixed_ip'
    _url_resource_path = '/os-fixed-ips'

    def get(self, ip=None):
        """
        Get information for fixed IP

        @keyword ip: Fixed IP (required)
        @type ip: str
        @return: Information of the fixed IP
        @rtype: str
        """
        ret = self._http.get(self._url_resource_path, ip)
        return ret.get('fixed_ip')

    def reserve(self, ip=None):
        """
        Reserve a fixed IP

        @keyword ip: Fixed IP (required)
        @type ip: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, ip, 'action',
                        data=dict(reserve=None))

    def unreserve(self, ip=None):
        """
        Release a fixed IP

        @keyword ip: Fixed IP (required)
        @type ip: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, ip, 'action',
                        data=dict(unreserve=None))
