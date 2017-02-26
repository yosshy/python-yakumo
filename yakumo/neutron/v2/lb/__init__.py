from . import health_monitor
from . import pool


class Client(object):

    def __init__(self, client, **kwargs):
        self.health_monitor = health_monitor.Manager(client, **kwargs)
        self.pool = pool.Manager(client, **kwargs)
