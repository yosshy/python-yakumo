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
Abstract classes for resource management
"""

import copy
import inspect
import time

from . import constant
from . import exception
from . import mapper
from . import utils


WRAPPER_METHODS = []
BAD_ATTRS = ['self']


class Resource(object):
    """Base class for resources."""

    _id = None
    _attrs = []
    _loaded = True
    _sub_manager_list = {}
    _state_attr = 'status'
    _stable_state = []

    def __init__(self, manager, *args, **kwargs):
        """
        Create a resource object

        Don't call this method directly; use Manager methods instead.

        @param manager: Manager object
        @type manager: yakumo.base.Manager
        @return: Resource object
        @rtype: yakumo.base.Resource
        """
        self._manager = manager
        self._attr2json = manager._attr2json
        self._client = manager._client
        self._has_extra_attr = manager._has_extra_attr
        self._http = manager._http
        self._id_attr = manager._id_attr
        self._json2attr = manager._json2attr
        self._json_resource_key = manager._json_resource_key
        self._no_such_api = manager._no_such_api
        self._update_method = manager._update_method
        self._url_resource_path = manager._url_resource_path
        self._verbose = manager._verbose

        id = kwargs.get(self._id_attr)
        if isinstance(id, Resource):
            self._id = id._id
        else:
            self._id = id
        self._attrs = [attr
                       for attr, json_attr, _mapper
                       in manager._attr_mapping]
        self._set_attrs(kwargs)
        if len(kwargs) == 1 and self._id_attr in kwargs:
            self._loaded = False
        if len(kwargs) >= 1 and self._id_attr in kwargs:
            for attr, sub_manager in self._sub_manager_list.items():
                setattr(self, attr,
                        sub_manager(self, *args, **kwargs))

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        try:
            self.delete()
            self.wait_for_finished()
        except:
            pass

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return False
        return self._id == other._id

    def __ne__(self, other):
        if not isinstance(other, Resource):
            return True
        return self._id != other._id

    def __repr__(self):
        if 'name' in self._attrs and self._id_attr != 'name' and self._loaded:
            return '<%s.%s (%s="%s", name="%s")>' % (
                self.__module__, self.__class__.__name__, self._id_attr,
                self._id, self.name)
        empty = ''
        if not self._loaded:
            empty = ' empty'
        return '<%s.%s (%s="%s"%s)>' % (
            self.__module__, self.__class__.__name__, self._id_attr,
            self._id, empty)

    def __str__(self):
        if self._verbose:
            attrs = self.get_attrs()
            return '<%s.%s (%s)>' % (
                self.__module__, self.__class__.__name__, attrs)
        else:
            return self.__repr__()

    def __getattr__(self, name):
        if not self._has_extra_attr and name not in self._attrs:
            raise AttributeError(name)
        if name == self._id_attr:
            return self._id
        if not self._loaded:
            self.reload()
            return self.__dict__.get(name)
        return None

    def _set_attrs(self, kwargs):
        _kwargs = copy.copy(kwargs)
        for attr in self._attrs:
            if attr in _kwargs:
                setattr(self, attr, _kwargs.pop(attr))
        if not self._has_extra_attr:
            return
        for key, value in _kwargs.items():
            if not key.startswith('_') and key not in BAD_ATTRS:
                setattr(self, key, value)

    def _clear_attrs(self):
        """
        Clear attributes

        @rtype: None
        """
        ret = {}
        if not self._loaded:
            return
        for key in dir(self):
            if key.startswith('_'):
                continue
            if key in self._sub_manager_list:
                continue
            value = getattr(self, key)
            if inspect.ismethod(value) or inspect.isfunction(value):
                continue
            delattr(self, key)

    def get_id(self):
        """
        Query ID of a resource

        @return: ID
        @rtype: str
        """
        return self._id

    def get_attrs(self):
        """
        Aquire attributes as a dictionary

        @return: attributes
        @rtype: dict
        """
        ret = {}
        if not self._loaded:
            self.reload()
            self._loaded = True
        for key in dir(self):
            if key.startswith('_'):
                continue
            value = getattr(self, key)
            if inspect.ismethod(value) or inspect.isfunction(value):
                continue
            ret[key] = value
        return ret

    def reload(self):
        """
        (Re)load attributes of a resource

        @return: Whether attributes are updated
        @rtype: bool
        """
        x = self._manager.get(getattr(self, self._id_attr))
        if x:
            self._clear_attrs()
            self._set_attrs(x.__dict__)
            self._loaded = True
            return True
        return False

    def update(self, **kwargs):
        """
        Update a resource and reload it.
        kwargs: attributes and their values to update

        @rtype: None
        """
        json_params = self._attr2json(kwargs)
        method = getattr(self._http, self._update_method)
        method(utils.join_path(self._url_resource_path, self._id),
               data={self._json_resource_key: json_params})
        self.reload()

    def delete(self):
        """
        Delete a resource

        @rtype: None
        """
        self._http.delete(utils.join_path(self._url_resource_path, self._id))

    def wait_for_finished(self, count=10, interval=10):
        """
        Wait for task finished

        @keyword count: Maximum polling time
        @type count: int
        @keyword interval: Polling interval in seconds
        @type interval: int
        @rtype: None
        """
        if self._stable_state == []:
            return
        for i in range(count):
            time.sleep(interval)
            try:
                self.reload()
            except exception.NotFound:
                return
            if getattr(self, self._state_attr, None) in self._stable_state:
                return


class Manager(object):
    """Base class for resource managers."""

    resource_class = None
    service_type = ''
    _attr_mapping = []
    _has_detail = True
    _has_extra_attr = False
    _hidden_methods = None
    _json_resource_key = ''
    _json_resources_key = ''
    _id_attr = 'id'
    _update_method = 'put'
    _url_resource_path = ''
    _url_resource_list_path = ''

    def __init__(self, client, verbose=False, **kwargs):
        """
        Create a Manager object

        kwargs: options

        @param client: client object
        @type client: yakumo.Client
        @keyword verbose: Whether str(Resource) displays all attributes
        @type verbose: bool
        @return: Manager object
        @rtype: yakumo.base.Manager
        """
        self._client = client
        self._session = client._session
        self._http = self._session.get_proxy(self.service_type)
        self._to_json_mapping = {}
        self._to_attr_mapping = {}
        self._verbose = verbose
        if not self._url_resource_list_path:
            self._url_resource_list_path = self._url_resource_path
        if self.resource_class is None:
            return
        mapper.make_mappings(self._attr_mapping,
                             self._to_json_mapping,
                             self._to_attr_mapping)
        if self._hidden_methods is not None:
            for method in self._hidden_methods:
                setattr(self, method, self._no_such_api)

    def _no_such_api(self, *args):
        raise exception.NoSuchAPI()

    def _json2attr(self, json_params):
        result = {}
        for key, value in json_params.items():
            _map = self._to_attr_mapping.get(key)
            if _map is not None:
                result[_map['attr']] = _map['mapper'].to_attr(self, value)
            elif self._has_extra_attr and \
                    not key.startswith('_') and key not in BAD_ATTRS:
                result[key] = value
        return result

    def _attr2json(self, attrs):
        result = {}
        for key, value in attrs.items():
            if value is constant.UNDEF:
                continue
            _map = self._to_json_mapping.get(key)
            if _map is not None:
                result[_map['json_attr']] = \
                    _map['mapper'].to_json(self, value)
            elif self._has_extra_attr \
                    and not key.startswith('_') and key not in BAD_ATTRS:
                result[key] = value
        return result

    def get_empty(self, id):
        """
        Create a resource object without attributes

        @return: Resource object (empty)
        @rtype: yakumo.base.Resource
        """
        if id is None:
            return None
        kwargs = {self._id_attr: id}
        return self.resource_class(self, **kwargs)

    def create(self, **kwargs):
        """
        Create a new resource

        kwargs: attributes of the resource

        @return: Resource object (empty)
        @rtype: yakumo.base.Resource
        """
        json_params = self._attr2json(kwargs)
        ret = self._http.post(self._url_resource_path,
                              data={self._json_resource_key: json_params})
        attrs = self._json2attr(ret[self._json_resource_key])
        return self.get_empty(attrs[self._id_attr])

    def get(self, id):
        """
        Aquire an existing resource object

        @param id: ID
        @type id: str
        @return: Resource object
        @rtype: yakumo.base.Resource
        """
        try:
            ret = self._http.get(utils.join_path(self._url_resource_path, id))
            json_params = ret.get(self._json_resource_key)
            attrs = self._json2attr(json_params)
            return self.resource_class(self, **attrs)
        except exception.NotFound:
            raise
        except:
            return None

    def _find_gen(self, **kwargs):
        if self._has_detail:
            ret = self._http.get(self._url_resource_list_path)
            for x in ret[self._json_resources_key]:
                attrs = self._json2attr(x)
                for k, v in kwargs.items():
                    if attrs.get(k) != v:
                        break
                else:
                    yield self.resource_class(self, **attrs)
        else:
            try:
                ret = self._http.get(self._url_resource_list_path)
            except:
                return
            for x in ret[self._json_resources_key]:
                ret = self.get(x['id'])
                for k, v in kwargs.items():
                    if getattr(ret, k, None) != v:
                        break
                else:
                    yield ret

    def find(self, **kwargs):
        """
        Query existing resource object matched the conditions

        kwargs is key=value style query conditions.
        Returns empty list if no matched resource.

        @return: List of Resource object
        @rtype: yakumo.base.Resource
        """
        return list(self._find_gen(**kwargs))

    def find_one(self, **kwargs):
        """
        Aquire an existing resource object matched the conditions

        kwargs is key=value style query conditions.
        Returns None if no matched resource.

        @return: Resource object
        @rtype: yakumo.base.Resource
        """
        try:
            return self._find_gen(**kwargs).next()
        except StopIteration:
            return None

    def list(self):
        """
        Aquire an existing resource object

        @return: List of Resource objects
        @rtype: [yakumo.base.Resource]
        """
        return self.find()


class SubManager(Manager):
    """Base class for sub resource managers."""

    def __init__(self, parent_resource, *args, **kwargs):
        self.parent_resource = parent_resource
        try:
            self._url_resource_path = \
                self._url_resource_path % self.parent_resource._id
        except TypeError:
            pass
        super(SubManager, self).__init__(
            self.parent_resource._manager._client, *args, **kwargs)


class GlanceV2Resource(Resource):
    """Base class for resource managers which don't use _json_resource_key."""

    def update(self, **kwargs):
        """
        Update a resource and reload it.
        kwargs: attributes and their values to update

        @rtype: None
        """
        json_params = self._attr2json(kwargs)
        self._http.put(utils.join_path(self._url_resource_path, self._id),
                       data=json_params)


class GlanceV2Manager(Manager):
    """Base class for resource managers which don't use _json_resource_key."""

    _has_extra_attr = True

    def create(self, **kwargs):
        """
        Create a new resource

        kwargs: attributes of the resource

        @return: Resource object (empty)
        @rtype: yakumo.base.Resource
        """
        json_params = self._attr2json(kwargs)
        ret = self._http.post(self._url_resource_path, data=json_params)
        attrs = self._json2attr(ret)
        return self.get_empty(attrs[self._id_attr])

    def get(self, id):
        """
        Aquire an existing resource object

        @param id: ID
        @type id: str
        @return: Resource object
        @rtype: yakumo.base.Resource
        """
        try:
            json_params = self._http.get(
                utils.join_path(self._url_resource_path, id))
            attrs = self._json2attr(json_params)
            return self.resource_class(self, **attrs)
        except exception.NotFound:
            raise
        except:
            return None


class GlanceV2SubManager(SubManager, GlanceV2Manager):
    """Base class for sub resource managers for GlanceV2Manager."""
    pass
