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
Resource class and its manager for containers on Object Storage V1 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from . import file_object
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('name', 'name', mapper.Noop),
    ('object_count', 'x-container-object-count', mapper.IntStr),
    ('used_bytes', 'x-container-bytes-used', mapper.IntStr),
    ('temp_url_key', 'x-container-meta-temp-url-key', mapper.Noop),
    ('temp_url_key2', 'x-container-meta-temp-url-key-2', mapper.Noop),
    ('quota_count', 'x-container-meta-quota-count', mapper.IntStr),
    ('quota_bytes', 'x-container-meta-quota-bytes', mapper.IntStr),
    ('storage_policy', 'x-storage-policy', mapper.Noop),
    ('read_acl', 'x-container-read', mapper.Noop),
    ('write_acl', 'x-container-write', mapper.Noop),
    ('acl_allow_origin', 'x-container-meta-access-control-allow-origin',
     mapper.Noop),
    ('acl_max_age', 'x-container-meta-access-control-max-age', mapper.IntStr),
    ('acl_expose_headers', 'x-container-meta-access-control-expose-headers',
     mapper.Noop),
    ('sync_key', 'x-container-sync-key', mapper.Noop),
    ('sync_to', 'x-container-sync-to', mapper.Noop),
    ('versions', 'x-versions-location', mapper.Noop),
    ('history', 'x-history-location', mapper.Noop),
    ('timestamp', 'x-timestamp', mapper.FloatStr),
    ('trans_id', 'x-trans-id', mapper.Noop),
    ('trans_id_extra', 'x-trans-id-extra', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
]


class Resource(base.SwiftV1Resource):
    """resource class for containers on Object Storage V1 API"""

    _sub_manager_list = {
        'object': file_object.Manager
    }

    def update(self, read_acl=UNDEF, write_acl=UNDEF,
               sync_to=UNDEF, sync_key=UNDEF,
               versions_location=UNDEF, history_location=UNDEF,
               ac_allow_origin=UNDEF, ac_max_age=UNDEF,
               quota_bytes=UNDEF, quota_count=UNDEF,
               temp_url_key=UNDEF, temp_url_key2=UNDEF,
               trans_id_extra=UNDEF, storage_policy=UNDEF):
        """
        Update a container

        @keyword read_acl: The ACL that grants read access
        @type read_acl: str
        @keyword write_acl: The ACL that grants write access
        @type write_acl: str
        @keyword sync_to: The destination for container synchronization
        @type sync_to: str
        @keyword sync_key: The secret key for container synchronization
        @type sync_key: str
        @keyword versions_location: The URL-encoded UTF-8 representation of
        the container that stores previous versions of objects
        @type versions_location: str
        @keyword history_location: The URL-encoded UTF-8 representation of
        the container that stores previous versions of objects
        @type history_location: str
        @keyword ac_allow_origin: Originating URLs allowed to make cross-origin
        requests (CORS), separated by spaces.
        @type ac_allow_origin: str
        @keyword ac_max_age: Maximum time for the origin to hold the preflight
        results
        @type ac_max_age:
        @keyword quota_bytes: The maximum size of the container, in bytes
        @type quota_bytes: int
        @keyword quota_count: The maximum object count of the container
        @type qouta_count: int
        @keyword temp_url_key: The secret key value for temporary URLs
        @type temp_url_key: str
        @keyword temp_url_key2: The 2nd secret key value for temporary URLs
        @type temp_url_key2: str
        @keyword trans_id_extra: Extra transaction information
        @type trans_id_extra: str
        @keyword storage_policy: Name of the storage policy
        @type storage_policy: str
        @return: Created container
        @rtype: yakumo.swift.v1.container.Resource
        """
        super(Resource, self).update(
            read_acl=read_acl,
            write_acl=write_acl,
            sync_to=sync_to,
            sync_key=sync_key,
            versions_location=versions_location,
            history_location=history_location,
            ac_allow_origin=ac_allow_origin,
            ac_max_age=ac_max_age,
            quota_bytes=quota_bytes,
            quota_count=quota_count,
            temp_url_key=temp_url_key,
            temp_url_key2=temp_url_key2,
            trans_id_extra=trans_id_extra,
            storage_policy=storage_policy)

    def set_metadata(self, **metadata):
        """
        Update metadata of a volume

        @keyword metadata: Key=value style metadata
        @type metadata: dict
        @rtype: None
        """
        headers = {}
        for key, value in metadata.items():
            x_key = "x-container-meta-" + key
            headers[x_key] = str(value)
        self._http.post_raw(self._url_resource_path, self._id, headers=headers)
        self.reload()

    def unset_metadata(self, *keys):
        """
        Delete metadata of a volume

        @param key: Key of the metadata
        @type keys: [str]
        @rtype: None
        """
        headers = {}
        for key in keys:
            x_key = "x-remove-container-meta-" + key
            headers[x_key] = "x"
        self._http.post_raw(self._url_resource_path, self._id, headers=headers)
        self.reload()


