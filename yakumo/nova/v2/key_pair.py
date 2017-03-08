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

import os
import stat

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('name', 'name', mapper.Noop),
    ('fingerprint', 'fingerprint', mapper.Noop),
    ('public_key', 'public_key', mapper.Noop),
    ('private_key', 'private_key', mapper.Noop),
    ('type', 'type', mapper.Noop),
    ('user', 'user_id', mapper.Resource('user')),
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

    def create(self, name=UNDEF, public_key=UNDEF, private_key_file=UNDEF,
               type=UNDEF, user=UNDEF):
        """
        Register a SSH public key

        @keyword name: Key name
        @type name: str
        @keyword public_key: content of SSH public key
        @type public_key: str
        @keyword type: 'ssh' or 'x509'
        @type type: str
        @keyword user: Owner
        @type user: yakumo.user.Resource
        @return: Registered key
        @rtype: yakumo.nova.v2.key_pair.Resource
        """
        kwargs = dict(name=name,
                      public_key=public_key,
                      type=type,
                      user=user)
        json_params = self._attr2json(kwargs)
        ret = self._http.post(self._url_resource_path,
                              data={self._json_resource_key: json_params})
        attrs = self._json2attr(ret[self._json_resource_key])
        if 'private_key' in attrs and private_key_file != UNDEF:
            with open(private_key_file, "w") as f:
                f.write(attrs['private_key'])
            os.chmod(private_key_file, stat.S_IRUSR)
        return self.resource_class(self, **attrs)

    def _find_gen(self, **kwargs):
        ret = self._http.get(self._url_resource_list_path)
        for x in ret[self._json_resources_key]:
            ret = self.get(x[self._json_resource_key]['name'])
            for k, v in kwargs.items():
                if getattr(ret, k, None) != v:
                    break
            else:
                yield ret
