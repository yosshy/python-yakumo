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
Resource class and its manager for images in Image V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils
from . import image_member


VISIBILITY_MAPPING = [
    (True, 'public'),
    (False, 'private'),
]

ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('file', 'file', mapper.Noop),
    ('disk_format', 'disk_format', mapper.Noop),
    ('container_format', 'container_format', mapper.Noop),
    ('size', 'size', mapper.Noop),
    ('virtual_size', 'virtual_size', mapper.Noop),
    ('checksum', 'checksum', mapper.Noop),
    ('min_ram', 'min_ram', mapper.Noop),
    ('min_disk', 'min_disk', mapper.Noop),
    ('owner', 'owner', mapper.Resource('keystone.user')),
    ('is_public', 'visibility', mapper.Simple(VISIBILITY_MAPPING)),
    ('is_protected', 'protected', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('tags', 'tags', mapper.Noop),
]


class Resource(base.GlanceV2Resource):
    """resource class for images on Image V2 API"""

    _stable_state = ['active', 'killed', 'deleted', 'deactivated']
    _sub_manager_list = {'members': image_member.Manager}

    def update(self, name=UNDEF, disk_format=UNDEF, container_format=UNDEF,
               size=UNDEF, virtual_size=UNDEF, checksum=UNDEF, min_ram=UNDEF,
               min_disk=UNDEF, owner=UNDEF, status=UNDEF, created_at=UNDEF,
               updated_at=UNDEF, is_public=UNDEF, protected=UNDEF,
               schema=UNDEF, tags=UNDEF, **kwargs):
        """
        Update properties of an image

        Non-standard key=value arguments are allowed (value must be a string).

        @keyword name: Image name
        @type name: str
        @keyword container_format: Container format
        ('ami','ari','aki','bare',or 'ovf')
        @type container_format: str
        @keyword disk_format: Disk format
        ('ami','ari','aki','vhd','vmdk','raw','qcow2', 'vdi',or 'iso')
        @type disk_format: str
        @keyword size: Image size in GB
        @type size: int
        @keyword virtual_size: virtual size in GB
        @type virtual_size: int
        @keyword checksum: Checksu
        @type checksum: str
        @keyword min_ram: Minimum size of RAM in MB
        @type min_ram: int
        @keyword min_disk: Minimum size of Disk in GB
        @type min_disk: int
        @keyword owner: User ID
        @type owner: str
        @keyword status: Image status
        @type status: str
        @keyword created_at: Created time
        @type created_at: str
        @keyword updated_at: Updated time
        @type updated_at: str
        @keyword is_public: Public flag
        @type is_public: bool
        @keyword is_protected: Protected flag
        @type is_protected: bool
        @keyword schema: Image schema
        @type schema: str
        @keyword tags: Image tags
        @type tags: [str]
        @keyword file: Image file path
        @type file: str
        @rtype: None
        """
        body = []
        attrs = dict(name=name, disk_format=disk_format,
                     container_format=container_format, size=size,
                     virtual_size=virtual_size, checksum=checksum,
                     min_ram=min_ram, min_disk=min_disk, owner=owner,
                     status=status, created_at=created_at,
                     updated_at=updated_at, is_public=is_public,
                     protected=protected, schema=schema, tags=tags)
        json_params = self._attr2json(attrs)
        json_params.update(kwargs)
        for k, v in json_params.items():
            if v is not None:
                body.append(dict(op='replace', path='/%s' % k, value=v))
        headers = {
            'Content-Type': 'application/openstack-images-v2.1-json-patch'}
        self._http.patch(self._url_resource_path, self._id,
                         data=body, headers=headers)
        self.reload()

    def upload(self, file=None):
        """
        Upload an image from a local file

        @keyword file: File name to save (required)
        @type file: str
        @rtype: None
        """
        self._http.put_raw(self._url_resource_path, self._id, 'file',
                           data=utils.gen_chunk(file))
        self.reload()

    def download(self, file=None):
        """
        Download an image into a local file

        @keyword file: File name to save (required)
        @type file: str
        @rtype: None
        """
        self._http.get_file(self._url_resource_path, self._id, 'file',
                            file=file)

    def activate(self):
        """
        Activate an image

        @rtype: None
        """
        self._http.post_raw(self._url_resource_path, self._id,
                            'actions/reactivate')
        self.reload()

    def deactivate(self):
        """
        Deactivate an image

        @rtype: None
        """
        self._http.post_raw(self._url_resource_path, self._id,
                            'actions/deactivate')
        self.reload()

    def add_tag(self, tag=None):
        """
        Tag an image

        @keyword tag: Tag (required)
        @type tag: str
        @rtype: None
        """
        self._http.put_raw(self._url_resource_path, self._id, 'tags', tag)
        self.reload()

    def remove_tag(self, tag=None):
        """
        Untag an image

        @keyword tag: Tag (required)
        @type tag: str
        @rtype: None
        """
        self._http.delete(self._url_resource_path, self._id, 'tags', tag)
        self.reload()


class Manager(base.GlanceV2Manager):
    """manager class for images on Image V2 API"""

    resource_class = Resource
    service_type = 'image'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'image'
    _json_resources_key = 'images'
    _url_resource_path = '/v2/images'

    def create(self, id=UNDEF, name=UNDEF, is_public=UNDEF, tags=UNDEF,
               container_format=UNDEF, disk_format=UNDEF, min_disk=UNDEF,
               min_ram=UNDEF, is_protected=UNDEF, file=None, **kwargs):
        """
        Register an image

        Non-standard key=value arguments are allowed (value must be a string).

        @keyword id: Image ID (optional)
        @type id: str
        @keyword name: Image name
        @type name: str
        @keyword is_public: Public flag
        @type is_public: bool
        @keyword tags: Tag list
        @type tags: [str]
        @keyword container_format: Container format
        ('ami','ari','aki','bare',or 'ovf')
        @type container_format: str
        @keyword disk_format: Disk format
        ('ami','ari','aki','vhd','vmdk','raw','qcow2', 'vdi',or 'iso')
        @type disk_format: str
        @keyword min_disk: Minimum disk size in GB
        @type min_disk: int
        @keyword min_ram: Minimum RAM size in MB
        @type min_ram: int
        @keyword is_protected: Protected flag
        @type is_protected: bool
        @keyword file: Image file path
        @type file: str
        @return: Created image
        @rtype: yakumo.glance.v2.image.Resource
        """
        obj = super(Manager, self).create(id=id, name=name,
                                          is_public=is_public,
                                          tags=tags,
                                          container_format=container_format,
                                          disk_format=disk_format,
                                          min_disk=min_disk,
                                          min_ram=min_ram,
                                          is_protected=is_protected,
                                          **kwargs)
        if file:
            obj.upload(file=file)
        return obj
