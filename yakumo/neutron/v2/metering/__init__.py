from . import label
from . import rule


class Client(object):

    def __init__(self, client, **kwargs):
        self.label = label.Manager(client, **kwargs)
        self.rule = rule.Manager(client, **kwargs)