class Manager(base.SwiftV1Manager):
    """manager class for containers on Object Storage V1 API"""

    resource_class = Resource
    service_type = 'object-store'
    _attr_mapping = ATTRIBUTE_MAPPING
    _has_detail = False
    _url_resource_path = None
    _json_resource_key = 'container'

    def create(self, name, read_acl=UNDEF, write_acl=UNDEF,
               sync_to=UNDEF, sync_key=UNDEF,
               versions_location=UNDEF, history_location=UNDEF,
               ac_allow_origin=UNDEF, ac_max_age=UNDEF,
               quota_bytes=UNDEF, quota_count=UNDEF,
               temp_url_key=UNDEF, temp_url_key2=UNDEF,
               trans_id_extra=UNDEF, storage_policy=UNDEF, metadata=UNDEF):
        """
        Create a volume

        @param name: Container name
        @type name: str
        @keyword read_acl: The ACL that grants read access
        @type read_acl: str
        @keyword write_acl: The ACL that grants write access
        @type write_acl: str
        @keyword sync_to: The destination for container synchronization
        @type sync_to: str
        @keyword sync_key: The secret key for container synchronization
        @type sync_key: str
        @keyword versions_location: The URL-encoded UTF-8 representation
        @type history_location: str
        @keyword ac_allow_origin: Originating URLs allowed to make cross-origin
        requests (CORS), separated by spaces.
        @type ac_allow_origin: int
        @keyword ac_max_age: Maximum time for the origin to hold the preflight
        results
        @type ac_max_age: int
        @keyword quota_bytes: The maximum size of the container, in bytes
        @type quota_bytes: int
        @keyword quota_count: The maximum object count of the container
        @type qouta_count: int
        @keyword temp_url_key: The secret key value for temporary URLs
        @type temp_url_key: str
        @keyword temp_url_key2: The 2nd secret key value for temporary URLs
        @type temp_url_key2: str
        @keyword trans_id_extra: Extra transaction information
        @type trans_id_extra: str
        @keyword storage_policy: Name of the storage policy
        @type storage_policy: str
        @keyword metadata: Key-value style metadata
        @type metadata: dict
        @return: Created container
        @rtype: yakumo.swift.v1.container.Resource
        """
        return super(Manager, self).create(
            name,
            read_acl=read_acl,
            write_acl=write_acl,
            sync_to=sync_to,
            sync_key=sync_key,
            versions_location=versions_location,
            history_location=history_location,
            ac_allow_origin=ac_allow_origin,
            ac_max_age=ac_max_age,
            quota_bytes=quota_bytes,
            quota_count=quota_count,
            temp_url_key=temp_url_key,
            temp_url_key2=temp_url_key2,
            trans_id_extra=trans_id_extra,
            storage_policy=storage_policy,
            metadata=metadata)
