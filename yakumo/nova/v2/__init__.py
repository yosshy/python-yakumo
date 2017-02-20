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
Sub client class for Nova API v2
"""

from . import agent
from . import aggregate
from . import availability_zone
from . import certificate
from . import cloudpipe
from . import fixed_ip
from . import flavor
from . import floating_ip
from . import floating_ip_bulk
from . import floating_ip_dns
from . import hypervisor
from . import image
from . import key_pair
from . import network
from . import security_group
from . import security_group_default_rule
from . import server
from . import server_group
from . import service
from . import quota_set


class Client(object):

    def __init__(self, client, *args, **kwargs):
        self.agent = agent.Manager(client)
        self.aggregate = aggregate.Manager(client)
        self.availability_zone = availability_zone.Manager(client)
        self.certificate = certificate.Manager(client)
        self.cloudpipe = cloudpipe.Manager(client)
        self.fixed_ip = fixed_ip.Manager(client)
        self.flavor = flavor.Manager(client)
        self.floating_ip = floating_ip.Manager(client)
        self.floating_ip_bulk = floating_ip_bulk.Manager(client)
        self.floating_ip_dns = floating_ip_dns.Manager(client)
        self.hypervisor = hypervisor.Manager(client)
        self.image = image.Manager(client)
        self.key_pair = key_pair.Manager(client)
        self.network = network.Manager(client)
        self.security_group = security_group.Manager(client)
        self.security_group_default_rule = \
            security_group_default_rule.Manager(client)
        self.server = server.Manager(client)
        self.server_group = server_group.Manager(client)
        self.service = service.Manager(client)
        self.quota_set = quota_set.Manager(client)

        client.aggregate = self.aggregate
        client.availability_zone = self.availability_zone
        client.cloudpipe = self.cloudpipe
        client.fixed_ip = self.fixed_ip
        client.flavor = self.flavor
        client.floating_ip = self.floating_ip
        client.floating_ip_bulk = self.floating_ip_bulk
        client.floating_ip_dns = self.floating_ip_dns
        client.hypervisor = self.hypervisor
        client.image = self.image
        client.key_pair = self.key_pair
        client.network = self.network
        client.security_group = self.security_group
        client.security_group_default_rule = \
            self.security_group_default_rule
        client.server = self.server
        client.server_group = self.server_group
