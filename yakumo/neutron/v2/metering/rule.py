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
Resource class and its manager for metering label rules for Networking v2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('remote_ip_prefix', 'remote_ip_prefix', mapper.Noop),
    ('direction', 'direction', mapper.Noop),
    ('excluded', 'excluded', mapper.Noop),
    ('metering_label', 'metering_label_id',
     mapper.Resource('neutron.metering.label')),
]


class Resource(base.Resource):
    """Resource class for metering label rules for Networking v2 API"""


class Manager(base.Manager):
    """Manager class for metering label rules for Networking v2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = '"metering_label_rule'
    _json_resources_key = '"metering_label_rules'
    _url_resource_path = '/v2.0/metering/metering-label-rules'

    def create(self, remote_ip_prefix=UNDEF, direction=UNDEF,
               is_excluded=UNDEF, metering_label=UNDEF):
        """
        Create a metering label rule

        :param remote_ip_prefix=: Remote IP prefix (str)
        :param direction=: Direction; 'ingress' or 'egress' (str)
        :param is_excluded=: Is the rule excluded (bool)
        :param metering_label=: MeteringLabel object
        """
        return super(Manager, self).create(remote_ip_prefix=remote_ip_prefix,
                                           direction=direction,
                                           excluded=excluded,
                                           metering_label=metering_label)
