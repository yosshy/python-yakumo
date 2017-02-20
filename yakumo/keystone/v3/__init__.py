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
Sub client class for Identity V3 API
"""

from . import credential
from . import domain
from . import endpoint
from . import group
from . import project
from . import role
from . import region
from . import service
from . import user


class Client(object):

    def __init__(self, client, *args, **kwargs):
        self.region = region.Manager(client)
        self.service = service.Manager(client)
        self.endpoint = endpoint.Manager(client)
        self.role = role.Manager(client)
        self.domain = domain.Manager(client)
        self.project = project.Manager(client)
        self.group = group.Manager(client)
        self.user = user.Manager(client)
        self.credential = credential.Manager(client)

        client.region = self.region
        client.service = self.service
        client.endpoint = self.endpoint
        client.role = self.role
        client.domain = self.domain
        client.project = self.project
        client.group = self.group
        client.user = self.user
        client.credential = self.credential
