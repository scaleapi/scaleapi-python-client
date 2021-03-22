class Batch(object):
    def __init__(self, param_dict, client):
        self.param_dict = param_dict
        self.name = param_dict['name']
        self.status = param_dict["status"]

        self.pending = None
        self.completed = None
        self.error = None
        self.canceled = None
        self.client = client
        self.get_status()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return 'Batch(name=%s)' % self.name

    def __repr__(self):
        return 'Batch(%s)' % self.param_dict

    def finalize(self):
        res = self.client.finalize_batch(self.name)
        self.status = res.status
        return res

    def get_status(self):
        res = self.client.batch_status(self.name)
        self.status = res["status"]
        for stat in ["pending", "completed", "error", "canceled"]:
            setattr(self, stat, res.get(stat, 0))
        return res
