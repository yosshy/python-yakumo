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
Resource class and its manager for hypervisors in Compute API v2
"""

from yakumo import base
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('hostname', 'hypervisor_hostname', mapper.Noop),
    ('type', 'hypervisor_type', mapper.Noop),
    ('version', 'hypervisor_version', mapper.Noop),
    ('cpu_info', 'cpu_info', mapper.Noop),
    ('workload', 'current_workload', mapper.Noop),
    ('disk_available_least', 'disk_available_least', mapper.Noop),
    ('free_disk_gb', 'free_disk_gb', mapper.Noop),
    ('free_ram_mb', 'free_ram_mb', mapper.Noop),
    ('local_gb', 'local_gb', mapper.Noop),
    ('local_gb_used', 'local_gb_used', mapper.Noop),
    ('memory_mb', 'memory_mb', mapper.Noop),
    ('memory_mb_used', 'memory_mb_used', mapper.Noop),
    ('running_vms', 'running_vms', mapper.Noop),
    ('service', 'service', mapper.Noop),
    ('vcpus', 'vcpus', mapper.Noop),
    ('vcpus_used', 'vcpus_used', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for hypervisors in Compute API v2"""


class Manager(base.Manager):
    """Manager class for hypervisors in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["create", "update"]
    _json_resource_key = 'hypervisor'
    _json_resources_key = 'hypervisors'
    _url_resource_path = '/os-hypervisors'

    def get_total_stats(self):
        """
        Aquire total statistics of hypervisors

        @return: Statistics
        @rtype: dict
        """
        return self._http.get(utils.join_path(self._url_resource_path,
                                              "statistics"))

    def servers(self, host):
        """
        Aquire hypervisor hosts

        @return: Host list
        @rtype: dict
        """
        return self._http.get(utils.join_path(self._url_resource_path,
                                              host, "servers"))
