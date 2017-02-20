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

    def __init__(self, client, *args, **kwargs):
        self.floating_ip = floating_ip.Manager(client)
        self.network = network.Manager(client)
        self.port = port.Manager(client)
        self.quota = quota.Manager(client)
        self.router = router.Manager(client)
        self.security_group = security_group.Manager(client)
        self.subnet = subnet.Manager(client)
        self.subnet_pool = subnet_pool.Manager(client)
        self.metering = metering.Client(client)
        self.lb = lb.Client(client)
        self.lbaas = lbaas.Client(client)
        self.vpn = vpn.Client(client)

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
