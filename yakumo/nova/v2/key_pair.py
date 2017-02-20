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
Resource class and its manager for key pairs in Compute API v2
"""

from yakumo import base
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('name', 'name', mapper.Noop),
    ('fingerprint', 'fingerprint', mapper.Noop),
    ('public_key', 'public_key', mapper.Noop),
    ('user', 'user_id', mapper.Resource('user')),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
    ('deleted_at', 'deleted_at', mapper.DateTime),
    ('is_deleted', 'deleted', mapper.Noop),
]


class Resource(base.Resource):
    """Resource class for key pairs in Compute API v2"""


class Manager(base.Manager):
    """Manager class for key pairs in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _id_attr = 'name'
    _json_resource_key = 'keypair'
    _json_resources_key = 'keypairs'
    _url_resource_path = '/os-keypairs'

    def create(self, name=None, public_key=None):
        """
        Register a SSH public key

        @keyword name: Key name
        @type name: str
        @keyword public_key: content of SSH public key
        @type public_key: str
        @return: Registered key
        @rtype: yakumo.nova.v2.key_pair.Resource
        """
        return super(Manager, self).create(name=name, public_key=public_key)

    def _find_gen(self, **kwargs):
        ret = self._http.get(self._url_resource_list_path)
        for x in ret[self._json_resources_key]:
            ret = self.get(x[self._json_resource_key]['name'])
            for k, v in kwargs.items():
                if getattr(ret, k, None) != v:
                    break
            else:
                yield ret
