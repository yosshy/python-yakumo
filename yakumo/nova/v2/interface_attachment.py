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
Resource class and its manager for interface attachment in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('port', 'port_id', mapper.Resource('port')),
    ('id', 'port_id', mapper.Resource('port')),
    ('network', 'net_id', mapper.Resource('network')),
    ('mac_addr', 'mac_addr', mapper.Noop),
    ('fixed_ips', 'fixed_ips', mapper.Noop),
    ('status', 'port_state', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for interface attachment in Compute API v2"""

    def detach(self):
        """
        Detach a interface

        @rtype: None
        """
        super(Resource, self).delete()


class Manager(base.SubManager):
    """Manager class for interface attachment in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "update", "delete"]
    _json_resource_key = 'interfaceAttachment'
    _json_resources_key = 'interfaceAttachments'
    _url_resource_path = '/servers/%s/os-interface'

    def attach(self, port=UNDEF, network=UNDEF, fixed_ips=UNDEF):
        """Attach a interface

        @keyword port: Port
        @type port: yakumo.neutron.v2.port.Resource
        @keyword network: Network
        @type network: yakumo.neutron.v2.network.Resource
        @keyword fixed_ips: list of fixed ips (required if network= exists)
        @type fixed_ips: [yakumo.neutron.v2.fixed_ip.Resource]
        @return: Interface attachment
        @rtype: yakumo.nova.v2.interface_attachment.Resource
        """
        return super(Manager, self).create(port=port,
                                           network=network,
                                           fixed_ips=fixed_ips)
