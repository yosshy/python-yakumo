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
Resource class and its manager for agents in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'agent_id', mapper.Noop),
    ('architecture', 'architecture', mapper.Noop),
    ('hypervisor', 'hypervisor', mapper.Noop),
    ('md5hash', 'md5hash', mapper.Noop),
    ('os', 'os', mapper.Noop),
    ('url', 'url', mapper.Noop),
    ('version', 'version', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for agents in Compute API v2"""

    def update(self, architecture=UNDEF, hypervisor=UNDEF, os=UNDEF, url=UNDEF,
               version=UNDEF):
        """
        Update properties of an agent

        @keyword architecture: Architecture
        @type architecture: str
        @keyword hypervisor: Hypervisor
        @type hypervisor: str
        @keyword os: Operating System
        @type os: str
        @keyword url: URL
        @type url: str
        @keyword version: Version
        @type version: str
        @rtype: None
        """
        super(Resource, self).update(
            architecture=architecture,
            hypervisor=hypervisor,
            os=os,
            url=url,
            version=version)


class Manager(base.Manager):
    """Manager class for agents in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'agent'
    _json_resources_key = 'agents'
    _url_resource_path = '/os-agents'

    def create(self, architecture=UNDEF, hypervisor=UNDEF, os=UNDEF, url=UNDEF,
               version=UNDEF):
        """
        Register an agent

        @keyword architecture: Architecture
        @type architecture: str
        @keyword hypervisor: Hypervisor
        @type hypervisor: str
        @keyword os: Operating System
        @type os: str
        @keyword url: URL
        @type url: str
        @keyword version: Version
        @type version: str
        @return: Registered agent
        @rtype: yakumo.nova.v2.agent.Resource
        """
        return super(Manager, self).create(
            architecture=architecture,
            hypervisor=hypervisor,
            os=os,
            url=url,
            version=version)
