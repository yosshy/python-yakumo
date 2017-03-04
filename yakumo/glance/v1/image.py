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
Resource class and its manager for images in Image V1 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('disk_format', 'disk_format', mapper.Noop),
    ('container_format', 'container_format', mapper.Noop),
    ('size', 'size', mapper.Noop),
    ('virtual_size', 'virtual_size', mapper.Noop),
    ('checksum', 'checksum', mapper.Noop),
    ('min_ram', 'min_ram', mapper.Noop),
    ('min_disk', 'min_disk', mapper.Noop),
    ('owner', 'owner', mapper.Noop),
    ('properties', 'properties', mapper.Noop),
    ('is_public', 'is_public', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('deleted_at', 'deleted_at', mapper.DateTime),
    ('is_deleted', 'deleted', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for images on Image V1 API"""

    _stable_state = ['active', 'killed', 'deleted', 'deactivated']

    def update(self, name=UNDEF, uri=UNDEF, disk_format=UNDEF,
               container_format=UNDEF, size=UNDEF, virtual_size=UNDEF,
               checksum=UNDEF, min_ram=UNDEF, min_disk=UNDEF, owner=UNDEF,
               properties=UNDEF, is_public=UNDEF, file=None):
        """
        Update properties of an image

        @keyword name: Image name
        @type name: str
        @keyword uri: URI to the Image
        @type uri: str
        @keyword disk_format: Disk format
        @type disk_format: str
        @keyword container_format: Container format
        @type container_format: str
        @keyword size: Actual file size
        @type size: int
        @keyword virtual_size: Virtual disk size
        @type virtual_size: int
        @keyword checksum: Checksum
        @type checksum: str
        @keyword min_ram: Minimum RAM size of the VM with the image
        @type min_ram: int
        @keyword owner: Owner of the image
        @type owner: str
        @keyword properties: Properties
        @type properties: dict
        @keyword is_public: Whether this is public or not
        @type is_public: bool
        @keyword file: File to upload
        @type file: str
        @rtype: None
        """

        attrs = dict(name=name, uri=uri, disk_format=disk_format,
                     container_format=container_format, size=size,
                     virtual_size=virtual_size, checksum=checksum,
                     min_ram=min_ram, min_disk=min_disk, owner=owner,
                     properties=properties, is_public=is_public)
        json_params = self._attr2json(attrs)
        headers = {}
        for key, value in json_params.items():
            headers['x-image-meta-%s' % key] = value

        if file:
            headers['x-image-meta-size'] = os.path.getsize(file)
            self._http.put_raw(self._url_resource_path, self._id,
                               headers=headers,
                               data=gen_chunk(file))
        elif uri:
            headers['x-image-meta-uri'] = uri
            self._http.put_raw(self._url_resource_path, self._id,
                               headers=headers)
        else:
            self._http.put_raw(self._url_resource_path, self._id,
                               headers=headers)
        self.reload()

    def download(self, file=None):
        """
        Download an image into a local file

        @keyword file: File name to save (required)
        @type file: str
        @rtype: None
        """
        try:
            self._http.get_file(self._url_resource_path, self._id, file=file)
        except:
            pass


class Manager(base.Manager):
    """manager class for images on Image V1 API"""

    resource_class = Resource
    service_type = 'image'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'image'
    _json_resources_key = 'images'
    _url_resource_list_path = '/v1/images/detail'
    _url_resource_path = '/v1/images'

    def create(self, name=UNDEF, uri=UNDEF, disk_format=UNDEF,
               container_format=UNDEF, size=UNDEF, virtual_size=UNDEF,
               checksum=UNDEF, min_ram=UNDEF, min_disk=UNDEF, owner=UNDEF,
               properties=UNDEF, is_public=UNDEF, file=None):
        """
        Register an image

        @keyword name: Image name
        @type name: str
        @keyword uri: URL to an image
        @type uri: str
        @keyword disk_format: Disk format (raw, qcow2, vmdk, ...)
        @type disk_format: str
        @keyword container_format: Container format (bare, vmdk, ...)
        @type container_format: str
        @keyword size: Image file size in GB
        @type size: int
        @keyword virtual_size: Virtual disk size in GB
        @type virtual_size: int
        @keyword checksum: Image checksum
        @type checksum: str
        @keyword min_ram: Minimum RAM size required for VMs in MB
        @type min_ram: int
        @keyword min_disk: Minimum disk size required for VMs in GB
        @type min_disk: int
        @keyword owner: Image owner
        @type owner: str
        @keyword properties: Image properties
        @type properties: dict
        @keyword is_public: Whether the image is public or not
        @type is_public: bool
        @keyword file: Filename to upload
        @type file: str
        @return: Created image
        @rtype: yakumo.glance.v1.image.Resource
        """
        attrs = dict(name=name, uri=uri, disk_format=disk_format,
                     container_format=container_format, size=size,
                     virtual_size=virtual_size, checksum=checksum,
                     min_ram=min_ram, min_disk=min_disk, owner=owner,
                     properties=properties, is_public=is_public)
        json_params = self._attr2json(attrs)
        headers = {}
        for key, value in json_params.items():
            headers['x-image-meta-%s' % key] = value

        if file:
            headers['x-image-meta-size'] = os.path.getsize(file)
            ret = self._http.post_raw(self._url_resource_path, headers=headers,
                                      data=utils.gen_chunk(file))
        elif uri:
            headers['x-image-meta-uri'] = uri
            ret = self._http.post_raw(self._url_resource_path, headers=headers)
        else:
            ret = self._http.post_raw(self._url_resource_path, headers=headers)

        return self.get_empty(
            ret[self._json_resource_key][self._id_attr])

    def get(self, id):
        """
        Get an image

        @param id: Image UUID
        @type id: str
        @return: Image
        @rtype: yakumo.glance.v1.image.Resource
        """
        try:
            ret = self._http.head(self._url_resource_path, id)
            json_params = {}
            for json_param in self._to_attr_mapping.keys():
                h = 'x-image-meta-%s' % json_param
                if h in ret:
                    json_params[json_param] = ret[h]
            attrs = self._json2attr(json_params)
            return self.resource_class(self, **attrs)
        except:
            raise
            return None
