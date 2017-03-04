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
Resource class and its manager for image members in Image V2 API
"""

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import mapper
from yakumo import utils


ATTRIBUTE_MAPPING = [
    ('user', 'member_id', mapper.Resource('user')),
    ('image', 'image_id', mapper.Resource('glance.image')),
    ('schema', 'schema', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('created_at', 'created_at', mapper.DateTime),
    ('updated_at', 'updated_at', mapper.DateTime),
]


class Resource(base.GlanceV2Resource):
    """resource class for image members on Image V2 API"""

    def update(self, status=UNDEF):
        """
        Update status of a member

        @keyword status: Member status
        ('accepted','pending','rejected',or 'all')
        @type status: str
        @rtype: None
        """
        return super(Resource, self).update(status=status)


class Manager(base.GlanceV2SubManager):
    """manager class for image membes on Image V2 API"""

    resource_class = Resource
    service_type = 'image'
    _attr_mapping = ATTRIBUTE_MAPPING
    _id_attr = 'user'
    _json_resources_key = 'members'
    _url_resource_path = '/v2/images/%s/members'

    def create(self, user=UNDEF):
        """
        Register a member for a image

        @keyword user: New user (required)
        @type user: yakumo.user.Resource
        @return: Registered image member
        @rtype: yakumo.glance.v2.image_member.Resource
        """
        ret = self._http.post(self._url_resource_path,
                              data=dict(member=user.get_id()))
        attrs = self._json2attr(ret)
        return self.get_empty(attrs.get(self._id_attr))
