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
Resource class and its manager for cloudpipes in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('server', 'instance_id', mapper.Resource('server')),
    ('project', 'project_id', mapper.Resource('project')),
    ('internal_ip', 'internal_ip', mapper.Noop),
    ('public_ip', 'public_ip', mapper.Noop),
    ('public_port', 'public_port', mapper.Noop),
    ('created_at', 'created_at', mapper.Noop),
    ('status', 'state', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for cloudpipes in Compute API v2"""

    def update(self, vpn_ip=UNDEF, vpn_port=UNDEF):
        """
        Update properties of a cloudpipe

        @keyword vpn_ip: IP address for VPN
        @type vpn_ip: str
        @keyword vpn_port: Port number for VPN
        @type vpn_port: str or int
        @rtype: None
        """
        self._http.post(join_path(self._url_resource_path, self._id,
                                  "configure-project"),
                        data=utils.get_json_body('configure_project',
                                                 vpn_ip=vpn_ip,
                                                 vpn_port=str(vpn_port)))


class Manager(base.Manager):
    """Manager class for cloudpipes in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _id_attr = 'server'
    _json_resource_key = 'cloudpipe'
    _json_resources_key = 'cloudpipes'
    _url_resource_path = '/os-cloudpipe'

    def create(self, project=UNDEF):
        """
        Create a cloudpipe

        @keyword project: Project
        @type project: yakumo.project.Resource
        @return: Created cloudpipe
        @rtype: yakumo.nova.v2.cloudpipe.Resource
        """
        return super(Manager, self).create(project=project)
