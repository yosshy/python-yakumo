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

import os_client_config

from . import exception
from . import session


class Client(object):

    def __init__(self, **kwargs):
        self._session = session.get_session(**kwargs)

        if self._session.has_endpoint('identity'):
            if self._session.config['identity_api_version'] == '2.0':
                import yakumo.keystone.v2
                self.keystone = yakumo.keystone.v2.Client(self, **kwargs)
            elif self._session.config['identity_api_version'] == '3':
                import yakumo.keystone.v3
                self.keystone = yakumo.keystone.v3.Client(self, **kwargs)

        if self._session.has_endpoint('compute'):
            if self._session.config['compute_api_version'] == '2':
                import yakumo.nova.v2
                self.nova = yakumo.nova.v2.Client(self, **kwargs)

        if self._session.has_endpoint('image'):
            if self._session.config['image_api_version'] == '1':
                import yakumo.glance.v1
                self.glance = yakumo.glance.v1.Client(self, **kwargs)
            elif self._session.config['image_api_version'] == '2':
                import yakumo.glance.v2
                self.glance = yakumo.glance.v2.Client(self, **kwargs)

        if self._session.has_endpoint('volume'):
            if self._session.config['volume_api_version'] == '1':
                import yakumo.cinder.v1
                self.cinder = yakumo.cinder.v1.Client(self, **kwargs)
            elif self._session.config['volume_api_version'] == '2':
                import yakumo.cinder.v2
                self.cinder = yakumo.cinder.v2.Client(self, **kwargs)

        if self._session.has_endpoint('network'):
            if self._session.config['network_api_version'] == '2':
                import yakumo.neutron.v2
                self.neutron = yakumo.neutron.v2.Client(self, **kwargs)
