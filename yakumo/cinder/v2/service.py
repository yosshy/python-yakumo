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
Resource class and its manager for services in Block Storage API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('host', 'host', mapper.Noop),
    ('binary', 'binary', mapper.Noop),
    ('state', 'state', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('availability_zone', 'zone',
     mapper.Resource('nova.availability_zone')),
    ('disabled_reason', 'disabled_reason', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for services in Block Storage API v2"""

    def enable(self):
        """
        Enable a service on a host

        @rtype: None
        """
        self._manager.enable(host=self.host, binary=self.binary)

    def disable(self):
        """
        Disable a service on a host

        @rtype: None
        """
        self._manager.disable(host=self.host, binary=self.binary)

    def set_disabled_reason(self, reason=None):
        """
        Set disabled reason for a service on a host

        @keyword reason: Description
        @type reason: str
        @rtype: None
        """
        self._manager.set_disabled_reason(host=self.host, binary=self.binary,
                                          reason=reason)

    def update(self, name=UNDEF, availability_zone=UNDEF):
        """
        Create a host aggregate

        @keyword name: name of the host aggregate
        @type name: str
        @keyword availability_zone: name of availability zone
        @type availability_zone: str
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            availability_zone=availability_zone)


class Manager(base.Manager):
    """Manager class for services in Block Storage API v2"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create"]
    _json_resource_key = 'service'
    _json_resources_key = 'services'
    _url_resource_path = '/os-services'

    def enable(self, host=None, binary=None):
        """
        Enable a service on a host

        @keyword host: host name (required)
        @type host: str
        @keyword binary: binary name (required)
        @type binary: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, "enable",
                       data=dict(host=host, binary=binary))

    def disable(self, host=None, binary=None):
        """
        Disable a service on a host

        @keyword host: host name (required)
        @type host: str
        @keyword binary: binary name (required)
        @type binary: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, "disable",
                       data=dict(host=host, binary=binary))

    def set_disabled_reason(self, host=None, binary=None, reason=None):
        """
        Set disabled reason for a service on a host

        @keyword host: host name (required)
        @type host: str
        @keyword binary: binary name (required)
        @type binary: str
        @keyword reason: description (required)
        @type reason: str
        @rtype: None
        """
        self._http.put(self._url_resource_path, "disable-log-reason",
                       data=dict(host=host, binary=binary,
                                 disabled_reason=reason))
