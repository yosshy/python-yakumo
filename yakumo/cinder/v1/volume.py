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
Resource class and its manager for volumes on Block Storage V1 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper

from yakumo.cinder.v1.snapshot import Resource as Snapshot
from yakumo.cinder.v1.volume_type import Resource as VolumeType
from yakumo.nova.v2.image import Resource as NovaV2Image
from yakumo.glance.v1.image import Resource as GlanceV1Image
from yakumo.glance.v2.image import Resource as GlanceV2Image


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'display_name', mapper.Noop),
    ('description', 'display_description', mapper.Noop),
    ('availability_zone', 'availability_zone', mapper.Noop),
    ('size', 'size', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('attachments', 'attachments', mapper.Noop),
    ('volume_type', 'volume_type',
     mapper.Resource('cinder.volume_type')),
    ('source_image', 'imageRef', mapper.Resource('image')),
    ('source_snapshot', 'snapshot_id',
     mapper.Resource('cinder.volume_snapshot')),
    ('source_volume', 'source_volid',
     mapper.Resource('cinder.volume')),
    ('is_bootable', 'bootable', mapper.BoolStr),
    ('is_encrypted', 'encrypted', mapper.Noop),
    ('is_multiattach', 'multiattach', mapper.Noop),
    ('project', 'os-vol-tenant-attr:tenant_id',
     mapper.Resource('project')),
    ('driver_data', 'os-volume-replication:driver_data', mapper.Noop),
    ('extended_status', 'os-volume-replication:extended_status',
     mapper.Noop),
    ('host', 'os-vol-host-attr:hos', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
]


class Resource(base.Resource):
    """resource class for volumes on Block Storage V1 API"""

    _stable_state = ['available', 'in-use', 'error', 'error_deleting']

    def get_metadata(self):
        """
        Get metadata of a volume

        @return: Metadata
        @rtype: dict
        """
        ret = self._http.get(self._url_resource_path, self._id, 'metadata')
        return ret.get('metadata')

    def set_metadata(self, **metadata):
        """
        Update metadata of a volume

        @keyword metadata: key=value style.
        @type metadata: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'metadata',
                        data={'metadata': metadata})
        self.reload()

    def unset_metadata(self, *keys):
        """
        Delete metadata of a volume

        @param key: key of the metadata
        @type keys: [str]
        @rtype: None
        """
        for key in keys:
            self._http.delete(self._url_resource_path, self._id,
                              'metadata', key)
        self.reload()


class Manager(base.Manager):
    """manager class for roles on Block Storage V1 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'volume'
    _json_resources_key = 'volumes'
    _hidden_methods = ["update"]
    _url_resource_list_path = '/volumes/detail'
    _url_resource_path = '/volumes'

    def _attr2json(self, attrs):
        volume_type = attrs.get('volume_type')
        if isinstance(volume_type, VolumeType):
            attrs['volume_type'] = volume_type.name
        return super(Manager, self)._attr2json(attrs)

    def _json2attr(self, json_params):
        ret = super(Manager, self)._json2attr(json_params)
        image = json_params.get('volume_image_metadata', {}).get('image_id')
        if image:
            ret['source_image'] = self._client.image.get_empty(image)
        volume_type = json_params.get('volume_type')
        if volume_type:
            ret['volume_type'] = self._client.volume_type.find_one(
                name=volume_type)
        return ret

    def create(self, name=UNDEF, description=UNDEF, size=UNDEF, project=UNDEF,
               availability_zone=UNDEF, source=UNDEF, volume_type=UNDEF,
               metadata=UNDEF):
        """
        Create a volume

        @keyword name: Volume name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword size: Size in GB
        @type size: int
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword availability_zone: Availability zone
        @type availability_zone: yakumo.availability_zone.Resource
        @keyword source: Source image/snapshot/volume (optional)
        @type source: one of yakumo.image.Resource,
        yakumo.volume_snapshot.Resource and yakumo.volume.Resource
        @keyword volume_type: Volume type
        @type volume_type: yakumo.cinder.v1.volume_type.Resource
        @keyword metadata: Metadata (key=value)
        @type metadata: dict
        @return: Created volume
        @type: yakumo.cinder.v1.volume.Resource
        """

        source_image = None
        source_volume = None
        source_snapshot = None
        if isinstance(source, Resource):
            source_volume = source
        elif isinstance(source, Snapshot):
            source_snapshot = source
        elif isinstance(source, (GlanceV1Image, GlanceV2Image, NovaV2Image)):
            source_image = source
        return super(Manager, self).create(project=project,
                                           availability_zone=availability_zone,
                                           size=size, name=name,
                                           description=description,
                                           source_volume=source_volume,
                                           source_snapshot=source_snapshot,
                                           source_image=source_image,
                                           volume_type=volume_type,
                                           metadata=metadata)
