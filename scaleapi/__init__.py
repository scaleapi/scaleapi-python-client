import requests
import platform

from .tasks import Task
from .batches import Batch
from .projects import Project
from ._version import __version__

TASK_TYPES = [
    'annotation',
    'audiotranscription',
    'categorization',
    'comparison',
    'cuboidannotation',
    'datacollection',
    'imageannotation',
    'lineannotation',
    'namedentityrecognition',
    'pointannotation',
    'polygonannotation',
    'segmentannotation',
    'transcription',
    'textcollection',
    'documenttranscription',
    'videoannotation',
    'videoboxannotation',
    'videoplaybackannotation',
    'videocuboidannotation'
]
SCALE_ENDPOINT = 'https://api.scale.com/v1/'
DEFAULT_LIMIT = 100
DEFAULT_OFFSET = 0


class ScaleException(Exception):
    def __init__(self, message, errcode):
        super(ScaleException, self).__init__(
            '<Response [{}]> {}'.format(errcode, message))
        self.code = errcode


class ScaleInvalidRequest(ScaleException, ValueError):
    pass


class Paginator(list):
    def __init__(self, docs, total, limit, offset, has_more, next_token=None):
        super(Paginator, self).__init__(docs)
        self.docs = docs
        self.total = total
        self.limit = limit
        self.offset = offset
        self.has_more = has_more
        self.next_token = next_token


class Tasklist(Paginator):
    pass


class Batchlist(Paginator):
    pass


class ScaleClient(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": _generate_useragent()
        }

    def _getrequest(self, endpoint, params=None):
        """Makes a get request to an endpoint.

        If an error occurs, assumes that endpoint returns JSON as:
            { 'status_code': XXX,
              'error': 'I failed' }
        """
        params = params or {}
        r = requests.get(SCALE_ENDPOINT + endpoint,
                         headers=self._headers,
                         auth=(self.api_key, ''), params=params)

        if r.status_code == 200:
            return r.json()
        else:
            try:
                error = r.json()['error']
            except ValueError:
                error = r.text
            if r.status_code == 400:
                raise ScaleInvalidRequest(error, r.status_code)
            else:
                raise ScaleException(error, r.status_code)

    def _postrequest(self, endpoint, payload=None):
        """Makes a post request to an endpoint.

        If an error occurs, assumes that endpoint returns JSON as:
            { 'status_code': XXX,
              'error': 'I failed' }
        """
        payload = payload or {}
        r = requests.post(SCALE_ENDPOINT + endpoint, json=payload,
                          headers=self._headers,
                          auth=(self.api_key, ''))

        if r.status_code == 200:
            return r.json()
        else:
            try:
                error = r.json()['error']
            except ValueError:
                error = r.text
            if r.status_code == 400:
                raise ScaleInvalidRequest(error, r.status_code)
            else:
                raise ScaleException(error, r.status_code)

    def fetch_task(self, task_id):
        """Fetches a task.

        Returns the associated task.
        """
        return Task(self._getrequest('task/%s' % task_id), self)

    def cancel_task(self, task_id):
        """Cancels a task.

        Returns the associated task.
        Raises a ScaleException if it has already been canceled.
        """
        return Task(self._postrequest('task/%s/cancel' % task_id), self)

    def tasks(self, **kwargs):
        """Returns a list of your tasks.
        Returns up to 100 at a time, to get more, use the next_token param passed back.

        Note that offset is deprecated.

        start/end_time are ISO8601 dates, the time range of tasks to fetch.
        status can be 'completed', 'pending', or 'canceled'.
        type is the task type.
        limit is the max number of results to display per page,
        next_token can be use to fetch the next page of tasks.
        customer_review_status can be 'pending', 'fixed', 'accepted' or 'rejected'.
        offset (deprecated) is the number of results to skip (for showing more pages).
        """
        allowed_kwargs = {'start_time', 'end_time', 'status', 'type', 'project',
                          'batch', 'limit', 'offset', 'completed_before', 'completed_after',
                          'next_token', 'customer_review_status', 'updated_before', 'updated_after',
                          'tags', 'unique_id'}
        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest('Illegal parameter %s for ScaleClient.tasks()'
                                          % key, None)
        response = self._getrequest('tasks', params=kwargs)
        docs = [Task(json, self) for json in response['docs']]
        return Tasklist(docs, response['total'], response['limit'],
                        response['offset'], response['has_more'], response.get('next_token'))

    def create_task(self, task_type, **kwargs):
        endpoint = 'task/' + task_type
        taskdata = self._postrequest(endpoint, payload=kwargs)
        return Task(taskdata, self)

    def create_batch(self, project, batch_name, callback):
        payload = dict(project=project, name=batch_name, callback=callback)
        batchdata = self._postrequest('batches', payload)
        return Batch(batchdata, self)

    def finalize_batch(self, batch_name):
        batchdata = self._postrequest('batches/%s/finalize' % batch_name)
        return Batch(batchdata, self)

    def batch_status(self, batch_name):
        batchdata = self._getrequest('batches/%s/status' % batch_name)
        return Batch.get_status(self)

    def get_batch(self, batch_name):
        batchdata = self._getrequest('batches/%s' % batch_name)
        return Batch(batchdata, self)

    def list_batches(self, **kwargs):
        allowed_kwargs = {'start_time', 'end_time', 'status', 'project',
                          'limit', 'offset', }
        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest('Illegal parameter %s for ScaleClient.list_batches()'
                                          % key, None)
        response = self._getrequest('batches', params=kwargs)
        docs = [Batch(doc, self) for doc in response['docs']]
        return Batchlist(
            docs, response['totalDocs'], response['limit'], response['has_more'], response.get(
                'next_token'),
        )

    def create_project(self, project_name, type, params):
        payload = dict(type=type, name=project_name, params=params)
        projectdata = self._postrequest('projects', payload)
        return Project(projectdata, self)

    def get_project(self, project_name):
        projectdata = self._getrequest('projects/%s' % project_name)
        return Project(projectdata, self)

    def projects(self):
        response = self._getrequest('projects')
        return response

    def update_project(self, project_name, **kwargs):
        allowed_kwargs = {'patch', 'instruction'}
        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest('Illegal parameter %s for ScaleClient.update_project()'
                                          % key, None)
        projectdata = self._postrequest('projects/%s/setParams' % project_name, payload=kwargs)
        return projectdata

def _generate_useragent():
    try:
        python_version = platform.python_version()
        os_platform = platform.platform()

        user_agent = '%s/%s Python/%s OS/%s' % (__name__, __version__, python_version, os_platform)
        return user_agent
    except:
        return "scaleapi-python-client"

def _AddTaskTypeCreator(task_type):
    def create_task_wrapper(self, **kwargs):
        return self.create_task(task_type, **kwargs)
    setattr(ScaleClient, 'create_' + task_type + '_task', create_task_wrapper)


for taskType in TASK_TYPES:
    _AddTaskTypeCreator(taskType)
