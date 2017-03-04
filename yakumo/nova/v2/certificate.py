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
Resource class and its manager for root certificates in Compute API v2
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('data', 'data', mapper.Noop),
    ('private_key', 'private_key', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for root certificates in Compute API v2"""


class Manager(base.Manager):
    """Manager class for root certificates in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update", "list", "find", "find_one"]
    _id_attr = 'private_key'
    _json_resource_key = 'certificate'
    _json_resources_key = 'certificates'
    _url_resource_path = '/os-certificates'

    def create(self, data=UNDEF, private_key=UNDEF):
        """
        Register a root certificate

        @keyword data: Certificate data (str, required)
        @type data: Certificate data (str, required)
        @keyword private_key: Priate key data (str)
        @type private_key: Priate key data (str)
        @return: Registered root certificate
        @rtype: yakumo.nova.v2.certificate.Resource
        """
        self._http.post(self._url_resource_path,
                        data=utils.get_json_body('certificate',
                                                 data=data,
                                                 private_key=private_key))

    def get(self):
        ret = self._http.get(self._url_resource_path)
        return ret.get('certificate')
