from typing import IO, Dict, Generator, Generic, List, TypeVar, Union

from scaleapi.batches import Batch, BatchStatus
from scaleapi.evaluation_tasks import EvaluationTask
from scaleapi.exceptions import ScaleInvalidRequest
from scaleapi.files import File
from scaleapi.projects import Project
from scaleapi.training_tasks import TrainingTask

from ._version import __version__  # noqa: F401
from .api import Api
from .tasks import Task, TaskReviewStatus, TaskStatus, TaskType

T = TypeVar("T")


class Paginator(list, Generic[T]):
    """Paginator for list endpoints"""

    def __init__(
        self,
        docs: List[T],
        total: int,
        limit: int,
        offset: int,
        has_more: bool,
        next_token=None,
    ):
        super().__init__(docs)
        self.docs = docs
        self.total = total
        self.limit = limit
        self.offset = offset
        self.has_more = has_more
        self.next_token = next_token


class Tasklist(Paginator[Task]):
    """Tasks Paginator"""


class Batchlist(Paginator[Batch]):
    """Batches Paginator"""


class ScaleClient:
    """Main class serves as an interface for Scale API"""

    def __init__(self, api_key, source=None, api_instance_url=None):
        self.api = Api(
            api_key, user_agent_extension=source, api_instance_url=api_instance_url
        )

    def get_task(self, task_id: str) -> Task:
        """Fetches a task.
        Returns the associated task.

        Args:
            task_id (str):
                Task identifier
        Returns:
            Task:
        """
        endpoint = f"task/{task_id}"
        return Task(self.api.get_request(endpoint), self)

    def cancel_task(self, task_id: str, clear_unique_id: bool = False) -> Task:
        """Cancels a task and returns the associated task.
        Raises a ScaleException if it has already been canceled.

        Args:
            task_id (str):
                Task id
            clear_unique_id (boolean):
                Option to clear unique id when the task is deleted

        Returns:
            Task
        """
        if clear_unique_id:
            endpoint = f"task/{task_id}/cancel?clear_unique_id=true"
        else:
            endpoint = f"task/{task_id}/cancel"
        return Task(self.api.post_request(endpoint), self)

    def update_task_unique_id(self, task_id: str, unique_id: str) -> Task:
        """Updates a task's unique_id and returns the associated task.
        Raises a ScaleDuplicateResource exception if unique_id
        is already in use.

        Args:
            task_id (str):
                Task id
            unique_id (str):
                unique_id to set

        Returns:
            Task
        """
        payload = dict(unique_id=unique_id)
        endpoint = f"task/{task_id}/unique_id"
        return Task(self.api.post_request(endpoint, body=payload), self)

    def clear_task_unique_id(self, task_id: str) -> Task:
        """Clears a task's unique_id and returns the associated task.

        Args:
            task_id (str):
                Task id

        Returns:
            Task
        """
        endpoint = f"task/{task_id}/unique_id"
        return Task(self.api.delete_request(endpoint), self)

    def tasks(self, **kwargs) -> Tasklist:
        """Returns a list of your tasks.
        Returns up to 100 at a time, to get more, use the
        next_token param passed back.

        Valid Args:
            start_time (str):
                The minimum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            end_time (str):
                The maximum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            status (str):
                Status to filter tasks, can be 'completed', 'pending',
                or 'canceled'

            type (str):
                Task type to filter. i.e. 'imageannotation'

            project (str):
                Project name to filter tasks by

            batch (str):
                Batch name to filter tasks by

            customer_review_status (str):
                Audit status of task, can be 'pending', 'fixed',
                'accepted' or 'rejected'.

            unique_id (List[str] | str):
                The unique_id of a task.

            completed_after (str):
                The minimum value of `completed_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            completed_before (str):
                The maximum value of `completed_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            updated_after (str):
                The minimum value of `updated_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            updated_before (str):
                The maximum value of `updated_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_after (str):
                The minimum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_before (str):
                The maximum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            tags (List[str] | str):
                The tags of a task; multiple tags can be
                specified as a list.

            limit (int):
                Determines the page size (1-100)

            next_token (str):
                Can be use to fetch the next page of tasks
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
                    f"Illegal parameter {key} for ScaleClient.tasks()"
                )

        response = self.api.get_request("tasks", params=kwargs)

        docs = [Task(json, self) for json in response["docs"]]
        return Tasklist(
            docs,
            response["total"],
            response["limit"],
            response["offset"],
            response["has_more"],
            response.get("next_token"),
        )

    def get_tasks(
        self,
        project_name: str,
        batch_name: str = None,
        task_type: TaskType = None,
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
    ) -> Generator[Task, None, None]:
        """Retrieve all tasks as a `generator` method, with the
        given parameters. This methods handles pagination of
        tasks() method.

        In order to retrieve results as a list, please use:
        `task_list = list(get_tasks(...))`

        Args:
            project_name (str):
                Project Name

            batch_name (str, optional):
                Batch Name

            task_type (TaskType, optional):
                Task type to filter i.e. `TaskType.TextCollection`

            status (TaskStatus, optional):
                Task status i.e. `TaskStatus.Completed`

            review_status (List[TaskReviewStatus] | TaskReviewStatus):
                The status of the audit result of the task.
                Input can be a single element or a list of
                TaskReviewStatus. i.e. `TaskReviewStatus.Accepted` to
                filter the tasks that you accepted after audit.

            unique_id (List[str] | str, optional):
                The unique_id of a task. Multiple unique IDs can be
                specified at the same time as a list.

            completed_after (str, optional):
                The minimum value of `completed_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            completed_before (str, optional):
                The maximum value of `completed_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            updated_after (str, optional):
                The minimum value of `updated_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            updated_before (str, optional):
                The maximum value of `updated_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_after (str, optional):
                The minimum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_before (str, optional):
                The maximum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            tags (List[str] | str, optional):
                The tags of a task; multiple tags can be
                specified as a list.

        Yields:
            Generator[Task]:
                Yields Task objects, can be iterated.
        """

        next_token = None
        has_more = True

        tasks_args = self._process_tasks_endpoint_args(
            project_name,
            batch_name,
            task_type,
            status,
            review_status,
            unique_id,
            completed_after,
            completed_before,
            updated_after,
            updated_before,
            created_after,
            created_before,
            tags,
        )

        while has_more:
            tasks_args["next_token"] = next_token

            tasks = self.tasks(**tasks_args)
            for task in tasks.docs:
                yield task

            next_token = tasks.next_token
            has_more = tasks.has_more

    def get_tasks_count(
        self,
        project_name: str,
        batch_name: str = None,
        task_type: TaskType = None,
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
    ) -> int:
        """Returns number of tasks with given filters.

        Args:
            project_name (str):
                Project Name

            batch_name (str, optional):
                Batch Name

            task_type (TaskType, optional):
                Task type to filter i.e. `TaskType.TextCollection`

            status (TaskStatus, optional):
                Task status i.e. `TaskStatus.Completed`

            review_status (List[TaskReviewStatus] | TaskReviewStatus):
                The status of the audit result of the task.
                Input can be a single element or a list of
                TaskReviewStatus. i.e. `TaskReviewStatus.Accepted` to
                filter the tasks that you accepted after audit.

            unique_id (List[str] | str, optional):
                The unique_id of a task. Multiple unique IDs can be
                specified at the same time as a list.

            completed_after (str, optional):
                The minimum value of `completed_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            completed_before (str, optional):
                The maximum value of `completed_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            updated_after (str, optional):
                The minimum value of `updated_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            updated_before (str, optional):
                The maximum value of `updated_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_after (str, optional):
                The minimum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_before (str, optional):
                The maximum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            tags (List[str] | str, optional):
                The tags of a task; multiple tags can be
                specified as a list.

        Returns:
            int:
                Returns number of tasks
        """

        tasks_args = self._process_tasks_endpoint_args(
            project_name,
            batch_name,
            task_type,
            status,
            review_status,
            unique_id,
            completed_after,
            completed_before,
            updated_after,
            updated_before,
            created_after,
            created_before,
            tags,
        )

        tasks_args["limit"] = 1

        tasks = self.tasks(**tasks_args)
        return tasks.total

    @staticmethod
    def _process_tasks_endpoint_args(
        project_name: str,
        batch_name: str = None,
        task_type: TaskType = None,
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
    ):
        """Generates args for /tasks endpoint."""
        tasks_args = {
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
        if task_type:
            tasks_args["type"] = task_type.value
        if review_status:
            if isinstance(review_status, List):
                value = ",".join(map(lambda x: x.value, review_status))
            else:
                value = review_status.value

            tasks_args["customer_review_status"] = value

        return tasks_args

    def create_task(self, task_type: TaskType, **kwargs) -> Task:
        """This method can be used for any Scale supported task type.
        Parameters may differ based on the given task_type.
        https://github.com/scaleapi/scaleapi-python-client#create-task

        Args:
            task_type (TaskType):
                Task type to be created
                i.e. `TaskType.ImageAnnotation`
            **kwargs:
                Passing in the applicable values into thefunction
                definition. The applicable fields and further
                information for each task type can be found in
                Scale's API documentation.
                https://docs.scale.com/reference

        Returns:
            Task:
                Returns created task.
        """
        endpoint = f"task/{task_type.value}"
        taskdata = self.api.post_request(endpoint, body=kwargs)
        return Task(taskdata, self)

    def create_batch(
        self,
        project: str,
        batch_name: str,
        callback: str = "",
        calibration_batch: bool = False,
        self_label_batch: bool = False,
    ) -> Batch:
        """Create a new Batch within a project.
        https://docs.scale.com/reference#batch-creation

        Args:
            project (str):
                Project name to create batch in
            batch_name (str):
                Batch name
            callback (str, optional):
                Email to notify, or URL to POST to
                when a batch is complete.
            calibration_batch (bool):
                Only applicable for self serve projects.
                Create a calibration_batch batch by setting
                the calibration_batch flag to true.
            self_label_batch (bool):
                Only applicable for self serve projects.
                Create a self_label batch by setting
                the self_label_batch flag to true.

        Returns:
            Batch: Created batch object
        """
        endpoint = "batches"
        payload = dict(
            project=project,
            name=batch_name,
            calibration_batch=calibration_batch,
            self_label_batch=self_label_batch,
            callback=callback,
        )
        batchdata = self.api.post_request(endpoint, body=payload)
        return Batch(batchdata, self)

    def finalize_batch(self, batch_name: str) -> Batch:
        """Finalizes a batch so its tasks can be worked on.
        https://docs.scale.com/reference#batch-finalization

        Args:
            batch_name (str):
                Batch name

        Returns:
            Batch
        """
        endpoint = f"batches/{Api.quote_string(batch_name)}/finalize"
        batchdata = self.api.post_request(endpoint)
        return Batch(batchdata, self)

    def batch_status(self, batch_name: str) -> Dict:
        """Returns the status of a batch with the counts of
        its tasks grouped by task status.
        https://docs.scale.com/reference#batch-status

        Args:
            batch_name (str):
                Batch name

        Returns:
            Dict {
                status: Batch status
                pending (optional): # of tasks in pending stage
                error (optional): # of tasks in error stage
                completed (optional): # of tasks in completed stage
                canceled (optional): # of tasks in canceled stage
            }
        """
        endpoint = f"batches/{Api.quote_string(batch_name)}/status"
        status_data = self.api.get_request(endpoint)
        return status_data

    def get_batch(self, batch_name: str) -> Batch:
        """Returns the details of a batch with the given name.
        https://docs.scale.com/reference#batch-retrieval

        Args:
            batch_name (str):
                Batch name

        Returns:
            Batch
        """
        endpoint = f"batches/{Api.quote_string(batch_name)}"
        batchdata = self.api.get_request(endpoint)
        return Batch(batchdata, self)

    def batches(self, **kwargs) -> Batchlist:
        """This is a paged endpoint for all of your batches.
        Pagination is based off limit and offset parameters,
        which determine the page size and how many results to skip.
        Returns up to 100 batches at a time (limit).
        https://docs.scale.com/reference#batch-list

        Valid Args:
            start_time (str):
                The minimum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            end_time (str):
                The maximum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            status (str):
                Status to filter batches by

            project (str):
                Project name to filter batches by

            limit (int):
                Determines the page size (1-100)

            offset (int):
                How many results to skip

        Returns:
            Batchlist:
                Paginated result. Batchlist.docs provides access
                to batches list. Batchlist.limit and Batchlist.offset
                are helpers for pagination.
        """
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
                    f"Illegal parameter {key} for ScaleClient.batches()"
                )
        endpoint = "batches"
        response = self.api.get_request(endpoint, params=kwargs)
        docs = [Batch(doc, self) for doc in response["docs"]]

        return Batchlist(
            docs,
            response["totalDocs"],
            response["limit"],
            response["offset"],
            response["has_more"],
        )

    def get_batches(
        self,
        project_name: str = None,
        batch_status: BatchStatus = None,
        created_after: str = None,
        created_before: str = None,
    ) -> Generator[Batch, None, None]:
        """`Generator` method to yield all batches with the given
        parameters.

        In order to retrieve results as a list, please use:
        `batches_list = list(get_batches(...))`

        Args:
            project_name (str):
                Project Name to filter batches

            batch_status (BatchStatus, optional):
                i.e. `BatchStatus.Completed`

            created_after (str, optional):
                The minimum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

            created_before (str, optional):
                The maximum value of `created_at` in UTC timezone
                ISO format: 'YYYY-MM-DD HH:MM:SS.mmmmmm'

        Yields:
            Generator[Batch]:
                Yields Batch, can be iterated.
        """

        has_more = True
        offset = 0

        while has_more:
            batches_args = {
                "start_time": created_after,
                "end_time": created_before,
                "project": project_name,
                "offset": offset,
            }

            if batch_status:
                batches_args["status"] = batch_status.value

            batches = self.batches(**batches_args)
            for batch in batches.docs:
                yield batch
            offset += batches.limit
            has_more = batches.has_more

    def create_project(
        self,
        project_name: str,
        task_type: TaskType,
        params: Dict = None,
        rapid: bool = False,
        studio: bool = False,
    ) -> Project:
        """Creates a new project.
        https://docs.scale.com/reference#project-creation

        Args:
            project_name (str):
                Project name

            task_type (TaskType):
                Task Type i.e. `TaskType.ImageAnnotation`

            params (Dict):
                Project parameters to be specificed.
                i.e. `{'instruction':'Please label the kittens'}`

        Returns:
            Project: [description]
        """
        endpoint = "projects"
        payload = dict(
            type=task_type.value,
            name=project_name,
            params=params,
            rapid=rapid,
            studio=studio,
        )
        projectdata = self.api.post_request(endpoint, body=payload)
        return Project(projectdata, self)

    def get_project(self, project_name: str) -> Project:
        """Retrieves a single project with the given name.
        https://docs.scale.com/reference#project-retrieval

        Args:
            project_name (str):
                Project name

        Returns:
            Project
        """
        endpoint = f"projects/{Api.quote_string(project_name)}"
        projectdata = self.api.get_request(endpoint)
        return Project(projectdata, self)

    def get_projects(self) -> List[Project]:
        """Returns all projects.
        Refer to Projects API Reference:
        https://docs.scale.com/reference#list-all-projects
        Same as `projects()` method.

        Returns:
            List[Project]
        """
        return self.projects()

    def projects(self) -> List[Project]:
        """Returns all projects.
        Refer to Projects API Reference:
        https://docs.scale.com/reference#list-all-projects

        Returns:
            List[Project]
        """
        endpoint = "projects"
        project_list = self.api.get_request(endpoint)
        return [Project(project, self) for project in project_list]

    def update_project(self, project_name: str, **kwargs) -> Project:
        """You can set parameters on a project. Project-level-parameters
        will be set on future tasks created under this project if they
        are not set in the task request. Any parameters specified in
        the task request will override any project parameter.
        https://docs.scale.com/reference#project-update-parameters

        Args:
            project_name (str):
                Project's name

            **kwargs:
                Project parameters to be set.

        Returns:
            Project
        """

        endpoint = f"projects/{Api.quote_string(project_name)}/setParams"
        projectdata = self.api.post_request(endpoint, body=kwargs)
        return Project(projectdata, self)

    def upload_file(self, file: IO, **kwargs) -> File:
        """Upload file.
        Refer to Files API Reference:
        https://docs.scale.com/reference#file-upload-1

        Args:
            file (IO):
                File buffer

        Returns:
            File
        """

        endpoint = "files/upload"
        files = {"file": file}
        filedata = self.api.post_request(endpoint, files=files, data=kwargs)
        return File(filedata, self)

    def import_file(self, file_url: str, **kwargs) -> File:
        """Import file from a remote url.
        Refer to Files API Reference:
        https://docs.scale.com/reference#file-import-1

        Args:
            file_url (str):
                File's url

        Returns:
            File
        """

        endpoint = "files/import"
        payload = dict(file_url=file_url, **kwargs)
        filedata = self.api.post_request(endpoint, body=payload)
        return File(filedata, self)

    def create_evaluation_task(
        self,
        task_type: TaskType,
        **kwargs,
    ) -> EvaluationTask:
        """This method can only be used for Rapid projects.
        Supported Task Types: [
            DocumentTranscription,
            SegmentAnnotation,
            VideoPlaybackAnnotation,
            ImageAnnotation,
            TextCollection,
            NamedEntityRecognition
        ]
        Parameters may differ based on the given task_type.

        Args:
            task_type (TaskType):
                Task type to be created
                e.g.. `TaskType.ImageAnnotation`
            **kwargs:
                The same set of parameters are expected with
                create_task function. Additionally with
                an expected_response and an optional initial_response
                if you want to make it a review phase evaluation task
                The expected_response/initial_response should follow
                the format of any other tasks' response on your project.
                It's recommended to try a self_label batch to get
                familiar with the response format.
                Scale's API documentation.
                https://docs.scale.com/reference

        Returns:
            EvaluationTask:
                Returns created evaluation task.
        """
        endpoint = f"evaluation_tasks/{task_type.value}"

        evaluation_task_data = self.api.post_request(endpoint, body=kwargs)
        return EvaluationTask(evaluation_task_data, self)

    def create_training_task(
        self,
        task_type: TaskType,
        **kwargs,
    ) -> TrainingTask:
        """This method can only be used for Rapid projects.
        Supported Task Types: [
            DocumentTranscription,
            SegmentAnnotation,
            VideoPlaybackAnnotation,
            ImageAnnotation,
            TextCollection,
            NamedEntityRecognition
        ]
        Parameters may differ based on the given task_type.

        Args:
            task_type (TaskType):
                Task type to be created
                e.g.. `TaskType.ImageAnnotation`
            **kwargs:
                The same set of parameters are expected with
                create_task function and an additional
                expected_response. Scale's API documentation.
                https://docs.scale.com/reference

        Returns:
            TrainingTask:
                Returns created training task.
        """
        endpoint = f"training_tasks/{task_type.value}"

        training_task_data = self.api.post_request(endpoint, body=kwargs)
        return TrainingTask(training_task_data, self)
