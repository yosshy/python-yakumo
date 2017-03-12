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
Resource class and its manager for objects on Object Storage V1 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('name', 'name', mapper.Noop),
    ('content_disposition', 'content-disposition', mapper.Noop),
    ('content_encoding', 'content-encoding', mapper.Noop),
    ('content_type', 'content-type', mapper.Noop),
    ('delete_at', 'x-delete-at', mapper.DateTime),
    ('delete_after', 'x-delete-after', mapper.IntStr),
    ('etag', 'etag', mapper.Noop),
    ('if_none_match', 'if-none-match', mapper.Noop),
    ('modified_at', 'last-modified', mapper.DateTime),
    ('object_count', 'x-container-object-count', mapper.IntStr),
    ('object_manifest', 'x-object-manifest', mapper.Noop),
    ('size', 'content-length', mapper.IntStr),
    ('static_large_object', 'x-static-large-object', mapper.Noop),
    ('timestamp', 'x-timestamp', mapper.FloatStr),
    ('trans_id', 'x-trans-id', mapper.Noop),
    ('trans_id_extra', 'x-trans-id-extra', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
    ('data', 'data', mapper.Noop),
]


class Resource(base.SwiftV1Resource):
    """resource class for containers on Object Storage V1 API"""

    def update(self, content_disposition=UNDEF, content_encoding=UNDEF,
               content_type=UNDEF, delete_after=UNDEF, delete_at=UNDEF,
               trans_id_extra=UNDEF, metadata=UNDEF):
        """
        Update metadata of an object

        @keyword content_disposition: Specifies the override behavior for the
        browser
        @type content_disposition: str
        @keyword content_encoding: Content-Encoding metadata
        @type content_encoding: str
        @keyword content_type: MIME type for the object
        @type content_type: str
        @keyword delete_after: Seconds after which the system removes the
        object
        @type delete_after: int
        @keyword delete_at: When the system removes the object
        @type delete_at: datetime.datetime
        @keyword trans_id_extra: Extra transaction information
        @type trans_id_extra: str
        @keyword metadata: Key-value style metadata
        @type metadata: dict
        @rtype: None
        """
        super(Resource, self).update(
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_type=content_type,
            delete_at=delete_at,
            delete_after=delete_after,
            trans_id_extra=trans_id_extra,
            metadata=metadata)

    def replace(self, content_disposition=UNDEF, content_encoding=UNDEF,
                content_type=UNDEF, etag=UNDEF, if_none_match=UNDEF,
                delete_after=UNDEF, delete_at=UNDEF, object_manifest=UNDEF,
                size=UNDEF, trans_id_extra=UNDEF, metadata=UNDEF, file=None):
        """
        Replace an object

        @keyword content_disposition: Specifies the override behavior for the
        browser
        @type content_disposition: str
        @keyword content_encoding: Content-Encoding metadata
        @type content_encoding: str
        @keyword content_type: MIME type for the object
        @type content_type: str
        @keyword etag: MD5 checksum of the object
        @type etag: str
        @keyword if_none_match: If-None-Match header
        @type if_none_match: str
        @keyword delete_after: When the system removes the object
        @type delete_after: datetime.datetime
        @keyword delete_at: When the system removes the object
        @type delete_at: datetime.datetime
        @keyword object_manifest: Dynamic large object manifest object
        @type object_manifest: str
        @keyword size: Object size
        @type size: int
        @keyword trans_id_extra: Extra transaction information
        @type trans_id_extra: str
        @keyword metadata: Key-value style metadata
        @type metadata: dict
        @keyword file: File name to upload
        @type file: str
        @rtype: None
        """
        old_attrs = self.get_attrs()
        new_attrs = dict(
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_type=content_type,
            object_manifest=object_manifest,
            delete_after=delete_after,
            delete_at=delete_at,
            etag=etag,
            if_none_match=if_none_match,
            size=size,
            trans_id_extra=trans_id_extra,
            metadata=metadata)
        for key, value in new_attrs.items():
            if value is UNDEF:
                continue
            new_attrs[key] = old_attrs[key]

        self._manager.create(self._id, file=file, **new_attrs)
        self.reload()

    def copy(self, container=UNDEF, name=UNDEF):
        """
        Copy an object

        @param container: Destination container
        @type container: swift.container.Resource
        @param name: Destination object name
        @type name: str
        @return: New object
        @rtype: swift.v1.file_object.Resource
        """
        if container is UNDEF:
            container = self._manager.parent_resource
        headers = {
            "x-copy-from": "/%s/%s" % (
                self._manager.parent_resource.get_id(), self._id),
        }
        self._http.put_raw(container._manager._url_resource_path,
                           container.get_id(), name,
                           headers=headers)
        return container.object.get_empty(name)

    def download(self, file=None):
        """
        Download an object into a file

        @keyword file: File name to save
        @type file: str
        @rtype: None
        """
        self._http.get_file(self._url_resource_path, self._id, file=file)

    def set_metadata(self, **metadata):
        """
        Update metadata of an object

        @keyword metadata: key=value style.
        @type metadata: dict
        @rtype: None
        """
        if self.metadata is None:
            self.metadata = {}
        self.metadata.update(metadata)
        self.update()

    def unset_metadata(self, *keys):
        """
        Delete metadata of an object

        @param key: key of the metadata
        @type keys: [str]
        @rtype: None
        """
        if self.metadata is None:
            return
        for key in keys:
            if key in self.metadata:
                self.metadata.pop(key)
        self.update()


class Manager(base.SwiftV1SubManager):
    """manager class for objects on Object Storage V1 API"""

    resource_class = Resource
    service_type = 'object-store'
    _attr_mapping = ATTRIBUTE_MAPPING
    _has_detail = False
    _url_resource_path = '/%s'
    _json_resource_key = 'object'

    def create(self, name, content_disposition=UNDEF, content_encoding=UNDEF,
               content_type=UNDEF, etag=UNDEF, if_none_match=UNDEF,
               delete_after=UNDEF, delete_at=UNDEF, object_manifest=UNDEF,
               size=UNDEF, trans_id_extra=UNDEF, metadata=UNDEF, file=None):
        """
        Create an object

        @param name: Object name
        @type name: str
        @keyword content_disposition: Specifies the override behavior for the
        browser
        @type content_disposition: str
        @keyword content_encoding: Content-Encoding metadata
        @type content_encoding: str
        @keyword content_type: MIME type for the object
        @type content_type: str
        @keyword etag: MD5 checksum of the object
        @type etag: str
        @keyword if_none_match: If-None-Match header
        @type if_none_match: str
        @keyword delete_after: When the system removes the object
        @type delete_after: datetime.datetime
        @keyword delete_at: When the system removes the object
        @type delete_at: datetime.datetime
        @keyword object_manifest: Dynamic large object manifest object
        @type object_manifest: str
        @keyword size: Object size
        @type size: int
        @keyword trans_id_extra: Extra transaction information
        @type trans_id_extra: str
        @keyword metadata: Key-value style metadata
        @type metadata: dict
        @keyword file: File name to upload
        @type file: str
        @return: Created objects
        @rtype: yakumo.swift.v1.objects.Resource
        """
        data = UNDEF
        if file:
            data = utils.gen_chunk(file)
        return super(Manager, self).create(
            name,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            content_type=content_type,
            object_manifest=object_manifest,
            delete_after=delete_after,
            delete_at=delete_at,
            etag=etag,
            if_none_match=if_none_match,
            size=size,
            trans_id_extra=trans_id_extra,
            metadata=metadata,
            data=data)
