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
Resource class and its manager for volume types on Block Storage V2 API
"""

import copy

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('metadata', 'extra_specs', mapper.Noop),
    ('is_public', 'is_public', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for volume types on Block Storage V2 API"""

    def set_metadata(self, **kwargs):
        """
        Remove metadata

        **kwargs: key=value style metadata
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'extra_specs',
                        data=utils.get_json_body("extra_specs", **kwargs))
        self.reload()

    def unset_metadata(self, *keys):
        """
        Remove metadata

        *keys: keys of metadata to remove
        @rtype: None
        """
        for key in keys:
            self._http.delete(self._url_resource_path, self._id,
                              'extra_specs', key)
        self.reload()

    def add_project(self, project=None):
        """
        Add private volume type access

        @keyword project: Project
        @type project: yakumo.project.Resource
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("addProjectAccess",
                                                 project=project.get_id()))

    def remove_project(self, project=None):
        """
        Remove private volume type access

        @keyword project: Project
        @type project: yakumo.project.Resource
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("removeProjectAccess",
                                                 project=project.get_id()))


class Manager(base.Manager):
    """manager class for volume types on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'volume_type'
    _json_resources_key = 'volume_types'
    _url_resource_list_path = '/types'
    _url_resource_path = '/types'

    def create(self, name=UNDEF, description=UNDEF, metadata=UNDEF,
               is_public=UNDEF):
        """
        Register a volume type

        @keyword name: Volume type name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword metadata: Metadata (key=value)
        @type metadata: dict
        @keyword is_public: Whether volume type is public
        @type is_public: bool
        @return: Created volume type
        @rtype: yakumo.cinder.v2.volume_type.Resource
        """
        return super(Manager, self).create(name=name,
                                           description=description,
                                           metadata=metadata,
                                           is_public=is_public)
