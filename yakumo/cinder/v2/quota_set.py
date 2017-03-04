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
Resource class and its manager for Quota sets in Block Storage API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('volumes', 'volumes', mapper.Noop),
    ('per_volume_gigabytes', 'per_volume_gigabytes', mapper.Noop),
    ('snapshots', 'snapshots', mapper.Noop),
    ('gigabytes', 'gigabytes', mapper.Noop),
    ('backups', 'backups', mapper.Noop),
    ('backup_gigabytes', 'backup_gigabytes', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for Quota sets in Block Storage API v2"""


class Manager(base.Manager):
    """Manager class for Quota sets in Block Storage API v2"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create"]
    _json_resource_key = 'quota_set'
    _url_resource_path = '/os-quota-sets'

    def get(self, project=None, user=None):
        """
        Get quota set for a project

        @keyword project: Project (required)
        @type project: yakumo.project.Resource
        @keyword user: User
        @type user: yakumo.user.Resource
        @rtype: yakumo.cinder.v2.quota_set.Resource
        """
        if project is None:
            project = self._project
        params = {}
        if user:
            params = dict(user_id=user.get_id())
        try:
            ret = self._http.get(self._url_resource_path, project._id,
                                 params=params)
            json_params = ret.get(self._json_resource_key)
            attrs = self._json2attr(json_params)
            return self.resource_class(self, **attrs)
        except:
            return None

    def update(self, project=UNDEF, user=UNDEF, volumes=UNDEF,
               per_volume_gigabytes=UNDEF, snapshots=UNDEF, gigabytes=UNDEF,
               backups=UNDEF, backup_gigabytes=UNDEF):
        """
        Update quota set for a project

        @keyword project: Project object (required)
        @type project: yakumo.project.Resource
        @keyword user: User object
        @type user: yakumo.user.Resource
        @keyword volumes: Max number of volumes
        @type volumes: int
        @keyword per_volume_gigabytes: Max size of a volume in GB
        @type per_volume_gigabytes: int
        @keyword snapshots: Max number of snapshots
        @type snapshots: int
        @keyword gigabytes: Max total size of volumes in GB
        @type gigabytes:int
        @keyword backups: Max number of volume backups
        @type backups: int
        @keyword backup_gigabytes: max total size of volume backup in GB
        @type backup_gigabytes: int
        @rtype: None
        """
        if project is None:
            project = self._project
        params = {}
        if user:
            params = dict(user_id=user._id)
        kwargs = dict(volumes=volumes,
                      per_volume_gigabytes=per_volume_gigabytes,
                      snapshots=snapshots,
                      gigabytes=gigabytes,
                      backups=backups,
                      backup_gigabytes=backup_gigabytes)
        json_params = self._attr2json(kwargs)
        self._http.put(self._url_resource_path, project._id,
                       params=params,
                       data=utils.get_json_body(self._json_resource_key,
                                                **json_params))

    def delete(self, project=None, user=None):
        """
        Delete quota set for a project

        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword user: User
        @type user: yakumo.user.Resource
        @rtype: None
        """
        if project is None:
            project = self._project
        params = {}
        if user:
            params = dict(user_id=user._id)
        self._http.delete(self._url_resource_path, project._id,
                          params=params)

    def get_default(self, project=None):
        """
        Get default quota set for a project

        @keyword project: Project
        @type project: yakumo.project.Resource
        @return: Default quota set
        @rtype: yakumo.cinder.v2.quota_set.Resource
        """
        if project is None:
            project = self._project
        try:
            ret = self._http.get(self._url_resource_path, project._id)
            json_params = ret.get(self._json_resource_key)
            attrs = self._json2attr(json_params)
            return self.resource_class(self, **attrs)
        except:
            return None
