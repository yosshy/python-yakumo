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
Resource class and its manager for consistency group snapshot on
Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'display_description', mapper.Noop),
    ('source_cg', 'consistencygroup_id',
     mapper.List(mapper.Resource('cinder.consistency_group'))),
    ('project', 'project_id', mapper.List(mapper.Resource('project'))),
    ('user', 'user_id', mapper.List(mapper.Resource('user'))),
    ('status', 'status', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
]


class Resource(base.Resource):
    """resource class for consistency group snapshot on Block Storage V2 API"""


class Manager(base.Manager):
    """manager class for consistency group snapshot on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ['update']
    _json_resource_key = 'cgsnapshot'
    _json_resources_key = 'cgsnapshots'
    _url_resource_list_path = '/cgsnapshots/detail'
    _url_resource_path = '/cgsnapshots'

    def create(self, name=UNDEF, description=UNDEF, source_cg=UNDEF,
               project=UNDEF, user=UNDEF, status=UNDEF):
        """
        Create a consistency group snapshot

        @keyword name: Consistency group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword source_cg: Source consistency group
        @type source_cg: yakumo.cinder.v2.consistency_group.Resource
        @keyword project: Project (optional)
        @type project: yakumo.project.Resource
        @keyword user: User (optional)
        @type user: yakumo.user.Resource
        @return: Created consistency group snapshot
        @rtype: yakumo.cinder.v2.consistency_group_snapshot.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            source_cg=source_cg,
            project=project,
            user=user,
            status=status)
