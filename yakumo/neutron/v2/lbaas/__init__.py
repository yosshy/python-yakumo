from . import load_balancer
from . import pool


class Client(object):

    def __init__(self, client, **kwargs):
        self.load_balancer = load_balancer.Manager(client, **kwargs)
        self.pool = pool.Manager(client, **kwargs)
