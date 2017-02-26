from . import service
from . import ike_policy
from . import ipsec_policy
from . import ipsec_site_connection


class Client(object):

    def __init__(self, client, **kwargs):
        self.service = service.Manager(client, **kwargs)
        self.ike_policy = ike_policy.Manager(client, **kwargs)
        self.ipsec_policy = ipsec_policy.Manager(client, **kwargs)
        self.ipsec_site_connection = ipsec_site_connection.Manager(client,
                                                                   **kwargs)
