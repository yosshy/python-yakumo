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
Resource class and its manager for security groups in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils
from . import security_group_rule


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('_rules', 'rules', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for security groups in Compute API v2"""

    _sub_manager_list = {
        'rules': security_group_rule.Manager
    }


class Manager(base.Manager):
    """Manager class for security groups in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'security_group'
    _json_resources_key = 'security_groups'
    _url_resource_path = '/os-security-groups'

    def create(self, name=UNDEF, description=UNDEF, project=UNDEF):
        """
        Create a security group

        @keyword name: Security group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @return: Created security group
        @rtype: yakumo.nova.v2.security_group.Resource
        """
        return super(Manager, self).create(name=name,
                                           description=description,
                                           project=project)
