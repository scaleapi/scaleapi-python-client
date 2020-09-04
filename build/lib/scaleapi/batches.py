class Batch(object):
    def __init__(self, param_dict, client):
        self.param_dict = param_dict
        self.name = param_dict['name']
        self.pending = None
        self.completed = None
        self.error = None
        self.canceled = None
        self.client = client

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return 'Batch(name=%s)' % self.name

    def __repr__(self):
        return 'Batch(%s)' % self.param_dict

    def finalize(self):
        return self.client._postrequest("batches/%s/finalize" % self.name)

    def get_status(self):
        res = self.client._getrequest("batches/%s/status" % self.name)
        for stat in ["pending", "completed", "error", "canceled"]:
            setattr(self, stat, res.get(stat, 0))
