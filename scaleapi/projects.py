class Project(object):
    """Project class"""
    def __init__(self, param_dict, client):
        self.client = client
        self.param_dict = param_dict
        self.name = param_dict['name']

    def __getattr__(self, name):
        if name in self.param_dict:
            return self.param_dict[name]
        if name in self.params:
            return self.params[name]
        raise AttributeError("'%s' object has no attribute %s"
                             % (type(self).__name__, name))

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return 'Project(name=%s)' % self.name

    def __repr__(self):
        return 'Project(%s)' % self.param_dict
