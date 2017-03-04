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
Resource class and its manager for QoS specifications on Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('consumer', 'consumer', mapper.Noop),
]


class Resource(base.Resource):
    """resource class for QoS specifications on Block Storage V2 API"""

    _stable_state = ['available', 'error', 'error_deleting']

    def get_metadata(self):
        """
        Aquire specs of a QoS Specs

        @return: specs in key=value format
        @rtype: dict
        """
        return self.get_attrs()

    def set_metadata(self, **kwargs):
        """
        Add or update specs into a QoS specification

        name can't be altered.

        @keyword kwargs: key=value style specs
        @type kwargs: str=str
        @rtype: None
        """
        self.update(**kwargs)

    def unset_metadata(self, *keys):
        """
        Remove specs from a QoS specification

        @keyword keys: List of keys to be deleted
        @type keys: [str]
        @rtype: None
        """
        self._http.put(self._url_resource_path, self._id, 'delete_keys',
                       data={"keys": keys})
        self.reload()

    def get_associations(self):
        """
        Get associated volume types for a QoS specs

        @return: List of associated volume types
        @rtype: [yakumo.cinder.v2.volume_types.Resource]
        """
        volume_types = []
        ret = self._http.get(self._url_resource_path, self._id, 'associations')
        for vt in ret['qos_associations']:
            volume_types.append(
                self._client.cinder.volume_type.get_empty(vt['id']))
        return volume_types

    def associate(self, *volume_types):
        """
        Associate QoS specs with a volume type

        @param volume_type: Volume type to be associated
        @type volume_type: [yakumo.cinder.v2.volume_type.Resource]
        @rtype: None
        """
        for volume_type in volume_types:
            self._http.get(self._url_resource_path, self._id, 'associate',
                           params={'vol_type_id': volume_type.get_id()})
        self.reload()

    def disassociate(self, *volume_types):
        """
        Dissociate QoS specs from a volume type

        @param volume_type: Volume type to be dissociated
        @type volume_type: yakumo.cinder.v2.volume_type.Resource
        @rtype: None
        """
        for volume_type in volume_types:
            self._http.get(self._url_resource_path, self._id, 'disassociate',
                           params={'vol_type_id': volume_type.get_id()})
        self.reload()

    def disassociate_all(self):
        """
        Disassociate QoS specs from all associations

        @rtype: None
        """
        self._http.get(self._url_resource_path, self._id, 'disassociate_all')
        self.reload()


class Manager(base.Manager):
    """manager class for QoS specifications on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _has_extra_attr = True
    _json_resource_key = 'qos_specs'
    _json_resources_key = 'qos_specs'
    _url_resource_list_path = '/qos-specs'
    _url_resource_path = '/qos-specs'

    def _json2attr(self, kwargs):
        specs = kwargs.pop('specs')
        kwargs.update(specs)
        return super(Manager, self)._json2attr(kwargs)

    def create(self, name=UNDEF, consumer=UNDEF, **kwargs):
        """
        Create a snapshot of a volume

        @keyword name: QoS specification name
        @type name: str
        @keyword consumer: Consumer of the QoS specification
        @type consumer: str
        @keyword kwargs: key=value style spec
        @type kwargs: str=str
        @return: Created QoS specs
        @rtype: yakumo.cinder.v2.qos.Resource
        """
        return super(Manager, self).create(name=name,
                                           consumer=consumer,
                                           **kwargs)
