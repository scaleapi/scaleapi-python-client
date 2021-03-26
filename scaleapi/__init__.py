from typing import Dict, Generic, List, TypeVar, Union

from scaleapi.batches import Batch, BatchStatus
from scaleapi.exceptions import ScaleInvalidRequest
from scaleapi.projects import Project

from .api import Api
from .tasks import Task, TaskReviewStatus, TaskStatus, TaskType
from ._version import __version__  # noqa: F401

T = TypeVar("T")


class Paginator(list, Generic[T]):
    def __init__(
        self,
        docs: List[T],
        total: int,
        limit: int,
        offset: int,
        has_more: bool,
        next_token=None,
    ):
        super(Paginator, self).__init__(docs)
        self.docs = docs
        self.total = total
        self.limit = limit
        self.offset = offset
        self.has_more = has_more
        self.next_token = next_token


class Tasklist(Paginator[Task]):
    pass


class Batchlist(Paginator[Batch]):
    pass


class ScaleClient(object):
    def __init__(self, api_key, source=None):
        self.api = Api(api_key, source)

    def fetch_task(self, task_id: str) -> Task:
        """Fetches a task.
        Returns the associated task.
        """
        endpoint = f"task/{task_id}"
        return Task(self.api._get_request(endpoint), self)

    def cancel_task(self, task_id: str) -> Task:
        """Cancels a task.
        Returns the associated task.
        Raises a ScaleException if it has already been canceled.
        """
        endpoint = f"task/{task_id}/cancel"
        return Task(self.api._post_request(endpoint), self)

    def tasks(self, **kwargs) -> Tasklist:
        """Returns a list of your tasks.
        Returns up to 100 at a time, to get more, use the next_token param passed back.
        start/end_time are ISO8601 dates, the time range of tasks to fetch.
        status can be 'completed', 'pending', or 'canceled'.
        type is the task type.
        limit is the max number of results to display per page,
        next_token can be use to fetch the next page of tasks.
        customer_review_status can be 'pending', 'fixed', 'accepted' or 'rejected'.
        """
        allowed_kwargs = {
            "start_time",
            "end_time",
            "status",
            "type",
            "project",
            "batch",
            "limit",
            "completed_before",
            "completed_after",
            "next_token",
            "customer_review_status",
            "tags",
            "updated_before",
            "updated_after",
            "unique_id",
        }

        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest(
                    f"Illegal parameter {key} for ScaleClient.tasks()", None
                )

        response = self.api._get_request("tasks", params=kwargs)

        docs = [Task(json, self) for json in response["docs"]]
        return Tasklist(
            docs,
            response["total"],
            response["limit"],
            response["offset"],
            response["has_more"],
            response.get("next_token"),
        )

    def tasks_all(
        self,
        project_name: str,
        batch_name: str = None,
        type: TaskType = None,
        status: TaskStatus = None,
        review_status: Union[List[TaskReviewStatus], TaskReviewStatus] = None,
        unique_id: Union[List[str], str] = None,
        completed_after: str = None,
        completed_before: str = None,
        updated_after: str = None,
        updated_before: str = None,
        created_after: str = None,
        created_before: str = None,
        tags: Union[List[str], str] = None,
    ) -> List[Task]:

        tasks_list: List[Task] = []
        next_token = None
        has_more = True

        while has_more:
            tasks_args = {
                "next_token": next_token,
                "start_time": created_after,
                "end_time": created_before,
                "project": project_name,
                "batch": batch_name,
                "completed_before": completed_before,
                "completed_after": completed_after,
                "tags": tags,
                "updated_before": updated_before,
                "updated_after": updated_after,
                "unique_id": unique_id,
            }

            if status:
                tasks_args["status"] = status.value
            if type:
                tasks_args["type"] = type.value
            if review_status:
                tasks_args["customer_review_status"] = review_status.value

            tasks = self.tasks(**tasks_args)
            next_token = tasks.next_token
            has_more = tasks.has_more
            tasks_list.extend(tasks.docs)

        return tasks_list

    def create_task(self, task_type: TaskType, **kwargs) -> Task:
        endpoint = f"task/{task_type.value}"
        taskdata = self.api._post_request(endpoint, body=kwargs)
        return Task(taskdata, self)

    def create_batch(self, project: str, batch_name: str, callback: str = "") -> Batch:
        endpoint = "batches"
        payload = dict(project=project, name=batch_name, callback=callback)
        batchdata = self.api._post_request(endpoint, body=payload)
        return Batch(batchdata, self)

    def finalize_batch(self, batch_name: str) -> Batch:
        endpoint = f"batches/{Api.quote_string(batch_name)}/finalize"
        batchdata = self.api._post_request(endpoint)
        return Batch(batchdata, self)

    def batch_status(self, batch_name: str) -> Dict:
        endpoint = f"batches/{Api.quote_string(batch_name)}/status"
        status_data = self.api._get_request(endpoint)
        return status_data

    def get_batch(self, batch_name):
        endpoint = f"batches/{Api.quote_string(batch_name)}"
        batchdata = self.api._get_request(endpoint)
        return Batch(batchdata, self)

    def list_batches(self, **kwargs) -> Batchlist:
        allowed_kwargs = {
            "start_time",
            "end_time",
            "status",
            "project",
            "limit",
            "offset",
        }

        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest(
                    f"Illegal parameter {key} for ScaleClient.list_batches()"
                )
        endpoint = "batches"
        response = self.api._get_request(endpoint, params=kwargs)
        docs = [Batch(doc, self) for doc in response["docs"]]

        return Batchlist(
            docs,
            response["totalDocs"],
            response["limit"],
            response["offset"],
            response["has_more"],
        )

    def list_batches_all(
        self,
        project_name: str,
        batch_status: BatchStatus = None,
        created_after: str = None,
        created_before: str = None,
        limit: int = 100,
    ) -> List[Batch]:

        batches_list: List[Batch] = []
        has_more = True
        offset = 0

        while has_more:
            batches_args = {
                "start_time": created_after,
                "end_time": created_before,
                "project": project_name,
                "offset": offset,
                "limit": limit,
            }

            if batch_status:
                batches_args["status"] = batch_status.value

            batches = self.list_batches(**batches_args)
            offset += batches.limit
            has_more = batches.has_more
            batches_list.extend(batches.docs)

        return batches_list

    def create_project(self, project_name: str, type: TaskType, params) -> Project:
        endpoint = "projects"
        payload = dict(type=type.value, name=project_name, params=params)
        projectdata = self.api._post_request(endpoint, body=payload)
        return Project(projectdata, self)

    def get_project(self, project_name: str) -> Project:
        endpoint = f"projects/{Api.quote_string(project_name)}"
        projectdata = self.api._get_request(endpoint)
        return Project(projectdata, self)

    def projects(self) -> List[Project]:
        endpoint = "projects"
        project_list = self.api._get_request(endpoint)
        return [Project(project, self) for project in project_list]

    def update_project(self, project_name: str, **kwargs) -> Project:
        allowed_kwargs = {"patch", "instruction"}
        for key in kwargs:
            if key not in allowed_kwargs:
                raise ScaleInvalidRequest(
                    f"Illegal parameter {key} for" "ScaleClient.update_project()", None,
                )

        endpoint = f"projects/{Api.quote_string(project_name)}/setParams"
        projectdata = self.api._post_request(endpoint, body=kwargs)
        return Project(projectdata, self)
