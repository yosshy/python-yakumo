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
Resource class and its manager for volume backup on Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from . import volume_transfer


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'display_name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('availability_zone', 'availability_zone',
     mapper.Resource('availability_zone')),
    ('source_volume', 'volume_id', mapper.Resource('cinder.volume')),
    ('size', 'size', mapper.Noop),
    ('object_count', 'object_count', mapper.Noop),
    ('container', 'container', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('status', 'status', mapper.Noop),
    ('fail_reason', 'fail_reason', mapper.Noop),
    ('has_dependent_backups', 'has_dependent_backups', mapper.Noop),
    ('is_incremental', 'incremental', mapper.Noop),
    ('is_incremental', 'is_incremental', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for volume backups on Block Storage V2 API"""

    _stable_state = ['available', 'error', 'error_deleting']

    def restore(self, volume=None, transfer=None):
        """
        Restore a volume from a volume backup

        @keyword volume: Destination volume
        @type volume: yakumo.cinder.v2.volume.Resource
        @keyword transfer: Volume transfer
        @type transfer: yakumo.cinder.v2.volume_transfer.Resource
        @rtype: None
        """
        transfer_name = None
        if isinstance(transfer, volume_transfer.Resource):
            transfer_name = transfer.name
        self._http.post(self._url_resource_path, self._id, 'restore',
                        data=utils.get_json_body("restore",
                                                 volume=volume.get_id(),
                                                 name=transfer_name))

    def delete(self, force=False):
        """
        Delete a volume backup

        @keyword force: Whether the deletion is forced
        @type force: bool
        @rtype: None
        """
        if not force:
            super(Resource. self).delete()
            return

        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-force_delete"))


class Manager(base.Manager):
    """manager class for volume backups on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'backup'
    _json_resources_key = 'backups'
    _hidden_methods = ["update"]
    _url_resource_list_path = '/backups/detail'
    _url_resource_path = '/backups'

    def create(self, name=UNDEF, description=UNDEF, source_volume=UNDEF,
               container=UNDEF, is_incremental=UNDEF):
        """
        Create a backup of a volume

        @keyword name: Snapshot name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword source_volume: Source volume
        @type source_volume: yakumo.cinder.v2.volume.Resource
        @keyword container: Container for store a volume backup
        @type source_volume: str
        @keyword is_incremental: Whether the backup is incremental
        @type is_incremental: bool
        @return: Created volume object
        @rtype: yakumo.cinder.v2.snapshot.Resource
        """
        return super(Manager, self).create(name=name,
                                           description=description,
                                           source_volume=source_volume,
                                           container=container,
                                           is_incremental=is_incremental)
