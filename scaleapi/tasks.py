class Task(object):
    """Task class, containing task information."""
    def __init__(self, param_dict, client):
        self.client = client
        self.param_dict = param_dict
        self.id = param_dict['task_id']

    def __getattr__(self, name):
        if name in self.param_dict:
            return self.param_dict[name]
        if name in self.params:
            return self.params[name]
        raise AttributeError("'%s' object has no attribute %s"
                             % (type(self).__name__, name))

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return 'Task(id=%s)' % self.id

    def __repr__(self):
        return 'Task(%s)' % self.param_dict

    def refresh(self):
        self.param_dict = self.client._getrequest('task/%s' % self.id)

    def cancel(self):
        self.client.cancel_task(self.id)
