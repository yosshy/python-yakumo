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
Resource class and its manager for volume transfer on Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper

from . import volume


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('auth_key', 'auth_key', mapper.Noop),
    ('volume', 'volume_id', mapper.Resource('cinder.volume')),
    ('created_at', 'created_at', mapper.DateTime),
]


class Resource(base.Resource):
    """resource class for volume transfer on Block Storage V2 API"""

    def accept(self, auth_key):
        """
        Accept a volume transfer

        @keyword auth_key: authentication key for a transfer
        @type auth_key: str
        @return: Accepted volume
        @rtype: yakumo.cinder.v2.volume.Resource
        """
        ret = self._http.post(self._url_resource_path, self._id, 'accept',
                              data=utils.get_json_body("accept",
                                                       auth_key=auth_key))
        volume_id = ret['volume_id']
        return self._client.cinder.volume.get_empty(volume_id)


class Manager(base.Manager):
    """manager class for volume transfer on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'transfer'
    _json_resources_key = 'transfers'
    _hidden_methods = ["update"]
    _url_resource_list_path = '/os-volume-transfer/detail'
    _url_resource_path = '/os-volume-transfer'

    def create(self, name=UNDEF, volume=UNDEF):
        """
        Create a volume transfer

        @keyword name: Volume transfer name (optional)
        @type name: str
        @keyword volume: Volume to send
        @type volume: yakumo.cinder.v2.volume.Resource
        @return: Created volume transfer
        @rtype: yakumo.cinder.v2.volume_transfer.Resource
        """
        return super(Manager, self).create(name=name, volume=volume)
