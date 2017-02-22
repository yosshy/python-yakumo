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
Resource class and its manager for projects in Identity V3 API
"""

from yakumo import base
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('parent', 'parent_id', mapper.Resource('keystone.project')),
    ('domain', 'domain_id', mapper.Resource('keystone.domain')),
    ('is_enabled', 'enabled', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for projects on Identity V3 API"""

    def update(self, name=None, description=None, parent=None, domain=None,
               is_enabled=None):
        """
        Update properties of a project

        @keyword name: Project name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword parent: Parent project
        @type parent: yakumo.keystone.v3.project.Resource
        @keyword domain: Domain
        @type domain: yakumo.keystone.v3.domain.Resource
        @keyword is_enabled: Whether project is enabled or not
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            parent=parent,
            domain=domain,
            is_enabled=is_enabled)


class Manager(base.Manager):
    """manager class for projects on Identity V3 API"""

    resource_class = Resource
    service_type = 'identity'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'project'
    _json_resources_key = 'projects'
    _update_method = 'patch'
    _url_resource_path = '/projects'

    def create(self, name=None, description=None, parent=None, domain=None,
               is_enabled=None):
        """
        Register a project

        @keyword name: Project name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword parent: Parent project
        @type parent: yakumo.keystone.v3.project.Resource
        @keyword domain: Domain
        @type domain: yakumo.keystone.v3.domain.Resource
        @keyword is_enabled: Whether project is enabled or not
        @type is_enabled: bool
        @return: Created project
        @rtype: yakumo.keystone.v3.project.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            parent=parent,
            domain=domain,
            is_enabled=is_enabled)
