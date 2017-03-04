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
Resource class and its manager for LBaaS listeners in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('protocol', 'protocol', mapper.Noop),
    ('protocol_port', 'protocol_port', mapper.Noop),
    ('connection_limit', 'connection_limit', mapper.Noop),
    ('default_tls_container_ref', 'default_tls_container_ref',
     mapper.Noop),
    ('sni_container_refs', 'sni_container_refs', mapper.Noop),
    ('default_pool', 'default_pool_id',
     mapper.Resource('neutron.lbaas.pool')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for LBaaS listeners in Networking V2 API"""

    def update(self, name=UNDEF, description=UNDEF, connection_limit=UNDEF,
               default_tls_container_ref=UNDEF, sni_container_refs=UNDEF,
               is_enabled=UNDEF):

        """
        Update a listener for LBaaS

        @keyword name: Listener name
        @type name: srt
        @keyword description: Description
        @type description: str
        @keyword connection_limit: Maximun connection number
        @type connection_limit: int
        @keyword default_tls_container_ref: A reference to a container of
        TLS secrets
        @type default_tls_container_ref: str
        @keyword sni_container_refs: A list of references to TLS secrets
        @type sni_container_refs: [str]
        @keyword is_enabled: Is listener enabled
        @type is_enabled: bool
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            connection_limit=connection_limit,
            default_tls_container_ref=default_tls_container_ref,
            sni_container_refs=sni_container_refs,
            is_enabled=is_enabled)


class Manager(base.SubManager):
    """Manager class for LBaaS listeners in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'listener'
    _json_resources_key = 'listeners'
    _url_resource_path = '/v2.0/lbaas/listeners'

    def create(self, name=UNDEF, description=UNDEF, protocol=UNDEF,
               protocol_port=UNDEF, connection_limit=UNDEF,
               default_tls_container_ref=UNDEF, sni_container_refs=UNDEF,
               project=UNDEF, is_enabled=UNDEF):
        """
        Create a listener for LBaaS

        @keyword name: Listener name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword protocol: Protocol ('TCP', 'UDP', 'HTTP' or 'HTTPS')
        @type protocol: str
        @keyword protocol_port: Protocol port number
        @type protocol_port: int
        @keyword connection_limit: Maximun connection number
        @type connection_limit: int
        @keyword default_tls_container_ref: A reference to a container of
        TLS secrets
        @type default_tls_container_ref: str
        @keyword sni_container_refs: A list of references to TLS secrets
        @type sni_container_refs: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @keyword is_enabled: Whether the listner is enabled
        @type is_enabled: bool
        @return: Created listener
        @rtype: yakumo.neutron.v2.lbaas.listener.Resource
        """
        load_balancer = self.parent_resource
        return super(Manager, self).create(
            name=name,
            description=description,
            protocol=protocol,
            protocol_port=protocol_port,
            connection_limit=connection_limit,
            loadbalancer=loadbalancer,
            default_tls_container_ref=default_tls_container_ref,
            sni_container_refs=sni_container_refs,
            project=project,
            is_enabled=is_enabled)
