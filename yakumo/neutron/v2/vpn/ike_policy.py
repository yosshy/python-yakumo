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
Resource class and its manager for VPN IKE policies in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'description', mapper.Noop),
    ('auth_algorithm', 'auth_algorithm', mapper.Noop),
    ('encryption_algorithm', 'encryption_algorithm', mapper.Noop),
    ('pfs', 'pfs', mapper.Noop),
    ('phase1_negotiation_mode', 'phase1_negotiation_mode', mapper.Noop),
    ('lifetime', 'lifetime', mapper.Noop),
    ('ike_version', 'ike_version', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
]


class Resource(base.Resource):
    """Resource class for VPN IKE policies in Networking V2 API"""

    def update(self, name=UNDEF, description=UNDEF, auth_algorithm=UNDEF,
               encryption_algorithm=UNDEF, pfs=UNDEF,
               phase1_negotiation_mode=UNDEF, lifetime=UNDEF,
               ike_version=UNDEF, project=UNDEF):
        """
        Update an IKE policy

        @keyword name: IKE policy name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword auth_algorithm: Auth algorithm; only 'sha1'
        @type auth_algorithm: str
        @keyword encryption_algorithm: Encryption algorithm
        ('3des', 'aes-128', 'aes-192', ...)
        @type encryption_algorithm: str
        @keyword pfs: Perfect forward secrecy
        ('Group2', 'Group5', 'Group14', ...)
        @type pfs: str
        @keyword phase1_negotiation_mode: IKE mode; only 'main'
        @type phase1_negotiation_mode: str
        @keyword lifetime: Life time; e.q.'3600seconds'
        @type lifetime: str
        @keyword ike_version: IKE version; 'v1' or 'v2'
        @type ike_version: str
        @keyword project: Project
        @type project: yakumo.project.Resource
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            auth_algorithm=auth_algorithm,
            encryption_algorithm=encryption_algorithm,
            pfs=pfs,
            phase1_negotiation_mode=phase1_negotiation_mode,
            lifetime=lifetime,
            ike_version=ike_version,
            project=project)


class Manager(base.Manager):
    """Manager class for VPN IKE policies in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'ike_policy'
    _json_resources_key = 'ike_policies'
    _url_resource_path = '/v2.0/vpn/ike_policies'

    def create(self, name=UNDEF, description=UNDEF, auth_algorithm=UNDEF,
               encryption_algorithm=UNDEF, pfs=UNDEF,
               phase1_negotiation_mode=UNDEF, lifetime=UNDEF,
               ike_version=UNDEF, project=UNDEF):
        """
        Create an IKE policy

        @keyword name: IKE policy name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword auth_algorithm: Auth algorithm; only 'sha1'
        @type auth_algorithm: str
        @keyword encryption_algorithm: Encryption algorithm
        ('3des', 'aes-128', 'aes-192', ...)
        @type encryption_algorithm: str
        @keyword pfs: Perfect forward secrecy
        ('Group2', 'Group5', 'Group14', ...)
        @type pfs: str
        @keyword phase1_negotiation_mode: IKE mode; only 'main'
        @type phase1_negotiation_mode: str
        @keyword lifetime: Life time; e.q.'3600seconds'
        @type lifetime: str
        @keyword ike_version: IKE version; 'v1' or 'v2'
        @type ike_version: str
        @keyword project: Project object
        @type project: yakumo.project.Resource
        @return: Created policy
        @rtype: yakumo.neutron.v2.vpn.ike_policy.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            auth_algorithm=auth_algorithm,
            encryption_algorithm=encryption_algorithm,
            pfs=pfs,
            phase1_negotiation_mode=phase1_negotiation_mode,
            lifetime=lifetime,
            ike_version=ike_version,
            project=project)
