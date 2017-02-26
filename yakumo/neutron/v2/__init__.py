from . import floating_ip
from . import lb
from . import lbaas
from . import network
from . import port
from . import quota
from . import router
from . import security_group
from . import subnet
from . import subnet_pool
from . import vpn
from . import metering


class Client(object):

    def __init__(self, client, **kwargs):
        self.floating_ip = floating_ip.Manager(client, **kwargs)
        self.network = network.Manager(client, **kwargs)
        self.port = port.Manager(client, **kwargs)
        self.quota = quota.Manager(client, **kwargs)
        self.router = router.Manager(client, **kwargs)
        self.security_group = security_group.Manager(client, **kwargs)
        self.subnet = subnet.Manager(client, **kwargs)
        self.subnet_pool = subnet_pool.Manager(client, **kwargs)
        self.metering = metering.Client(client, **kwargs)
        self.lb = lb.Client(client, **kwargs)
        self.lbaas = lbaas.Client(client, **kwargs)
        self.vpn = vpn.Client(client, **kwargs)

        client.floating_ip = self.floating_ip
        client.network = self.network
        client.port = self.port
        client.network_quota = self.quota
        client.router = self.router
        client.security_group = self.security_group
        client.subnet = self.subnet
        client.subnet_pool = self.subnet_pool
        client.lb = self.lb
        client.lbaas = self.lbaas
        client.vpn = self.vpn
