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
Sub client class for Cinder API v1
"""

from . import snapshot
from . import volume
from . import volume_type


class Client(object):

    def __init__(self, client, *args, **kwargs):
        self.volume = volume.Manager(client)
        self.volume_snapshot = snapshot.Manager(client)
        self.volume_type = volume_type.Manager(client)

        client.volume = self.volume
        client.volume_snapshot = self.volume_snapshot
        client.volume_type = self.volume_type