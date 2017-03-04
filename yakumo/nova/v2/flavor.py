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
Resource class and its manager for flavors in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('ram', 'ram', mapper.Noop),
    ('vcpus', 'vcpus', mapper.Noop),
    ('disk', 'disk', mapper.Noop),
    ('ephemeral', 'OS-FLV-EXT-DATA:ephemeral', mapper.Noop),
    ('swap', 'swap', mapper.Noop),
    ('rxtx_factor', 'rxtx_factor', mapper.Noop),
    ('is_public', 'os-flavor-access:is_public', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for flavors in Compute API v2"""

    def add_project(self, project=None):
        """
        Make a project accessible to the flavor

        @keyword project: Project (required)
        @type project: yakumo.project.Resource
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body('addTenantAccess',
                                                 tenant=project.id))

    def remove_project(self, project=None):
        """
        Make a project accessible to the flavor

        @keyword project: Project (required)
        @type project: yakumo.project.Resource
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body('removeTenantAccess',
                                                 tenant=project.id))

    def list_project(self):
        """
        Make a project accessible to the flavor

        @return: Project list
        @rtype: [yakumo.project.Resource]
        """
        ret = self._http.get(self._url_resource_path, self._id,
                             'os-flavor-access')
        return [self._client.project.get_empty(x["tenant_id"])
                for x in ret.get("flavor_access", [])]

    def get_extra_spec(self, key=None):
        """Get extra specs for a flavor

        @keyword key: key
        @type key: str
        @return: value
        @rtype: str
        """
        if key is None:
            ret = self._http.get(self._url_resource_path, self._id,
                                 'os-extra_specs')
            return ret.get('extra_specs', {})
        else:
            return self._http.get(self._url_resource_path, self._id,
                                  'os-extra_specs', key)

    def create_extra_spec(self, extra_spec=None):
        """
        Create extra specs for a flavor

        @keyword extra_spec: Extra specs
        @type extra_spec: dict
        @rtype: None
        """
        if not isinstance(_kwargs, dict):
            _kwargs = {}
        kwargs.update(_kwargs)
        kwargs = {k: str(v) for k, v in kwargs.items()}
        self._http.post(self._url_resource_path, self._id, 'os-extra_specs',
                        data=dict(extra_specs=kwargs))

    def update_extra_spec(self, _kwargs=None, **kwargs):
        """
        Update extra specs for a flavor

        @keyword extra_spec: Extra specs
        @type extra_spec: dict
        @rtype: None
        """
        if not isinstance(_kwargs, dict):
            _kwargs = {}
        kwargs.update(_kwargs)
        kwargs = {k: str(v) for k, v in kwargs.items()}
        for key, value in kwargs.items():
            self._http.put(self._url_resource_path, self._id, 'os-extra_specs',
                           key,
                           data={key: value})

    def delete_extra_spec(self, key):
        """Delete one key=value from extra specs

        @keyword key: Key
        @type key: str
        @rtype: None
        """
        self._http.delete(self._url_resource_path, self._id, 'os-extra_specs',
                          key)


class Manager(base.Manager):
    """Manager class for flavors in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'flavor'
    _json_resources_key = 'flavors'
    _url_resource_path = '/flavors'
    _url_resource_list_path = '/flavors/detail'

    def create(self, id=UNDEF, name=UNDEF, ram=UNDEF, vcpus=UNDEF,
               disk=UNDEF, ephemeral=UNDEF, swap=UNDEF, rxtx_factor=UNDEF,
               is_public=UNDEF):
        """Register a flavor

        @keyword id: ID of the new flavor (int)
        @type id: int
        @keyword name: name of the new flavor (str)
        @type name: str
        @keyword vcpus: number of virtual CPU(s) (int)
        @type vcpus: int
        @keyword ram: size of RAM in MB (int)
        @type ram: int
        @keyword disk: size of ephemeral disk for image in GB (int)
        @type disk: int
        @keyword ephemeral: size of extra ephemeral disk in GB (int)
        @type ephemeral: int
        @keyword swap: size of swap ephemeral disk in GB (int)
        @type swap: int
        @keyword rxtx_factor: rate of bandwidth cap (float)
        @type rxtx_factor: float
        @keyword is_public: the new flavor is public or not (bool)
        @type is_public: bool
        @return: Registered flavor
        @rtype: yakumo.nova.v2.flavor.Resource
        """
        return super(Manager, self).create(id=id, name=name, ram=ram,
                                           vcpus=vcpus, disk=disk,
                                           ephemeral=ephemeral,
                                           swap=swap,
                                           rxtx_factor=rxtx_factor,
                                           is_public=is_public)
