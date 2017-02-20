from . import label
from . import rule


class Client(object):

    def __init__(self, client, *args, **kwargs):
        self.label = label.Manager(client)
        self.rule = rule.Manager(client)
