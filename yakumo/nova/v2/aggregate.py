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
Resource class and its manager for aggregates in Compute API v2
"""

from yakumo import base
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.StrInt),
    ('name', 'name', mapper.Noop),
    ('hosts', 'hosts', mapper.Noop),
    ('availability_zone', 'availability_zone',
     mapper.Resource('nova.availability_zone')),
    ('metadata', 'metadata', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('deleted_at', 'deleted_at', mapper.DateTime),
    ('is_deleted', 'deleted', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for aggregates in Compute API v2"""

    def update(self, name=None, availability_zone=None):
        """
        Update properties of a host aggregate

        @keyword name: Name of the host aggregate
        @type name: str
        @keyword availability_zone: Name of availability zone
        @type availability_zone: str
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            availability_zone=availability_zone)

    def add_host(self, host=None):
        """
        Create a host aggregate

        @keyword host: host name
        @type host: host name
        @rtype: None
        """
        return self._http.post(self._url_resource_path, self._id, "action",
                               data=utils.get_json_body("add_host", host=host))

    def remove_host(self, host=None):
        """
        Remove a host aggregate

        @keyword host: host name
        @type host: host name
        @rtype: None
        """
        return self._http.post(self._url_resource_path, self._id, "action",
                               data=utils.get_json_body("remove_host",
                                                        host=host))

    def set_metadata(self, metadata=None):
        """
        Remove a host aggregate

        @keyword metadata: key=value parameters
        @type metadata: dict
        @rtype: None
        """
        return self._http.post(self._url_resource_path, self._id, "action",
                               data={"set_metadata": {"metadata": kwargs}})


class Manager(base.Manager):
    """Manager class for aggregates in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'aggregate'
    _json_resources_key = 'aggregates'
    _url_resource_path = '/os-aggregates'

    def create(self, name=None, availability_zone=None):
        """
        Create a host aggregate

        @keyword name: name of the host aggregate
        @type name: str
        @keyword availability_zone: name of availability zone
        @type availability_zone: str
        @return: Created host aggregate
        @rtype: yakumo.nova.v2.aggregate.Resource
        """
        return super(Manager, self).create(
            name=name,
            availability_zone=availability_zone)
