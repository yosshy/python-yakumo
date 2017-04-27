Yakumo - Pythonic, Unified OpenStack Client Library
===================================================

Each OpenStack client library like python-novaclient can handle only one OpenStack program, so we have to use multiple client libraries/commands to use OpenStack platform.
Yakumo is a pythonic, unified OpenStack client library. Its basic usage is a bit similar to python-novaclient and others, but it can handle multiple programs (Nova, Swift Glance, Cinder, Neutron and Keystone now) and it's easy to manage multiple resources on the multiple programs with it.

Yes, there is another unified OpenStack client library named 'python-openstacksdk'. But its API style is different from python-novaclient and others. That is the reason I started Yakumo development by myself.

## Basic Usage

Yakumo contains a simple sample OpenStack shell named 'ossh'. For example,
```
bash$ ossh --os-cloud=packstack --verbose
>>>
Welcome to bpython! Press <F1> for help.
```
'c' is a client object defined in ossh, using credential information from environment variables. Of course, you can define another client object by yourself. See ossh source code for details.

ossh has code completion capability of bpython if available. Type "c.":
```
>>> c.
+------------------------------------------------------------------------------------------+
| aggregate                     availability_zone             cinder                       |
| cloudpipe                     consistency_group             consistency_group_snapshot   |
| container                     credential                    domain                       |
| endpoint                      fixed_ip                      flavor                       |
| floating_ip                   floating_ip_bulk              floating_ip_dns              |
| glance                        group                         hypervisor                   |
| image                         key_pair                      keystone                     |
| lb                            lbaas                         network                      |
| network_quota                 neutron                       nova                         |
| port                          project                       region                       |
| role                          router                        security_group               |
| security_group_default_rule   server                        server_group                 |
| service                       subnet                        subnet_pool                  |
| swift                         user                          volume                       |
| volume_backup                 volume_snapshot               volume_transfer              |
| volume_type                   volume_type_qos               vpn                          |
+------------------------------------------------------------------------------------------+
```

You can also use built-in completion capability without bpython. Type "c.<tab><tab>":
```
>>> c.
c.aggregate                    c.image                        c.server
c.availability_zone            c.key_pair                     c.server_group
c.cinder                       c.keystone                     c.service
c.cloudpipe                    c.lb                           c.subnet
c.consistency_group            c.lbaas                        c.subnet_pool
c.consistency_group_snapshot   c.network                      c.swift
c.container                    c.network_quota                c.user
c.endpoint                     c.neutron                      c.volume
c.fixed_ip                     c.nova                         c.volume_backup
c.flavor                       c.port                         c.volume_snapshot
c.floating_ip                  c.project                      c.volume_transfer
c.floating_ip_bulk             c.role                         c.volume_type
c.floating_ip_dns              c.router                       c.volume_type_qos
c.glance                       c.security_group               c.vpn
c.hypervisor                   c.security_group_default_rule
```

