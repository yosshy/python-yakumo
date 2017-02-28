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
Resource class and its manager for images in Compute API v2
"""

from yakumo import base
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('size', 'OS-EXT-IMG-SIZE:size', mapper.Noop),
    ('min_ram', 'minRam', mapper.Noop),
    ('min_disk', 'minDisk', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('created_at', 'created', mapper.Noop),
    ('updated_at', 'updated', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for images in Compute API v2"""

    def get_metadata(self):
        """Get extra specs for a flavor

        @return: Metadata
        @rtype: dir
        """
        ret = self._http.get(self._url_resource_path, self._id, 'metadata')
        return ret.get('metadata', {})

    def set_metadata(self, **metadata):
        """
        Create metadata for a image

        @keyword metadata: Metadata with key=value
        @type metadata: dict
        @rtype: None
        """
        metadata = {k: str(v) for k, v in metadata.items()}
        self._http.post(self._url_resource_path, self._id, 'metadata',
                        data=dict(metadata=metadata))
        self.reload()

    def unset_metadata(self, *keys):
        """
        Delete one metadata from an image

        @param keys: keys of metadata to remove
        @type keys: [str]
        @rtype: None
        """
        for key in keys:
            self._http.delete(self._url_resource_path, self._id, 'metadata',
                              key)
        self.reload()


class Manager(base.Manager):
    """Manager class for images in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "update"]
    _json_resource_key = 'image'
    _json_resources_key = 'images'
    _url_resource_path = '/images'
    _url_resource_list_path = '/images/detail'
