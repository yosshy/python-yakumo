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


from . import st10_v2_role_project_user_admin
from . import st11_v2_service_endpoint_admin
from . import st12_v3_role_project_user_admin
from . import st13_v3_service_endpoint_admin
from . import st14_v3_project_on_project_admin
from . import st15_v3_region_on_region_admin
from . import st20_image
from . import st22_image_metadata_nova
from . import st30_network_subnet_port
from . import st31_security_group
from . import st40_volume_snapshot
from . import st41_upload_to_image
from . import st42_volume_type_admin
from . import st43_volume_type_qos_admin
from . import st50_server
from . import st51_boot_from_volume
from . import st52_attach_volume
from . import st53_attach_interface
from . import st54_server_metadata
from . import st55_host_aggregate_admin
from . import st56_key_pair


__all__ = [
    'KEYSTONE_TESTS',
    'GLANCE_TESTS',
    'NEUTRON_TESTS',
    'CINDER_TESTS',
    'NOVA_TESTS',
]

KEYSTONE_TESTS = [
    st10_v2_role_project_user_admin,
    st11_v2_service_endpoint_admin,
    st12_v3_role_project_user_admin,
    st13_v3_service_endpoint_admin,
    st14_v3_project_on_project_admin,
    st15_v3_region_on_region_admin,
]

GLANCE_TESTS = [
    st20_image,
    st22_image_metadata_nova,
]

NEUTRON_TESTS = [
    st30_network_subnet_port,
    st31_security_group,
]

CINDER_TESTS = [
    st40_volume_snapshot,
    st41_upload_to_image,
    st42_volume_type_admin,
    st43_volume_type_qos_admin,
]

NOVA_TESTS = [
    st50_server,
    st51_boot_from_volume,
    st52_attach_volume,
    st53_attach_interface,
    st54_server_metadata,
    st55_host_aggregate_admin,
    st56_key_pair,
]
