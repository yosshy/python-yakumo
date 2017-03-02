# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
# Copyright (c) 2017 Akira Yoshiyama
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


def get_session_endpoint(self, service_key):
        """Return the endpoint from config or the catalog.

        THIS IS FROM os_client_config.CloudConfig.get_session_endpoint()
        If a configuration lists an explicit endpoint for a service,
        return that. Otherwise, fetch the service catalog from the
        keystone session and return the appropriate endpoint.

        :param service_key: Generic key for service, such as 'compute' or
                            'network'

        :returns: Endpoint for the service, or None if not found
        """

        override_endpoint = self.get_endpoint(service_key)
        if override_endpoint:
            return override_endpoint
        # don't make keystone special
        session = self.get_session()
        args = {
            'service_type': self.get_service_type(service_key),
            'service_name': self.get_service_name(service_key),
            'interface': self.get_interface(service_key),
            'region_name': self.region
        }
        try:
            endpoint = session.get_endpoint(**args)
        except keystoneauth1.exceptions.catalog.EndpointNotFound:
            self.log.warning("Keystone catalog entry not found (%s)",
                             args)
            endpoint = None
        return endpoint
