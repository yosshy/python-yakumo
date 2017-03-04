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
Resource class and its manager for consistency group on Block Storage V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('description', 'display_description', mapper.Noop),
    ('volume_types', 'volume__types',
     mapper.List(mapper.Resource('cinder.volume_type'))),
    ('availability_zone', 'availability_zone',
     mapper.Resource('availability_zone')),
    ('status', 'status', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
]


class Resource(base.Resource):
    """resource class for consistency group on Block Storage V2 API"""

    def update(self, name=UNDEF, description=UNDEF, add=UNDEF, remove=UNDEF):
        """
        Update properties of a consistency group

        @keyword name: Consistency group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword add: List of volumes to add
        @type add: [yakumo.cinder.v2.volume.Resource]
        @keyword remove: List of volumes to remove
        @type remove: [yakumo.cinder.v2.volume.Resource]
        @rtype: None
        """
        super(Resource, self).update(
            name=name,
            description=description,
            add=add,
            remove=remove)

    def delete(self, force=False):
        """
        Delete a consistency group

        @keyword force: Force delete
        @type force: boot
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'delete',
                        data=utils.get_json_body("consistencygroup",
                                                 force=force))


class Manager(base.Manager):
    """manager class for consistency group on Block Storage V2 API"""

    resource_class = Resource
    service_type = 'volume'
    _attr_mapping = ATTRIBUTE_MAPPING
    _json_resource_key = 'consistencygroup'
    _json_resources_key = 'consistencygroups'
    _url_resource_list_path = '/consistencygroups/detail'
    _url_resource_path = '/consistencygroups'

    def create(self, name=UNDEF, description=UNDEF, volume_types=UNDEF,
               availability_zone=False):
        """
        Create a consistency group

        @keyword name: Consistency group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword volume_types: List of volume types
        @type volume_types: [yakumo.cinder.v2.volume_type.Resource]
        @keyword availability_zone: Availability zone
        @type availability_zone: yakumo.availability_zone.Resource
        @return: Created volume object
        @rtype: yakumo.cinder.v2.consistency_group.Resource
        """
        return super(Manager, self).create(
            name=name,
            description=description,
            volume_types=volume_types,
            availability_zone=availability_zone)

    def copy(self, name=None, description=None, source_cg=None,
             source_cg_snapshot=None, project=None, user=None):
        """
        Create a consistency group from source

        @keyword name: Consistency group name
        @type name: str
        @keyword description: Description
        @type description: str
        @keyword source_cg: Source consistency group
        @type source_cg: yakumo.cinder.v2.consistency_group.Resource
        @keyword source_cg_snapshot: Source consistency group snapshot
        @type source_cg_snapshot:
        yakumo.cinder.v2.consistency_group_snapshot.Resource
        @keyword project: Project
        @type description: yakumo.project.Resource
        @keyword project: User
        @type description: yakumo.user.Resource
        @return: Copied volume object
        @rtype: yakumo.cinder.v2.consistency_group.Resource
        """
        ret = self._http.post(self._url_resource_path, self._id,
                              'create_from_src',
                              data=utils.get_json_body(
                                  "consistencygroup-from-src",
                                  name=name,
                                  description=description,
                                  cgsnapshot_id=source_cg_snapshot.get_id(),
                                  source_cgid=source_cg.get_id(),
                                  user_id=user.get_id(),
                                  project_id=project.get_id(),
                                  status=status))
        attrs = self._json2attr(ret)
        return self.get_empty(attrs[self._id_attr])
