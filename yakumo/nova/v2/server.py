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
Resource class and its manager for servers in Compute API v2
"""

import time

from yakumo import base
from yakumo.constant import UNDEF
from yakumo import exception
from yakumo import mapper
from yakumo import utils
from . import volume_attachment
from . import interface_attachment
from yakumo.neutron.v2.network import Resource as Network
from yakumo.neutron.v2.port import Resource as Port
from yakumo.cinder.v2.volume import Resource as Volume
from yakumo.cinder.v2.snapshot import Resource as Snapshot
from yakumo.glance.v2.image import Resource as Image


ATTRIBUTE_MAPPING = [
    ('id', 'id', mapper.Noop),
    ('name', 'name', mapper.Noop),
    ('access_ipv4', 'accessIPv4', mapper.Noop),
    ('access_ipv6', 'accessIPv6', mapper.Noop),
    ('addresses', 'addresses', mapper.Noop),
    ('host', 'OS-EXT-SRV-ATTR:host', mapper.Noop),
    ('networks', 'networks', mapper.Noop),
    ('disks', 'block_device_mapping_v2', mapper.Noop),
    ('user_data', 'user_data', mapper.Base64),
    ('progress', 'progress', mapper.Noop),
    ('status', 'status', mapper.Noop),
    ('task_state', 'OS-EXT-STS:task_state', mapper.Noop),
    ('created_at', 'created', mapper.DateTime),
    ('updated_at', 'updated', mapper.DateTime),
    ('metadata', 'metadata', mapper.Noop),
    ('flavor', 'flavorRef', mapper.Resource('nova.flavor')),
    ('image', 'imageRef', mapper.Resource('image')),
    ('project', 'tenant_id', mapper.Resource('project')),
    ('user', 'user_id', mapper.Resource('user')),
    ('key_pair', 'key_name', mapper.Resource('nova.key_pair')),
    ('error_reason', 'fault', mapper.Noop),
    ('availability_zone', 'availability_zone',
     mapper.Resource('nova.availability_zone')),
    ('availability_zone', 'OS-EXT-AZ:availability_zone',
     mapper.Resource('nova.availability_zone')),
]


class Resource(base.Resource):
    """Resource class for servers in Compute API v2"""

    _sub_manager_list = {
        'volume': volume_attachment.Manager,
        'interface': interface_attachment.Manager,
    }

    def wait_for_finished(self, count=10, interval=10):
        """
        Wait for task finished

        @keyword count: Maximum polling time
        @type count: int
        @keyword interval: Polling interval in seconds
        @type interval: int
        @rtype: None
        """
        for i in range(count):
            time.sleep(interval)
            try:
                self.reload()
            except exception.NotFound:
                return
            if not self.task_state:
                return

    def start(self):
        """
        Start a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-start"))

    def stop(self):
        """
        Stop a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("os-stop"))

    def reboot(self, force=False):
        """
        Reboot a server

        @keyword force: Whether reboot type is hard or soft. force=True means
        hard reboot.
        @type type: bool
        @rtype: None
        """
        if force:
            type = "HARD"
        else:
            type = "SOFT"
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("reboot", type=type))

    def pause(self):
        """
        Pause a server (save to RAM if server is a VM)

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("pause"))

    def unpause(self):
        """
        Unpause a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("unpause"))

    def suspend(self):
        """
        Suspend a server (save to disk if server is a VM)

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("suspend"))

    def resume(self):
        """
        Resume a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("resume"))

    def reset_network(self):
        """
        Reset networking of a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("resetNetwork"))

    def inject_network_info(self):
        """
        Inject network information to a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("injectNetworkInfo"))

    def lock(self):
        """
        Lock a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("lock"))

    def unlock(self):
        """
        Unlock a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("unlock"))

    def force_delete(self):
        """
        Force to delete a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("forceDelete"))

    def restore(self):
        """
        Restore a defered-deleted server if available

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("restore"))

    def rescue(self, password=None):
        """
        Create rescue environment for the server

        @keyword password: password of the rescue OS
        @type password: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("rescue", dminPass=password))

    def unrescue(self):
        """
        Terminate the rescue environment

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("unrescue"))

    def shelve(self):
        """
        Shelve a running server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("shelve"))

    def unshelve(self):
        """
        Restore a shelved server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("unshelve"))

    def delete_shelve(self):
        """
        Delete a shelved server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("shelveOffload"))

    def create_image(self, name=None, metadata=None):
        """
        Create server image

        @keyword name: Image name
        @type name: str
        @keyword metadata: Metadata
        @type metadata: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "createImage",
                            name=name,
                            metadata=metadata))

    def backup(self, name=None, backup_type=None, rotation=None):
        """
        Create server backup

        @keyword name: name of the backup data
        @type name: str
        @keyword backup_type: 'daily' or 'weekly'
        @type backup_type: str
        @keyword rotation: number of backups to maintain
        @type rotation: int
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "createBackup",
                            name=name,
                            backup_type=backup_type,
                            rotation=rotation))

    def live_migration(self, host=None, disk_over_commit=False):
        """
        Move a server to another host without rebooting

        @keyword host: Destination host
        @type host: str
        @keyword disk_over_commit: do disk over commit or not
        @type disk_over_commit: bool
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "os-migrateLive",
                            host=host,
                            block_migration=False,
                            disk_over_commit=disk_over_commit))

    def block_migration(self, host=None, disk_over_commit=False):
        """
        Move a server to another host without rebooting, with disk copy

        @keyword host: Destination host
        @type host: str
        @keyword disk_over_commit: do disk over commit or not
        @type disk_over_commit: bool
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "os-migrateLive",
                            host=host,
                            block_migration=True,
                            disk_over_commit=disk_over_commit))

    def evacuate(self, host=None, password=None, shared=True):
        """
        Move a server to another host without rebooting, with disk copy

        @keyword host: Destination host
        @type host: str
        @keyword password: new administrator password
        @type password: str
        @keyword shared: whether the vm is on the shared storage
        @type shared: bool
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "evacuate",
                            host=host,
                            adminPass=password,
                            onSharedStorage=shared))

    def reset_status(self, status=None):
        """
        Move a server to another host

        @keyword status: new status of the server ('active', 'pause', ...)
        @type status: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body(
                            "os-resetState", state=status))

    def get_vnc_console(self, type='novnc'):
        """
        Get VNC console

        @keyword type: 'novnc' or 'xvpvnc' (required)
        @type type: str
        @return: Console information
        @rtype: dict
        """
        ret = self._http.post(self._url_resource_path, self._id, 'action',
                              data=utils.get_json_body(
                                  "os-getVNCConsole",
                                  type=type))
        return ret.get('console')

    def get_console_log(self, lines=50):
        """
        Get console output

        @keyword lines: number of lines
        @type lines: int
        @return: Console logs
        @rtype: dict
        """
        ret = self._http.post(self._url_resource_path, self._id, 'action',
                              data=utils.get_json_body(
                                  "os-getConsoleOutput",
                                  length=lines))
        return ret.get('output')

    def get_diagnostics(self):
        """
        Get diagnostics

        @return: Diagnostics
        @rtype: dict
        """
        return self._http.get(self._url_resource_path, self._id, 'diagnostics')

    def resize(self, flavor=None, disk_config='AUTO'):
        """
        Get console output

        @keyword flavor: Flavor (required)
        @type flavor: yakumo.nova.v2.flavor.Resource
        @keyword disk_config: disk configuration ('AUTO')
        @type disk_config: str
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data={"resize": {
                            "flavorRef": flavor.id,
                            "OS-DCF:diskConfig": disk_config}})

    def confirm_resize(self):
        """
        Confirm resizing of a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("confirmResize"))

    def revert_resize(self):
        """
        Revert resizing of a server

        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'action',
                        data=utils.get_json_body("revertResize"))

    def rebuild(self, image=None, disk_config='AUTO', password=None,
                ipv4=None, ipv6=None, personality=None):
        """
        Rebuild a server

        @keyword image: Image
        @type image: yakumo.image.Resource
        @keyword disk_config: disk configuration ('AUTO')
        @type disk_config: str
        @keyword password: admin password
        @type password: str
        @keyword ipv4: IPv4 address
        @type ipv4: str
        @keyword ipv6: IPv6 address
        @type ipv6: str
        @keyword persoality: personality data
        @type persoality: [str]

        @rtype: None
        """
        json_body = utils.get_json_body(
            "rebuild",
            imageRef=image.id,
            adminPass=password,
            accessIPv4=ipv4,
            accessIPv6=ipv6,
            personality=personality)
        if disk_config is not None:
            json_body['rebuild']['OS-DCF:diskConfig'] = disk_config

        self._http.post(self._url_resource_path, self._id, 'action',
                        data=json_body)

    def get_actions(self):
        """
        Get instance actions

        @rtype: dict
        """
        ret = self._http.get(self._url_resource_path, self._id,
                             'os-instance-actions')
        return ret.get("instanceActions")

    def get_password(self):
        """
        Get instance password

        @rtype: dict
        """
        ret = self._http.get(self._url_resource_path, self._id,
                             'os-server-password')
        return ret.get("password")

    def clear_password(self):
        """
        Clear instance password

        @rtype: None
        """
        self._http.delete(self._url_resource_path, self._id,
                          'os-server-password')

    def get_security_groups(self):
        """
        Get security group list for a server

        @return: Security group list
        @rtype: [str]
        """
        ret = self._http.get(self._url_resource_path, self._id,
                             'os-security-groups')
        return [self._client.security_group_nova.
                get_empty(x.get('id'))
                for x in ret.get('security_groups', [])]

    def get_metadata(self):
        """
        Get instance metadata

        @return: Metadata
        @rtype: dict
        """
        ret = self._http.get(self._url_resource_path, self._id, 'metadata')
        return ret.get('metadata')

    def set_metadata(self, **metadata):
        """
        Update instance metadata

        @keyword metadata: key=value style.
        @type metadata: dict
        @rtype: None
        """
        self._http.post(self._url_resource_path, self._id, 'metadata',
                        data={'metadata': metadata})
        self.reload()

    def unset_metadata(self, *keys):
        """
        Delete instance metadata

        @param key: key of the metadata
        @type keys: [str]
        @rtype: None
        """
        for key in keys:
            self._http.delete(self._url_resource_path, self._id,
                              'metadata', key)
        self.reload()


class Manager(base.Manager):
    """Manager class for servers in Compute API v2"""

    resource_class = Resource
    service_type = 'compute'
    _attr_mapping = ATTRIBUTE_MAPPING
    _hidden_methods = ["update"]
    _json_resource_key = 'server'
    _json_resources_key = 'servers'
    _url_resource_path = '/servers'
    _url_resource_list_path = '/servers/detail'

    def _json2attr(self, json_params):
        flavor_id = json_params.pop('flavor', {}).get('id')
        ret = super(Manager, self)._json2attr(json_params)
        if flavor_id:
            ret['flavor'] = self._client.flavor.get_empty(flavor_id)
        return ret

    def create(self, name=UNDEF, image=UNDEF, flavor=UNDEF,
               personality=UNDEF, disks=UNDEF, max_count=UNDEF,
               min_count=UNDEF, networks=UNDEF, security_groups=UNDEF,
               availability_zone=UNDEF, metadata=UNDEF,
               config_drive=UNDEF, key_pair=UNDEF, user_data=UNDEF):
        """Create a new server

        @keyword name: name of the new server (required)
        @type name: str
        @keyword flavor: Flavor object to use (required)
        @type flavor: yakumo.nova.v2.flavor.Resource
        @keyword image: Image object to use for ephemeral disk
        @type image: yakumo.image.Resource
        @keyword key_pair: KeyPair object to use
        @type key_pair: yakumo.nova.v2.key_pair.Resource
        @keyword networks: list of networks or ones with tag and/or fixed IP
        @type networks: [yakumo.network.Resource]
        @keyword security_groups: list of SecurityGroup object(s) to use
        @type security_groups: [yakumo.nova.v2.security_group.Resource]
        @keyword disks: block device mapping
        @type disks: [dict]
        @keyword personality: file path and the content to embed
        @type personality: dict
        @keyword max_count: the maximum number of server(s) to create
        @type max_count: int
        @keyword min_count: the minimun number of server(s) to create
        @type min_count: int
        @keyword availability_zone: Availability Zone
        @type availability_zone: yakumo.availability_zone.Resource
        @keyword metadata: Metadata
        @type metadata: dict
        @keyword config_drive: config drive exists or not (bool)
        @type config_drive: bool
        @keyword user_data: content of a batch file (str)
        @type user_data: str
        @return: Created server
        @rtype: yakumo.nova.v2.server.Resource
        """
        if networks == UNDEF:
            networks = []
        if disks == UNDEF:
            disks = []
        _networks = []
        for net in networks:
            _network = {}
            if isinstance(net, dict):
                if 'tag' in net:
                    _network['tag'] = net['tag']
                if 'fixed_ip' in net:
                    _network['fixed_ip'] = net['fixed_ip']
                net = net.get('network', net.get('port'))
            if isinstance(net, Network):
                _network['uuid'] = net.get_id()
            if isinstance(net, Port):
                _network['port'] = net.get_id()
            _networks.append(_network)

        _disks = []
        boot_index = 0
        for disk in disks:
            _disk = {}
            if 'tag' in disk:
                _disk['tag'] = disk['tag']
            if 'size' in disk:
                _disk['volume_size'] = disk['size']
            if 'source' in disk:
                _disk['uuid'] = disk['source'].get_id()
                if isinstance(disk['source'], Volume):
                    _disk['source_type'] = 'volume'
                    _disk['destination_type'] = 'volume'
                elif isinstance(disk['source'], Snapshot):
                    _disk['source_type'] = 'snapshot'
                    _disk['destination_type'] = 'volume'
                elif isinstance(disk['source'], Image):
                    _disk['source_type'] = 'image'
                    _disk['destination_type'] = \
                        disk.get('destination_type', 'volume')
            else:
                _disk['source_type'] = 'blank'
                _disk['destination_type'] = \
                    disk.get('destination_type', 'volume')
            if 'delete_on_termination' in disk:
                _disk['delete_on_termination'] = \
                    disk['delete_on_termination']
            if 'guest_format' in disk:
                _disk['guest_format'] = disk['guest_format']
            _disk['boot_index'] = boot_index
            _disks.append(_disk)
            boot_index += 1

        return super(Manager, self).create(name=name, image=image,
                                           flavor=flavor,
                                           personality=personality,
                                           disks=_disks,
                                           max_count=max_count,
                                           min_count=min_count,
                                           networks=_networks,
                                           security_groups=security_groups,
                                           availability_zone=availability_zone,
                                           config_drive=config_drive,
                                           key_pair=key_pair,
                                           metadata=metadata,
                                           user_data=user_data)
