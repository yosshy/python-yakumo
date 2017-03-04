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
Resource class and its manager for volumes on Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils

from yakumo.cinder.v2.snapshot import Resource as Snapshot
from yakumo.cinder.v2.volume_type import Resource as VolumeType
from yakumo.nova.v2.image import Resource as NovaV2Image
from yakumo.glance.v1.image import Resource as GlanceV1Image
from yakumo.glance.v2.image import Resource as GlanceV2Image


ATTRIBUTE_MAPPING = [
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('volume_type', 'volume_type', mapper.Noop),
    ('size', 'size', mapper.Noop),
    ('availability_zone', 'availability_zone',
     mapper.Resource('availability_zone')),
    ('source_image', 'imageRef', mapper.Resource('image')),
    ('source_volume', 'source_volid', mapper.Resource('cinder.volume')),
    ('source_snapshot', 'snapshot_id',
     mapper.Resource('cinder.volume_snapshot')),
    ('source_replica', 'source_replica', mapper.Noop),
    ('consistencygroup', 'consistencygroup_id',
     mapper.Resource('cinder.consistency_group')),
    ('scheduler_hints', 'scheduler_hints', mapper.Noop),
    ('metadata', 'metadata', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('project', 'os-vol-tenant-attr:tenant_id', mapper.Resource('project')),
    ('is_multiattach', 'multiattach', mapper.Noop),
    ('id', 'id', mapper.Noop),
    ('attachments', 'attachments', mapper.Noop),
    ('attachment', 'attachment', mapper.Resource('volume_attachment')),
    ('host', 'host', mapper.Noop),
    ('host', 'os-vol-host-attr:host', mapper.Noop),
    ('volume_replication_driver', 'os-volume-replication:driver_data',
     mapper.DateTime),
    ('replication_status', 'replication_status', mapper.Noop),
    ('extended_replication_status', 'os-volume-replication:extended_status',
     mapper.Noop),
    ('migration_status', 'migration_status', mapper.Noop),
    ('backend_volume_id', 'os-vol-mig-status-attr:name_id', mapper.Noop),
    ('user', 'user_id', mapper.Resource('user')),
    ('status', 'status', mapper.Noop),
    ('is_bootable', 'bootable', mapper.BoolStr),
    ('is_encrypted', 'encrypted', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
]


class Resource(base.Resource):
    """resource class for volumes on Block Storage V2 API"""

    _stable_state = ['available', 'in-use', 'error', 'error_deleting']

    def update(self, name=UNDEF, description=UNDEF, metadata=UNDEF):
        """
        Update properties of a volume

        @keyword name: Volume name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword metadata: Metadata (key=value)
        @type metadata: dict
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            metadata=metadata)

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

    def extend(self, size=None):
        """
        Extend a volume

        @keyword size: new size; should be larger than the current size
        @type size: int
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-extend", new_size=size))

    def reset_status(self, status=None, attach_status=None,
                     migration_status=None):
        """
        Reset status of a volume

        @keyword status: new status
        @type status: str
        @keyword attach_status: new attach status
        @type status: str
        @keyword migration_status: new migration status
        @type migration_status: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "os-reset_status",
                            status=status,
                            attach_status=attach_status,
                            migration_status=migration_status))

    def set_image_metadata(self, metadata=None):
        """
        Set image metadata

        @keyword metadata: new metadata
        @type metadata: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-set_image_metadata",
                                                 metadata=metadata))

    def delete_image_metadata(self, key=None):
        """
        Set image metadata

        @keyword key: key to delete
        @type key: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-unset_image_metadata",
                                                 key=key))

    def unmanage(self):
        """
        Unmanage a volume

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-unmanage"))

    def force_detach(self, attachment=None, connector=None):
        """
        Force detach a volume

        @keyword attachment: Volume attachment
        @type attachment: yakumo.server.volume_attachment.Resource
        @keyword connector: Connector information
        @type connector: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "os-force_detach",
                            attachment=attachment,
                            connector=connector))

    def upload(self, name=None, disk_format='raw', force=False):
        """
        Upload volume image to Glance

        @keyword name: Image name
        @type name: str
        @keyword disk_format: Disk format (default: 'raw')
        @type disk_format: str
        @keyword force: Force creation
        @type force: bool
        """
        ret = self._http.post(self._url_resource_path, self._id, 'action',
                              data=utils.get_json_body(
                                  "os-volume_upload_image",
                                  image_name=name,
                                  disk_format=disk_format,
                                  force=force))
        image_id = ret.get('os-volume_upload_image', {}).get('image_id')
        return self._client.image.get_empty(image_id)


class Manager(base.Manager):
    """manager class for volumes on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'volume'
    _json_resources_key = 'volumes'
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

    def create(self, name=UNDEF, description=UNDEF, volume_type=UNDEF,
               size=UNDEF, availability_zone=UNDEF, source=UNDEF,
               is_replication=UNDEF, consistency_group=UNDEF,
               scheduler_hints=UNDEF, metadata=UNDEF,
               project=UNDEF, is_multiattach=UNDEF):
        """
        Create a volume

        @keyword name: Volume name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword volume_type: Volume type
        @type volume_type: yakumo.cinder.v2.volume_type.Resource
        @keyword size: Size in GB
        @type size: int
        @keyword availability_zone: Availability zone
        @type availability_zone: yakumo.availability_zone.Resource
        @keyword source: Source image/snapshot/volume (optional)
        @type source: one of yakumo.image.Resource,
        yakumo.volume_snapshot.Resource and yakumo.volume.Resource
        @keyword is_replication: Whether the volume is a replica of another
        volume
        @type source: bool
        @keyword consistency_group: Consistency group (optional)
        @type consistency_group: yakumo.cinder.v2.consistency_group.Resource
        @keyword scheduler_hints: Scheduler hints (optional)
        @type scheduler_hints: dict
        @keyword metadata: Metadata (key=value)
        @type metadata: dict
        @keyword is_multiattach: Whether multiattach is allowed
        @type is_multiattach: bool
        @return: Created volume
        @rtype: yakumo.cinder.v2.volume.Resource
        """
        source_image = UNDEF
        source_volume = UNDEF
        source_snapshot = UNDEF
        source_replica = UNDEF
        if isinstance(source, Resource):
            if is_replication is not UNDEF:
                source_replica = source
            else:
                source_volume = source
        elif isinstance(source, Snapshot):
            source_snapshot = source
        elif isinstance(source, (GlanceV1Image, GlanceV2Image, NovaV2Image)):
            source_image = source
        return super(Manager, self).create(
            name=name,
            description=description,
            volume_type=volume_type,
            size=size,
            availability_zone=availability_zone,
            source_image=source_image,
            source_volume=source_volume,
            source_snapshot=source_snapshot,
            source_replica=source_replica,
            consistency_group=consistency_group,
            scheduler_hints=scheduler_hints,
            metadata=metadata,
            is_multiattach=is_multiattach)

    def manage(self, name=UNDEF, description=UNDEF, volume_type=UNDEF,
               size=UNDEF, availability_zone=UNDEF, metadata=UNDEF,
               ref=UNDEF, project=UNDEF, is_bootable=UNDEF):
        """
        Manage a volume

        @keyword name: Volume name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword volume_type: Volume type
        @type volume_type: yakumo.cinder.v2.volume_type.Resource
        @keyword size: Size in GB
        @type size: int
        @keyword availability_zone: Availability zone
        @type availability_zone: yakumo.availability_zone.Resource
        @keyword metadata: Metadata (key=value)
        @type metadata: dict
        @keyword host: Reference for volume host
        @type host: str
        @keyword ref: Reference for existing volume (key=value)
        @type ref: dict
        @keyword is_bootable: Whether volume is bootable
        @type is_bootable: bool
        @return: Created volume
        @rtype: yakumo.cinder.v2.volume.Resource
        """
        json_attr = self._attr2json(dict(
            name=name,
            description=description,
            volume_type=volume_type,
            size=size,
            availability_zone=availability_zone,
            metadata=metadata,
            host=host,
            ref=ref,
            is_bootable=is_bootable))
        ret = self._http.post(self._url_resource_path, 'os-volume-manage',
                              data=utils.get_json_body("volume", **json_attr))
        attrs = self._json2attr(ret)
        return self.get_empty(attrs[self._id_attr])
