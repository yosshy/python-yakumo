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
Resource class and its manager for floating IP DNS entries in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('domain', 'domain', mapper.Noop),
    ('project', 'project', mapper.Resource('project')),
    ('scope', 'scope', mapper.Noop),
    ('availability_zone', 'availability_zone',
     mapper.Resource('nova.availability_zone')),
]


class Resource(base.Resource):
    """Resource class for floating IP DNS entries in Compute API v2"""

    def update(self, new_domain=UNDEF, project=UNDEF, scope=UNDEF,
               availability_zone=UNDEF):
        """
        Update properties of a domain

        @keyword new_domain: New domain name
        @type new_domain: str
        @keyword project: Project object
        @type project: yakumo.project.Resource
        @keyword scope: 'public' or 'private'
        @type scope: str
        @keyword availability_zone: Availability zone name
        @type availability_zone: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, self._id,
                       data=utils.get_json_body(
                           'domain_entry',
                           domain=new_domain,
                           project=project,
                           scope=scope,
                           availability_zone=availability_zone))

    def add_entry(self, name=None, ip=None, dns_type="A"):
        """
        Add an entry

        @keyword name: Hostname
        @type name: str
        @keyword ip: IP address
        @type ip: str
        @keyword dns_type: DNS type
        @type dns_type: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, self._id,
                       data=utils.get_json_body(
                           'domain_entry',
                           domain=new_domain,
                           project=project,
                           scope=scope,
                           availability_zone=availability_zone))

    def remove_entry(self, name=None):
        """
        Remove an entry

        @keyword name: Hostname
        @type name: str
        @rtype: None
        """
        self._http.delete(self._url_resource_path, self._id, 'entries', name)

    def get_entry(self, ip=None):
        """
        Get DNS entries for an IP address

        @keyword ip: IP address
        @type ip: str
        @return: DNS entries
        @rtype: [str]
        """
        ret = self._http.get(self._url_resource_path, self._id, 'entries',
                             name)
        return ret.get('dns_entries')


class Manager(base.Manager):
    """Manager class for floating IP DNS entries in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _id_attr = 'domain'
    _json_resource_key = 'domain_entry'
    _json_resources_key = 'domain_entries'
    _url_resource_path = '/os-floating-ip-dns'

    def create(self, domain=UNDEF, project=UNDEF, scope=UNDEF,
               availability_zone=UNDEF):
        """
        Create a domain

        @keyword domain: Domain name (str, required)
        @type domain: str
        @keyword project: Project object
        @type project: yakumo.project.Resource
        @keyword scope: 'public' or 'private' (str)
        @type scope: str
        @keyword availability_zone: Availability zone name (str)
        @type availability_zone: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, domain,
                       data=utils.get_json_body(
                           'domain_entry',
                           domain=domain,
                           project=project,
                           scope=scope,
                           availability_zone=availability_zone))
