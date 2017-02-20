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

import os_client_config as occ
import json

from . import exception
from . import utils


CHUNK_SIZE = 8192


def get_config(**kwargs):
    ret = occ.get_config(**kwargs)
    return ret.config


def get_rest_clients(**kwargs):
    rest_clients = {}
    cc = occ.get_config(**kwargs)
    for service in cc.get_services():
        try:
            rest_client = occ.make_rest_client(service, **kwargs)
            rest_client.get_endpoint()
            rest_clients[service] = rest_client
        except exception.EndpointNotFound:
            pass
    return rest_clients


class RestClient(object):
    def __init__(self, rest_clients, service_type):
        self.rest_clients = rest_clients
        self.service_type = service_type

    @staticmethod
    def json_body(kwargs):
        jsondata = json.dumps(kwargs.get('data', {}))
        kwargs['data'] = jsondata

    @staticmethod
    def make_headers(kwargs, content_type=None, accept='application/json'):
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

    def head(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        response = self.rest_clients[self.service_type].head(path, **kwargs)
        response.raise_for_status()
        return response.headers

    def get(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        response = self.rest_clients[self.service_type].get(path, **kwargs)
        response.raise_for_status()
        if len(response.content) > 0:
            return response.json()

    def patch(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        self.json_body(kwargs)
        response = self.rest_clients[self.service_type].patch(path, **kwargs)
        response.raise_for_status()
        if len(response.content) > 0:
            return response.json()

    def put(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        self.json_body(kwargs)
        response = self.rest_clients[self.service_type].put(path, **kwargs)
        response.raise_for_status()
        if len(response.content) > 0:
            return response.json()

    def post(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        self.json_body(kwargs)
        response = self.rest_clients[self.service_type].post(path, **kwargs)
        response.raise_for_status()
        if len(response.content) > 0:
            return response.json()

    def delete(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        response = self.rest_clients[self.service_type].delete(path, **kwargs)
        response.raise_for_status()

    def get_raw(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs)
        response = self.rest_clients[self.service_type].get(path, **kwargs)
        response.raise_for_status()
        return response.content

    def put_raw(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs, content_type="application/octet-stream")
        response = self.rest_clients[self.service_type].put(path, **kwargs)
        response.raise_for_status()
        if len(response.content) > 0:
            return response.json()

    def post_raw(self, *args, **kwargs):
        path = utils.join_path(*args)
        self.make_headers(kwargs, content_type="application/octet-stream")
        response = self.rest_clients[self.service_type].post(path, **kwargs)
        response.raise_for_status()
        if len(response.content) > 0:
            return response.json()

    def get_file(self, *args, **kwargs):
        path = utils.join_path(*args)
        file = kwargs.pop('file')
        response = self.rest_clients[self.service_type].\
            get(path, stream=True, **kwargs)
        response.raise_for_status()
        with open(file, 'wb') as f:
            for c in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(c)
                f.flush()
        return response.headers

    def put_file(self, *args, **kwargs):
        path = utils.join_path(*args)
        files = {'file': open(kwargs['file'], 'rb')}
        kwargs['files'] = files
        response = self.rest_clients[self.service_type].put(path, **kwargs)
        response.raise_for_status()

    def post_file(self, *args, **kwargs):
        path = utils.join_path(*args)
        files = {'file': open(kwargs['file'], 'rb')}
        kwargs['files'] = files
        response = self.rest_clients[self.service_type].post(path, **kwargs)
        response.raise_for_status()
