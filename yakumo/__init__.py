# Copyright 2014-2017 by Akira Yoshiyama <akirayoshiyama@gmail.com>.
# All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""
Client class definition
"""

import os

from . import exception
from . import rest_client


class Client(object):

    def __init__(self, **kwargs):
        self._os_config = rest_client.get_config(**kwargs)
        self._rest_clients = rest_client.get_rest_clients(**kwargs)
        self._RestClient = rest_client.RestClient

        keystone_v2_client = None
        if 'identity' in self._rest_clients:
            if self._os_config['identity_api_version'] == '2.0':
                import yakumo.keystone.v2
                self.keystone = yakumo.keystone.v2.Client(self)
            elif self._os_config['identity_api_version'] == '3':
                import yakumo.keystone.v3
                self.keystone = yakumo.keystone.v3.Client(self)

        if 'compute' in self._rest_clients:
            if self._os_config['compute_api_version'] == '2':
                import yakumo.nova.v2
                self.nova = yakumo.nova.v2.Client(self)

        if 'image' in self._rest_clients:
            if self._os_config['image_api_version'] == '1':
                import yakumo.glance.v1
                self.glance = yakumo.glance.v1.Client(self)
            elif self._os_config['image_api_version'] == '2':
                import yakumo.glance.v2
                self.glance = yakumo.glance.v2.Client(self)

        if 'volume' in self._rest_clients:
            if self._os_config['volume_api_version'] == '1':
                import yakumo.cinder.v1
                self.cinder = yakumo.cinder.v1.Client(self)
            elif self._os_config['volume_api_version'] == '2':
                import yakumo.cinder.v2
                self.cinder = yakumo.cinder.v2.Client(self)

        if 'network' in self._rest_clients:
            if self._os_config['network_api_version'] == '2':
                import yakumo.neutron.v2
                self.neutron = yakumo.neutron.v2.Client(self)
