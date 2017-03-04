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
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('hosts', 'hosts', mapper.Noop),
    ('availability_zone', 'availability_zone', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('deleted_at', 'deleted_at', mapper.DateTime),
    ('is_deleted', 'deleted', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for aggregates in Compute API v2"""

    def update(self, name=UNDEF, availability_zone=UNDEF):
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
        self.reload()

    def add_hosts(self, *hosts):
        """
        Register hosts to a host aggregate

        @params hosts: List of host names
        @type hosts: [str]
        @rtype: None
        """
        for host in hosts:
            self._http.post(self._url_resource_path, self._id, "action",
                            data=utils.get_json_body("add_host", host=host))
        self.reload()

    def remove_hosts(self, *hosts):
        """
        Unregister hosts from a host aggregate

        @keyword hosts: List of host names
        @type hosts: [str]
        @rtype: None
        """
        for host in hosts:
            self._http.post(self._url_resource_path, self._id, "action",
                            data=utils.get_json_body("remove_host",
                                                     host=host))
        self.reload()

    def get_metadata(self):
        """
        Aquire metadata of a host aggregate

        @return: Metadata
        @rtype: dict
        """
        return self.metadata

    def set_metadata(self, **metadata):
        """
        Set metadata for a host aggregate

        @keyword metadata: Metadata as key=value
        @type metadata: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, "action",
                        data={"set_metadata": {"metadata": metadata}})
        self.reload()

    def unset_metadata(self, *keys):
        """
        Remove metadata of a host aggregate

        @param keys: metadata keys to remove
        @type keys: [str]
        @rtype: None
        """
        metadata = self.metadata
        for key in keys:
            if key in metadata:
                metadata[key] = None
        self.set_metadata(**metadata)


class Manager(base.Manager):
    """Manager class for aggregates in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'aggregate'
    _json_resources_key = 'aggregates'
    _url_resource_path = '/os-aggregates'

    def _json2attr(self, json_params):
        if json_params.get('metadata', {}).get('availability_zone'):
            json_params['metadata'].pop('availability_zone')
        return super(Manager, self)._json2attr(json_params)

    def create(self, name=UNDEF, availability_zone=UNDEF, metadata=UNDEF):
        """
        Create a host aggregate

        @keyword name: name of the host aggregate
        @type name: str
        @keyword availability_zone: name of availability zone
        @type availability_zone: str
        @keyword metadata: Metadata
        @type metadata: dict
        @return: Created host aggregate
        @rtype: yakumo.nova.v2.aggregate.Resource
        """
        ret = super(Manager, self).create(
            name=name,
            availability_zone=availability_zone)
        if metadata:
            ret.set_metadata(**metadata)
        return ret
