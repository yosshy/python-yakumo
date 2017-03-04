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
Resource class and its manager for LB Health Monitors in Networking V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('is_enabled', 'admin_state_up', mapper.Noop),
    ('pools', 'pools',
     mapper.List(mapper.Resource('neutron.lb.pool'))),
    ('type', 'type', mapper.Noop),
    ('http_method', 'http_method', mapper.Noop),
    ('url_path', 'url_path', mapper.Noop),
    ('expected_codes', 'expected_codes', mapper.Noop),
    ('delay', 'delay', mapper.Noop),
    ('timeout', 'timeout', mapper.Noop),
    ('max_retries', 'max_retries', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for LB Health Monitors in Networking V2 API"""

    def update(self, delay=UNDEF):
        """
        Update a LB health monitor

        @keyword delay: Seconds to start waiting a response
        @type delay: int
        @rtype: None
        """
        super(Resource, self).update(delay=delay)


class Manager(base.Manager):
    """Manager class for LB Health Monitors in Networking V2 API"""

    resource_class = Resource
    service_type = 'network'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'health_monitor'
    _json_resources_key = 'health_monitors'
    _url_resource_path = '/v2.0/lb/health_monitors'

    def create(self, type=UNDEF, http_method=UNDEF, url_path=UNDEF,
               expected_codes=UNDEF, delay=UNDEF, timeout=UNDEF,
               max_retries=UNDEF, is_enabled=UNDEF):
        """
        Create a LB health monitor

        @keyword type: Monitor type ('PING', 'TCP', 'HTTP', or 'HTTPS')
        @type type: str
        @keyword http_method: HTTP method like 'GET'
        @type http_method: str
        @keyword url_path: URL path like '/index.html'
        @type url_path: str
        @keyword expected_codes: Expected HTTP response code list separated
        with comma
        @type expected_codes: str
        @keyword delay: Seconds to start waiting a response
        @type delay: int
        @keyword timeout: Maximum seconds to wait a response
        @type timeout: int
        @keyword max_retries: Number of allowed connection failures (up to 10)
        @type max_retries: int
        @keyword is_enabled: Monitor is enabled
        @type is_enabled: bool
        @return: Created monitor
        @rtype: yakumo.neutron.v2.lb.health_monitor.Resource
        """
        return super(Manager, self).create(type=type,
                                           http_method=http_method,
                                           url_path=url_path,
                                           expected_codes=expected_codes,
                                           delay=delay,
                                           timeout=timeout,
                                           max_retries=max_retries,
                                           is_enabled=is_enabled)