c.CATEGORY.list() returns a list of resource objects:
```
>>> c.image.list()
[<yakumo.glance.v2.image.Resource (id="887b0393-5065-4bcf-941d-623100baa06e", name="trusty")>]
>>>
```
c.CATEGORY.find(cond) returns a list of resource objects matched to cond:
```
>>> c.flavor.find(vcpus=1)
[<yakumo.nova.v2.flavor.Resource (id="1", name="m1.tiny")>, <yakumo.nova.v2.flavor.Resource (id="2", name="m1.small")>]
>>>
```
c.CATEGORY.find_one(cond) returns a resource object matched to cond:
```
>>> i = c.image.find_one(name="trusty")
>>> f = c.flavor.find_one(name='m1.small')
>>> k = c.key_pair.find_one(name='key1')
>>> n = c.network.find_one(name='private')
>>> i, f, k, n
(<yakumo.glance.v2.image.Resource (id="887b0393-5065-4bcf-941d-623100baa06e", name="trusty")>, <yakumo.nova.v2.flavor.Resource (id="2"
, name="m1.small")>, <yakumo.nova.v2.key_pair.Resource (name="key1")>, <yakumo.neutron.v2.network.Resource (id="22e3fa30-11c0-4065-bbf
7-8d8bbb50f63b", name="private")>)
>>>
```
pprint() is useful. It's already imported
```
>>> pprint((i, f, k, n))
(<yakumo.glance.v2.image.Resource (id="887b0393-5065-4bcf-941d-623100baa06e", name="trusty")>,
 <yakumo.nova.v2.flavor.Resource (id="2", name="m1.small")>,
 <yakumo.nova.v2.key_pair.Resource (name="key1")>,
 <yakumo.neutron.v2.network.Resource (id="22e3fa30-11c0-4065-bbf7-8d8bbb50f63b", name="private")>)
>>>
```
get_attrs() method returns all attribute.
```
>>> pprint(f.get_attrs())
{'disk': 20,
 'ephemeral': 0,
 'id': u'2',
 'is_public': True,
 'name': u'm1.small',
 'ram': 2048,
 'rxtx_factor': 1.0,
 'swap': u'',
 'vcpus': 1}
>>>
```
You can see description of a method:
```
>>> c.server.create(
+--------------------------------------------------------------------------------------------------------------+
| c.server.create: (self, name=None, image=None, flavor=None, personality=None, block_devices=None,            |
| max_count=None, min_count=None, networks=None, security_groups=None, config_drive=False, key_pair=None,      |
| user_data=None)                                                                                              |
| create                                                                                                       |
| Create a new server                                                                                          |
|                                                                                                              |
| @keyword name: name of the new server (required)                                                             |
| @type name: str                                                                                              |
| @keyword flavor: Flavor object to use (required)                                                             |
| @type flavor: yakumo.nova.v2.flavor.Resource                                                                 |
| @keyword image: Image object to use for ephemeral disk                                                       |
| @type image: yakumo.image.Resource                                                                           |
| @keyword key_pair: KeyPair object to use                                                                     |
| @type key_pair: yakumo.nova.v2.key_pair.Resource                                                             |
| @keyword networks: list of networks or ones with tag and/or fixed IP                                         |
| @type networks: [yakumo.network.Resource]                                                                    |
| @keyword security_groups: list of SecurityGroup object(s) to use                                             |
| @type security_groups: [yakumo.nova.v2.security_group.Resource]                                              |
| @keyword block_devices: block device mapping                                                                 |
| @type block_devices: [dict]                                                                                  |
| @keyword personality: file path and the content to embed                                                     |
| @type personality: dict                                                                                      |
| @keyword max_count: the maximum number of server(s) to create                                                |
| @type max_count: int                                                                                         |
| @keyword min_count: the minimun number of server(s) to create                                                |
| @type min_count: int                                                                                         |
| @keyword config_drive: config drive exists or not (bool)                                                     |
| @type config_drive: bool                                                                                     |
| @keyword user_data: content of a batch file (str)                                                            |
| @type user_data: str                                                                                         |
| @return: Created server                                                                                      |
| @rtype: yakumo.nova.v2.server.Resource                                                                       |
+--------------------------------------------------------------------------------------------------------------+
```
You can create a new resource:
```
>>> s = c.server.create(name='vm1', image=i, flavor=f, networks=[n], key_pair=k)
>>> s
<yakumo.nova.v2.server.Resource (id="b1477f6c-bbc4-4c37-ba05-14b935a5d08c" empty)>
>>>
```
's' is an empty resource object for the new instance. "empty" means the object has only ID attribute. Other attributes will be loaded on-demand. For example, "print(s)" causes loading attributes.
```
>>> print(s)
<yakumo.nova.v2.server.Resource ({'status': u'BUILD', 'addresses': {u'private': [{u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:0a:73:d3', u'version': 4, u'addr': u'10.0.0.10', u'OS-EXT-IPS:type': u'fixed'}]}, 'access_ipv4': u'', 'created_at': datetime.datetime(2017, 2, 10, 3, 24, 22, tzinfo=tzutc()), 'updated_at': datetime.datetime(2017, 2, 10, 3, 24, 31, tzinfo=tzutc()), 'name': u'vm1', 'project': <yakumo.keystone.v2.project.Resource (id="68b7f45b07084546a089e75b29efae29" empty)>, 'host': <yakumo.nova.v2.host.Resource (name="packstack3" empty)>, 'key_pair': <yakumo.nova.v2.key_pair.Resource (name="key1" empty)>, 'user': <yakumo.keystone.v2.user.Resource (id="99605955005446c386a4c9bce4eaa7a1" empty)>, 'progress': 0, 'id': u'b1477f6c-bbc4-4c37-ba05-14b935a5d08c', 'access_ipv6': u''})>
>>>
```
Let's confirm the keypair.
```
>>> s.key_pair
<yakumo.nova.v2.key_pair.Resource (name="key1" empty)>
>>>
```
You can update the information of 's':
```
>>> s.reload()
>>>
```
Waiting server becomes active:
```
>>> s.wait_for_finished()
>>>
```
Let's confirm status of the new instance.
```
>>> s.status
u'ACTIVE'
>>>
```
get_id() method returns its ID.
```
>>> s.get_id()
u'b1477f6c-bbc4-4c37-ba05-14b935a5d08c'
>>>
```
You can create a new resource object directly if you have its ID.
```
>>> s2 = c.server.get('b1477f6c-bbc4-4c37-ba05-14b935a5d08c')
>>> s2
<yakumo.nova.v2.server.Resource (id="b1477f6c-bbc4-4c37-ba05-14b935a5d08c", name="vm1")>
>>>
```
You can check the two objects are the same:
```
>>> s == s2
True
>>>
```
and delete one:
```
>>> s.delete()
>>>
```
How about this?
```
>>> for i in c.server.list(): i.delete()
```
CAUTION: YOUR INSTANCES WILL BE DELETED IF YOU RUN ABOVE.

Yes, that's one of things I want to do.

## Author

Akira Yoshiyama / akirayoshiyama _at_ gmail.com

## Project URL

https://github.com/yosshy/python-yakumo

## License

Apache License Version 2.0

See LICENSE for more details.
