#   Copyright 2014 Akira Yoshiyama
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
utility function(s) for session
"""
from contextlib import contextmanager
import functools
import json
import os
import os_client_config
from os_client_config import cloud_config
import random
import requests
from simplejson.scanner import JSONDecodeError

from . import exception
from . import patch
from . import utils


CHUNK_SIZE = 4096


# Patch it!
cloud_config.CloudConfig.get_session_endpoint = patch.get_session_endpoint


def get_session(**kwargs):
    """
    Session class dispatcher

    :return: Session class
    """
    config = os_client_config.OpenStackConfig()
    cloud_config = config.get_one_cloud(**kwargs)
    if cloud_config.config.get('insecure'):
        cloud_config.config['verify'] = False
        cloud_config.config['cacert'] = None
    if 'timeout' not in cloud_config.config:
        cloud_config.config['timeout'] = 600

    return Session(cloud_config)


class SessionProxy(object):

    def __init__(self, session, service):
        self.session = session
        self.service = service

    def has_endpoint(self, service):
        return self.session.has_endpoint(service)

    def get(self, *args, **kwargs):
        return self.session.get(self.service, *args, **kwargs)

    def head(self, *args, **kwargs):
        return self.session.head(self.service, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(self.service, *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.session.patch(self.service, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(self.service, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(self.service, *args, **kwargs)

    def get_raw(self, *args, **kwargs):
        return self.session.get_raw(self.service, *args, **kwargs)

    def post_raw(self, *args, **kwargs):
        return self.session.post_raw(self.service, *args, **kwargs)

    def put_raw(self, *args, **kwargs):
        return self.session.put_raw(self.service, *args, **kwargs)

    def get_file(self, *args, **kwargs):
        return self.session.get_file(self.service, *args, **kwargs)

    def post_file(self, *args, **kwargs):
        return self.session.post_file(self.service, *args, **kwargs)

    def put_file(self, *args, **kwargs):
        return self.session.put_file(self.service, *args, **kwargs)


def reauth(func):

    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except exception.NotFound:
            self.get_token()
            return func(self, *args, **kwargs)

    return _wrapper


def exception_translator(func):

    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except exception.HTTPError as e:
            raise exception.mapping[e.response.status_code]()

    return _wrapper


def safe_json_load(func):

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except JSONDecodeError:
            return None

    return _wrapper


class Session(object):

    def __init__(self, config):
        self.config = config.config
        self.keystone_session = config.get_session()
        self.get_token()
        self.endpoints = {}
        for service in config.get_services():
            try:
                self.endpoints[service] = config.get_session_endpoint(service)
            except:
                pass

    def has_endpoint(self, service):
        return service in self.endpoints

    def get_proxy(self, service):
        return SessionProxy(self, service)

    def get_token(self):
        self.token = self.keystone_session.get_token()

    @staticmethod
    def json_body(kwargs):
        jsondata = json.dumps(kwargs.get('data', {}))
        kwargs['data'] = jsondata

    def make_headers(self, kwargs, content_type=None,
                     accept='application/json'):
        kwargs.setdefault('headers', {})
        headers = kwargs['headers']
        if 'Content-Type' not in headers:
            if content_type:
                headers['Content-Type'] = content_type
            else:
                headers['Content-Type'] = "application/json; charset=UTF-8"
        if 'Accept' not in headers:
            headers['Accept'] = accept
        headers['Accept-Encoding'] = 'identity'
        headers['X-Auth-Token'] = self.token

    @reauth
    @exception_translator
    @safe_json_load
    def get(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    def head(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        response = requests.head(url, **kwargs)
        response.raise_for_status()
        return response.headers

    @reauth
    @exception_translator
    def delete(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        response = requests.delete(url, **kwargs)
        response.raise_for_status()

    @reauth
    @exception_translator
    @safe_json_load
    def patch(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        self.json_body(kwargs)
        response = requests.patch(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    @safe_json_load
    def post(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        self.json_body(kwargs)
        response = requests.post(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    @safe_json_load
    def put(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        self.json_body(kwargs)
        response = requests.put(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    def get_raw(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs)
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response.content

    @reauth
    @exception_translator
    @safe_json_load
    def post_raw(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs, content_type="application/octet-stream")
        response = requests.post(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    @safe_json_load
    def put_raw(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        self.make_headers(kwargs, content_type="application/octet-stream")
        response = requests.put(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    @safe_json_load
    def get_file(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        file = kwargs.pop('file')
        self.make_headers(kwargs)
        response = requests.get(url, stream=True, **kwargs)
        response.raise_for_status()
        with open(file, 'wb') as f:
            for c in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(c)
                f.flush()
        return response.headers

    @reauth
    @exception_translator
    @safe_json_load
    def post_file(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        with open(kwargs.pop('file'), 'rb') as f:
            kwargs['files'] = {'file': f}
            self.make_headers(kwargs)
            response = requests.post(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @reauth
    @exception_translator
    @safe_json_load
    def put_file(self, service, *args, **kwargs):
        url = utils.join_path(self.endpoints[service], *args)
        with open(kwargs.pop('file'), 'rb') as f:
            kwargs['files'] = {'file': f}
            self.make_headers(kwargs)
            response = requests.put(url, **kwargs)
        response.raise_for_status()
        return response.json()
