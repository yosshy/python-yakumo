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
Resource class and its manager for volume attachment in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('device', 'device', mapper.Noop),
    ('server', 'serverId', mapper.Resource('nova.server')),
    ('volume', 'volumeId', mapper.Resource('volume')),
]


class Resource(base.Resource):
    """Resource class for volume attachment in Compute API v2"""

    def detach(self):
        """
        Detach a volume

        @rtype: None
        """
        super(Resource, self).delete()


class Manager(base.SubManager):
    """Manager class for volume attachment in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "update"]
    _json_resource_key = 'volumeAttachment'
    _json_resources_key = 'volumeAttachments'
    _url_resource_path = '/servers/%s/os-volume_attachments'

    def attach(self, device=UNDEF, volume=UNDEF):
        """
        Attach a volume

        @keyword device: device path on the guest OS (e.q. '/dev/sda')
        @type device: str
        @keyword volume: Volume (required)
        @type volume: yakumo.volume.Resource
        """
        return super(Manager, self).create(device=device,
                                           volume=volume)
