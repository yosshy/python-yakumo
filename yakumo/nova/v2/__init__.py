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

    def __init__(self, client, **kwargs):
        self.agent = agent.Manager(client, **kwargs)
        self.aggregate = aggregate.Manager(client, **kwargs)
        self.availability_zone = availability_zone.Manager(client, **kwargs)
        self.certificate = certificate.Manager(client, **kwargs)
        self.cloudpipe = cloudpipe.Manager(client, **kwargs)
        self.fixed_ip = fixed_ip.Manager(client, **kwargs)
        self.flavor = flavor.Manager(client, **kwargs)
        self.floating_ip = floating_ip.Manager(client, **kwargs)
        self.floating_ip_bulk = floating_ip_bulk.Manager(client, **kwargs)
        self.floating_ip_dns = floating_ip_dns.Manager(client, **kwargs)
        self.hypervisor = hypervisor.Manager(client, **kwargs)
        self.image = image.Manager(client, **kwargs)
        self.key_pair = key_pair.Manager(client, **kwargs)
        self.network = network.Manager(client, **kwargs)
        self.security_group = security_group.Manager(client, **kwargs)
        self.security_group_default_rule = \
            security_group_default_rule.Manager(client, **kwargs)
        self.server = server.Manager(client, **kwargs)
        self.server_group = server_group.Manager(client, **kwargs)
        self.service = service.Manager(client, **kwargs)
        self.quota_set = quota_set.Manager(client, **kwargs)

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
