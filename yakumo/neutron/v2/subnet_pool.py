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
Resource class and its manager for subnet pools in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('prefixes', 'prefixes', mapper.Noop),
    ('ip_version', 'ip_version', mapper.Noop),
    ('min_prefixlen', 'min_prefixlen', mapper.Noop),
    ('default_prefixlen', 'default_prefixlen', mapper.Noop),
    ('max_prefixlen', 'max_prefixlen', mapper.Noop),
    ('default_quota', 'default_quota', mapper.Noop),
    ('is_shared', 'shared', mapper.Noop,),
    ('address_scope_id', 'address_scope_id', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for subnet pools in Compute API v2"""

    def update(self, name=UNDEF, address_scope_id=UNDEF, prefixes=UNDEF,
               default_prefixlen=UNDEF, min_prefixlen=UNDEF,
               max_prefixlen=UNDEF, default_quota=UNDEF, project=UNDEF):
        """
        Update a subnet pool

        @keyword name: Subnet pool name
        @type name: str
        @keyword address_scope_id: UUID of address scope
        @type address_scope_id: str
        @keyword prefixes: a list of subnets
        @type prefixes: [str]
        @keyword default_prefixlen: Default prefix length
        @type default_prefixlen: int
        @keyword min_prefixlen: Minimum prefix length
        @type min_prefixlen: int
        @keyword max_prefixlen: Maximum prefix length
        @type max_prefixlen: int
        @keyword default_quota: Default quota
        @type default_quota: int
        @keyword project: Project
        @type project: yakumo.project.Resource
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            address_scope_id=address_scope_id,
            prefixes=prefixes,
            default_prefixlen=default_prefixlen,
            min_prefixlen=min_prefixlen,
            max_prefixlen=max_prefixlen,
            default_quota=default_quota,
            project=project)


class Manager(base.Manager):
    """Manager class for subnet pools in Compute API v2"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'subnetpool'
    _json_resources_key = 'subnetpools'
    _url_resource_path = '/v2.0/subnetpools'

    def create(self, name=UNDEF, address_scope_id=UNDEF, prefixes=UNDEF,
               default_prefixlen=UNDEF, min_prefixlen=UNDEF,
               max_prefixlen=UNDEF, default_quota=UNDEF, project=UNDEF,
               is_shared=UNDEF):
        """
        Create a subnet pool

        @keyword name: Subnet pool name
        @type name: str
        @keyword address_scope_id: UUID of address scope
        @type address_scope_id: str
        @keyword prefixes: a list of subnets
        @type prefixes: [str]
        @keyword default_prefixlen: Default prefix length
        @type default_prefixlen: int
        @keyword min_prefixlen: Minimum prefix length
        @type min_prefixlen: int
        @keyword max_prefixlen: Maximum prefix length
        @type max_prefixlen: int
        @keyword default_quota: Default quota
        @type default_quota: int
        @keyword project: Project
        @type project: yakumo.porject.Resource
        @keyword is_shared: Whether the subnet pool is shared
        @type is_shared: bool
        @return: Created subnet pool
        @rtype: yakumo.neutron.v2.subnet_pool.Resource
        """
        return super(Manager, self).create(
            name=name,
            address_scope_id=address_scope_id,
            prefixes=prefixes,
            default_prefixlen=default_prefixlen,
            min_prefixlen=min_prefixlen,
            max_prefixlen=max_prefixlen,
            default_quota=default_quota,
            project=project,
            is_shared=is_shared)
