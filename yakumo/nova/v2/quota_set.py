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
Resource class and its manager for Quota sets in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('cores', 'cores', mapper.Noop),
    ('fixed_ips', 'fixed_ips', mapper.Noop),
    ('floating_ips', 'floating_ips', mapper.Noop),
    ('injected_file_content_bytes', 'injected_file_content_bytes',
     mapper.Noop),
    ('injected_file_path_bytes', 'injected_file_path_bytes', mapper.Noop),
    ('injected_files', 'injected_files', mapper.Noop),
    ('instances', 'instances', mapper.Noop),
    ('key_pairs', 'key_pairs', mapper.Noop),
    ('metadata_items', 'metadata_items', mapper.Noop),
    ('ram', 'ram', mapper.Noop),
    ('security_group_rules', 'security_group_rules', mapper.Noop),
    ('security_groups', 'security_groups', mapper.Noop),
    ('server_group_members', 'server_group_members', mapper.Noop),
    ('server_groups', 'server_groups', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for Quota sets in Compute API v2"""


class Manager(base.Manager):
    """Manager class for Quota sets in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
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
        @rtype: yakumo.nova.v2.quota_set.Resource
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

    def update(self, project=UNDEF, user=UNDEF, cores=UNDEF, fixed_ips=UNDEF,
               floating_ips=UNDEF, injected_file_content_bytes=UNDEF,
               injected_file_path_bytes=UNDEF, injected_files=UNDEF,
               instances=UNDEF, key_pairs=UNDEF, metadata_items=UNDEF,
               ram=UNDEF, security_group_rules=UNDEF, security_groups=UNDEF,
               server_group_members=UNDEF, server_groups=UNDEF):
        """
        Update quota set for a project

        @keyword project: Project object (required)
        @type project: yakumo.project.Resource
        @keyword user: User object
        @type user: yakumo.user.Resource
        @keyword cores: max number of cores
        @type cores: int
        @keyword fixed_ips: max number of fixed IPs
        @type fixed_ips: int
        @keyword floating_ips: max number of floating IPs
        @type floating_ips: int
        @keyword injected_file_content_bytes: max bytes of an injected file
        @type injected_file_content_bytes:int
        @keyword injected_file_path_bytes: max path length of an injected file
        @type injected_file_path_bytes: int
        @keyword injected_files: max number of injected files
        @type injected_files: int
        @keyword instances: max number of instances
        @type instances: int
        @keyword key_pairs: max number of key pairs
        @type key_pairs: int
        @keyword metadata_items: max number of metadata items
        @type metadata_items: int
        @keyword ram: max number of RAM
        @type ram: int
        @keyword security_group_rules: max number of security group rules
        @type security_group_rules: int
        @keyword security_groups: max number of security groups
        @type security_groups: int
        @keyword server_group_members: max number of server group members
        @type server_group_members: int
        @keyword server_groups: max number of server groups
        @type server_groups:int
        @rtype: None
        """
        if project is None:
            project = self._project
        params = {}
        if user:
            params = dict(user_id=user._id)
        kwargs = dict(cores=cores, fixed_ips=fixed_ips,
                      floating_ips=floating_ips,
                      injected_file_content_bytes=injected_file_content_bytes,
                      injected_file_path_bytes=injected_file_path_bytes,
                      injected_files=injected_files, instances=instances,
                      key_pairs=key_pairs, metadata_items=metadata_items,
                      ram=ram, security_group_rules=security_group_rules,
                      security_groups=security_groups,
                      server_group_members=server_group_members,
                      server_groups=server_groups)
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
        @rtype: yakumo.nova.v2.quota_set.Resource
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
