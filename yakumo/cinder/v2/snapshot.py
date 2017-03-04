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
Resource class and its manager for volume snapshots on Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('size', 'size', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('force', 'force', mapper.Noop),
    ('source', 'volume_id', mapper.Resource('cinder.volume')),
    ('progress', 'os-extended-snapshot-attributes:progress', mapper.Noop),
    ('project', 'os-extended-snapshot-attributes:project_id',
     mapper.Resource('project')),
    ('metadata', 'metadata', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
]


class Resource(base.Resource):
    """resource class for volume snapshots on Block Storage V2 API"""

    _stable_state = ['available', 'error', 'error_deleting']

    def get_metadata(self):
        """
        Get metadata of a volume snapshot

        @return: Metadata
        @rtype: dict
        """
        ret = self._http.get(self._url_resource_path, self._id, 'metadata')
        return ret.get('metadata')

    def set_metadata(self, **metadata):
        """
        Update metadata of a volume snapshot

        @keyword metadata: key=value style.
        @type metadata: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'metadata',
                        data={'metadata': metadata})
        self.reload()

    def unset_metadata(self, *keys):
        """
        Delete metadata of a volume snapshot

        @param key: key of the metadata
        @type keys: [str]
        @rtype: None
        """
        for key in keys:
            self._http.delete(self._url_resource_path, self._id,
                              'metadata', key)
        self.reload()


class Manager(base.Manager):
    """manager class for volume snapshots on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'snapshot'
    _json_resources_key = 'snapshots'
    _hidden_methods = ["update"]
    _url_resource_list_path = '/snapshots/detail'
    _url_resource_path = '/snapshots'

    def create(self, name=UNDEF, description=UNDEF, metadata=UNDEF,
               source=UNDEF, force=False):
        """
        Create a snapshot of a volume

        @keyword name: Snapshot name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword metadata: Metadata
        @type metadata: dict
        @keyword source: Source volume
        @type source: yakumo.cinder.v2.volume.Resource
        @return: Created volume object
        @rtype: yakumo.cinder.v2.snapshot.Resource
        """
        return super(Manager, self).create(name=name,
                                           description=description,
                                           metadata=metadata,
                                           source=source,
                                           force=force)
