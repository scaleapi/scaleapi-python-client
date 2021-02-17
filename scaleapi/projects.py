class Project(object):
    def __init__(self, param_dict, client):
        self.param_dict = param_dict
        self.name = param_dict['name']
        self.client = client 

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return 'Project(name=%s)' % self.name

    def __repr__(self):
        return 'Project(%s)' % self.param_dict
