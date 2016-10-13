class Task(object):
    """Task class, containing task information."""
    def __init__(self, param_dict, client):
        self.client = client
        self.param_dict = param_dict
        self.id = param_dict['task_id']

    def __getattr__(self, name):
        if name in self.param_dict:
            return self.param_dict[name]
        raise AttributeError("'%s' object has no attribute %s"
                             % (type(self).__name__, name))

    def cancel(self):
        self.client.cancel_task(self.id)
