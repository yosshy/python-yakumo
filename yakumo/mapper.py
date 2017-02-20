# Copyright 2014-2017 by Akira Yoshiyama <akirayoshiyama@gmail.com>.
# All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""
Mapper classes
"""

import base64
import json
from datetime import datetime
import dateutil.parser


def make_mappings(source, to_json, to_attr):
    for attr, json_attr, _mapper in source:
        if isinstance(attr, str):
            if attr not in to_json:
                to_json[attr] = {
                    'json_attr': json_attr,
                    'mapper': _mapper,
                }
        if isinstance(json_attr, str):
            to_attr[json_attr] = {
                'attr': attr,
                'mapper': _mapper,
            }


class NoopClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        return attr

    @staticmethod
    def to_json(manager_class, attr):
        return attr


class IntStrClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        return int(attr)

    @staticmethod
    def to_json(manager_class, attr):
        return str(attr)


class StrIntClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        return str(attr)

    @staticmethod
    def to_json(manager_class, attr):
        return int(attr)


class FloatStrClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        return float(attr)

    @staticmethod
    def to_json(manager_class, attr):
        return str(attr)


class BoolStrClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        if attr.lower() == 'true':
            return True
        if attr.lower() == 'false':
            return False
        return None

    @staticmethod
    def to_json(manager_class, attr):
        if attr is True:
            return 'true'
        if attr is False:
            return 'false'
        return None


class JSONClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        return json.loads(attr)

    @staticmethod
    def to_json(manager_class, attr):
        return json.dumps(attr)


class Base64(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        return base64.b64decode(attr)

    @staticmethod
    def to_json(manager_class, attr):
        return base64.b64encode(attr)


class DateTimeClass(object):

    @staticmethod
    def to_attr(manager_class, attr, do_raise=False):
        try:
            return dateutil.parser.parse(attr)
        except:
            return None

    @staticmethod
    def to_json(manager_class, attr):
        try:
            return datetime.isoformat(attr)
        except:
            return None


class Simple(object):

    def __init__(self, mapping):
        self.mapping = mapping

    def to_attr(self, manager_class, value, do_raise=False):
        for obj_value, json_value in self.mapping:
            if json_value == value:
                return obj_value

    def to_json(self, manager_class, value):
        for obj_value, json_value in self.mapping:
            if obj_value == value:
                return json_value


class Resource(object):

    manager_class = None

    def __init__(self, manager_path):
        self.manager_path = manager_path

    def _load_manager_class(self, manager_class):
        if self.manager_class:
            return
        resource = manager_class._client
        for path in self.manager_path.split('.'):
            resource = getattr(resource, path)
        self.manager_class = resource

    def to_attr(self, manager_class, id, do_raise=False):
        if id is None:
            return None
        self._load_manager_class(manager_class)
        return self.manager_class.get_empty(id)

    def to_json(self, manager_class, obj):
        if obj is None:
            return None
        self._load_manager_class(manager_class)
        return obj._id


class List(object):

    mapper = None

    def __init__(self, mapper):
        self.mapper = mapper

    def to_attr(self, manager_class, attr, do_raise=False):
        return [self.mapper.to_attr(manager_class, x) for x in attr]

    def to_json(self, manager_class, attr):
        return [self.mapper.to_json(manager_class, x) for x in attr]


class Dict(object):

    mappers = None

    def __init__(self, mappers):
        # mappers has list like below
        # [('subnet', 'subnet_ip', mapper.Resource('subnet')),
        #  ('ip_address', 'ip_address', mapper.Noop)}]
        self.mappers = mappers

    def to_attr(self, manager_class, attr, do_raise=False):
        if attr is None:
            return {}
        ret = {}
        for _attr, _json, mapper in self.mappers:
            if _json in attr:
                ret[_attr] = mapper.to_attr(manager_class, attr[_json])
        return ret

    def to_json(self, manager_class, attr):
        if attr is None:
            return {}
        converted = []
        ret = {}
        for _attr, _json, mapper in self.mappers:
            if _attr in attr and _attr not in converted:
                converted.append(_attr)
                ret[_json] = mapper.to_json(manager_class, attr[_attr])
        return ret


Noop = NoopClass()
IntStr = IntStrClass()
StrInt = StrIntClass()
FloatStr = FloatStrClass()
BoolStr = BoolStrClass()
JSON = JSONClass()
DateTime = DateTimeClass()
