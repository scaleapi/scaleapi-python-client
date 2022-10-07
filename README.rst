*********************
Scale AI | Python SDK
*********************

If you use earlier versions of the SDK, please refer to `v1.0.4 documentation <https://github.com/scaleapi/scaleapi-python-client/blob/release-1.0.4/README.rst>`_.

If you are migrating from earlier versions to v2,  please refer to `Migration Guide to v2 <https://github.com/scaleapi/scaleapi-python-client/blob/master/docs/migration_guide.md>`_.

|pic1| |pic2| |pic3|

.. |pic1| image:: https://pepy.tech/badge/scaleapi/month
  :alt: Downloads
  :target: https://pepy.tech/project/scaleapi
.. |pic2| image:: https://img.shields.io/pypi/pyversions/scaleapi.svg
  :alt: Supported Versions
  :target: https://pypi.org/project/scaleapi
.. |pic3| image:: https://img.shields.io/github/contributors/scaleapi/scaleapi-python-client.svg
  :alt: Contributors
  :target: https://github.com/scaleapi/scaleapi-python-client/graphs/contributors

Installation
____________

Install with PyPI (pip)

.. code-block:: bash

    $ pip install --upgrade scaleapi

or install with Anaconda (conda)

.. code-block:: bash

    $ conda install -c conda-forge scaleapi

Usage
_____

.. code-block:: python

    import scaleapi

    client = scaleapi.ScaleClient("YOUR_API_KEY_HERE")

Tasks
_____

Most of these methods will return a `scaleapi.Task` object, which will contain information
about the json response (task_id, status, params, response, etc.).

Any parameter available in `Scale's API documentation`__ can be passed as an argument option with the corresponding type.

__ https://docs.scale.com/reference#tasks-object-overview

The following endpoints for tasks are available:

Create Task
^^^^^^^^^^^

This method can be used for any Scale supported task type using the following format:

.. code-block:: python

    client.create_task(TaskType, ...task parameters...)

Passing in the applicable values into the function definition. The applicable fields and further information for each task type can be found in `Scale's API documentation`__.

__ https://docs.scale.com/reference

.. code-block:: python

    from scaleapi.tasks import TaskType
    from scaleapi.exceptions import ScaleDuplicateResource

    payload = dict(
        project = "test_project",
        callback_url = "http://www.example.com/callback",
        instruction = "Draw a box around each baby cow and big cow.",
        attachment_type = "image",
        attachment = "http://i.imgur.com/v4cBreD.jpg",
        unique_id = "c235d023af73",
        geometries = {
            "box": {
                "objects_to_annotate": ["Baby Cow", "Big Cow"],
                "min_height": 10,
                "min_width": 10,
            }
        },
    )

    try:
        client.create_task(TaskType.ImageAnnotation, **payload)
    except ScaleDuplicateResource as err:
        print(err.message)  # If unique_id is already used for a different task


Retrieve a task
^^^^^^^^^^^^^^^

Retrieve a task given its id. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#retrieve-tasks

.. code-block :: python

    task = client.get_task("30553edd0b6a93f8f05f0fee")
    print(task.status)  # Task status ("pending", "completed", "error", "canceled")
    print(task.response) # If task is complete


Task Attributes
^^^^^^^^^^^^^^^

The older ``param_dict`` attribute is now replaced with a method ``as_dict()`` to return a task's all attributes as a dictionary (JSON).

.. code-block :: python

    task.as_dict()

    # {
    #  'task_id': '30553edd0b6a93f8f05f0fee',
    #  'created_at': '2021-06-17T21:46:36.359Z',
    #  'type': 'imageannotation',
    #  'status': 'pending',
    #   ....
    #  'params': {
    #   'attachment': 'http://i.imgur.com/v4cBreD.jpg',
    #   'attachment_type': 'image',
    #   'geometries': {
    #    'box': {
    #     'objects_to_annotate': ['Baby Cow', 'Big Cow'],
    #     'min_height': 10,
    #     'min_width': 10,
    #     ...
    #   },
    #  'project': 'My Project',
    #  ...
    # }

First-level attributes of Task are also accessible with ``.`` annotation as the following:

.. code-block :: python

    task.status                   # same as task.as_dict()["status"]
    task.params["geometries"]     # same as task.as_dict()["params"]["geometries"]
    task.response["annotations"]  # same as task.as_dict()["response"]["annotations"]


Accessing ``task.params`` child objects directly at task level is **deprecated**. Instead of ``task.attribute``, you should use ``task.params["attribute"]`` for accessing objects under `params`.

.. code-block :: python

    task.params["geometries"]   # task.geometries is DEPRECATED
    task.params["attachment"]   # task.attachment is DEPRECATED

Retrieve List of Tasks
^^^^^^^^^^^^^^^^^^^^^^

Retrieve a list of `Task` objects, with filters for: ``project_name``, ``batch_name``, ``type``, ``status``,
``review_status``, ``unique_id``, ``completed_after``, ``completed_before``, ``updated_after``, ``updated_before``,
``created_after``, ``created_before`` and ``tags``.

``get_tasks()`` is a **generator** method and yields ``Task`` objects.

*A generator is another type of function, returns an iterable that you can loop over like a list.
However, unlike lists, generators do not store the content in the memory.
That helps you to process a large number of objects without increasing memory usage.*

If you will iterate through the tasks and process them once, using a generator is the most efficient method.
However, if you need to process the list of tasks multiple times, you can wrap the generator in a ``list(...)``
statement, which returns a list of Tasks by loading them into the memory.

Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#list-multiple-tasks

.. code-block :: python

    from scaleapi.tasks import TaskReviewStatus, TaskStatus

    tasks = client.get_tasks(
        project_name = "My Project",
        created_after = "2020-09-08",
        completed_before = "2021-04-01",
        status = TaskStatus.Completed,
        review_status = TaskReviewStatus.Accepted
    )

    # Iterating through the generator
    for task in tasks:
        # Download task or do something!
        print(task.task_id)

    # For retrieving results as a Task list
    task_list = list(tasks)
    print(f"{len(task_list))} tasks retrieved")

Get Tasks Count
^^^^^^^^^^^^^^^

``get_tasks_count()`` method returns the number of tasks with the given optional parameters for: ``project_name``, ``batch_name``, ``type``, ``status``,
``review_status``, ``unique_id``, ``completed_after``, ``completed_before``, ``updated_after``, ``updated_before``,
``created_after``, ``created_before`` and ``tags``.

.. code-block :: python

    from scaleapi.tasks import TaskReviewStatus, TaskStatus

    task_count = client.get_tasks_count(
        project_name = "My Project",
        created_after = "2020-09-08",
        completed_before = "2021-04-01",
        status = TaskStatus.Completed,
        review_status = TaskReviewStatus.Accepted
    )

    print(task_count)  # 1923


Cancel Task
^^^^^^^^^^^

Cancel a task given its id if work has not started on the task (task status is ``Queued`` in the UI). Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#cancel-task

.. code-block :: python

    task = client.cancel_task('30553edd0b6a93f8f05f0fee')

    # If you also want to clear 'unique_id' of a task while canceling
    task = client.cancel_task('30553edd0b6a93f8f05f0fee', clear_unique_id=True)

    # cancel() is also available on task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    task.cancel()

    # If you also want to clear 'unique_id' of a task while canceling
    task.cancel(clear_unique_id=True)


Update A Task's Unique Id
^^^^^^^^^^^^^^^^^^^^^^^^^

Update a given task's unique_id. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/update-task-unique-id

.. code-block :: python

    task = client.update_task_unique_id('30553edd0b6a93f8f05f0fee', "new_unique_id")

    # update_unique_id() is also available on task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    task.update_unique_id("new_unique_id")


Clear A Task's Unique Id
^^^^^^^^^^^^^^^^^^^^^^^^^

Clear a given task's unique_id. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/delete-task-unique-id

.. code-block :: python

    task = client.clear_task_unique_id('30553edd0b6a93f8f05f0fee')

    # clear_unique_id() is also available on task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    task.clear_unique_id()


Set A Task's Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^

Set a given task's ``metadata``. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/set-metadata

.. code-block :: python

    # set metadata on a task by specifying task id
    new_metadata = {'myKey': 'myValue'}
    task = client.set_task_metadata('30553edd0b6a93f8f05f0fee', new_metadata)

    # set metadata on a task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    new_metadata = {'myKey': 'myValue'}
    task.set_metadata(new_metadata)

Batches
_______

Create Batch
^^^^^^^^^^^^

Create a new Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-creation

.. code-block:: python

    batch = client.create_batch(
        project = "test_project",
        callback = "http://www.example.com/callback",
        batch_name = "batch_name_01_07_2021"
    )

    print(batch.name)  # batch_name_01_07_2021

Throws ``ScaleDuplicateResource`` exception if a batch with the same name already exists.

Finalize Batch
^^^^^^^^^^^^^^^

Finalize a Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-finalization

.. code-block:: python

    client.finalize_batch(batch_name="batch_name_01_07_2021")

    # Alternative method
    batch = client.get_batch(batch_name="batch_name_01_07_2021")
    batch.finalize()

Check Batch Status
^^^^^^^^^^^^^^^^^^

Get the status of a Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-status

.. code-block:: python

    client.batch_status(batch_name = "batch_name_01_07_2021")

    # Alternative via Batch.get_status()
    batch = client.get_batch("batch_name_01_07_2021")
    batch.get_status() # Refreshes tasks_{status} attributes of Batch
    print(batch.tasks_pending, batch.tasks_completed)

Retrieve A Batch
^^^^^^^^^^^^^^^^

Retrieve a single Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-retrieval

.. code-block:: python

    batch = client.get_batch(batch_name = "batch_name_01_07_2021")

The older ``param_dict`` attribute is now replaced with a method ``batch.as_dict()`` to return a batch's all attributes as a dictionary (JSON).

List Batches
^^^^^^^^^^^^

Retrieve a list of Batches. Optional parameters are ``project_name``, ``batch_status``, ``created_after`` and ``created_before``.

``get_batches()`` is a **generator** method and yields ``Batch`` objects.

*A generator is another type of function, returns an iterable that you can loop over like a list.
However, unlike lists, generators do not store the content in the memory.
That helps you to process a large number of objects without increasing memory usage.*

When wrapped in a ``list(...)`` statement, it returns a list of Batches by loading them into the memory.

Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-list

.. code-block :: python

    from scaleapi.batches import BatchStatus

    batches = client.get_batches(
        batch_status=BatchStatus.Completed,
        created_after = "2020-09-08"
    )

    counter = 0
    for batch in batches:
        counter += 1
        print(f"Downloading batch {counter} | {batch.name} | {batch.project}")

    # Alternative for accessing as a Batch list
    batch_list = list(batches)
    print(f"{len(batch_list))} batches retrieved")

Projects
________

Create Project
^^^^^^^^^^^^^^

Create a new Project. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#project-creation

.. code-block:: python

    from scaleapi.tasks import TaskType

    project = client.create_project(
        project_name = "Test_Project",
        task_type = TaskType.ImageAnnotation,
        params = {"instruction": "Please label the kittens"},
    )

    print(project.name)  # Test_Project

Specify ``rapid=true`` for Rapid projects and ``studio=true`` for Studio projects. Throws ``ScaleDuplicateResource`` exception if a project with the same name already exists.

Retrieve Project
^^^^^^^^^^^^^^^^

Retrieve a single Project. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#project-retrieval

.. code-block:: python

    project = client.get_project(project_name = "test_project")

The older ``param_dict`` attribute is now replaced with a method ``project.as_dict()`` to return a project's all attributes as a dictionary (JSON).

List Projects
^^^^^^^^^^^^^

This function does not take any arguments. Retrieve a list of every Project.
Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-list

.. code-block :: python

    counter = 0
    projects = client.projects()
    for project in projects:
        counter += 1
        print(f'Downloading project {counter} | {project.name} | {project.type}')

Update Project
^^^^^^^^^^^^^^

Creates a new version of the Project. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#project-update-parameters

.. code-block :: python

    data = client.update_project(
        project_name="test_project",
        patch=False,
        instruction="update: Please label all the stuff",
    )

Files
________

Files are a way of uploading local files directly to Scale storage or importing files before creating tasks.


Upload Files
^^^^^^^^^^^^^^

Upload a file. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#file-upload-1

.. code-block:: python

    with open(file_name, 'rb') as f:
        my_file = client.upload_file(
            file=f,
            project_name = "test_project",
        )

The ``file.attachment_url`` can be used in place of attachments in task payload.


.. code-block:: python

    my_file.as_dict()

    # {
    #  'attachment_url': 'scaledata://606e2a0a46102303a130949/8ac09a90-c143-4154-9a9b-6c35121396d1f',
    #  'created_at': '2021-06-17T21:56:53.825Z',
    #  'id': '8ac09d70-ca43-4354-9a4b-6c3591396d1f',
    #  'mime_type': 'image/png',
    #  'project_names': ['test_project'],
    #  'size': 340714,
    #  'updated_at': '2021-06-17T21:56:53.825Z'
    # }

Import Files
^^^^^^^^^^^^^^

Import a file from a URL. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#file-import-1

.. code-block:: python

    my_file = client.import_file(
        file_url="http://i.imgur.com/v4cBreD.jpg",
        project_name = "test_project",
    )


After the files are successfully uploaded to Scale's storage, you can access the URL as ``my_file.attachment_url``, which will have a prefix like ``scaledata://``.

The attribute can be passed to the task payloads, in the ``attachment`` parameter.

.. code-block:: python

  task_payload = dict(
      ...
      ...
      attachment_type = "image",
      attachment = my_file.attachment_url,  # scaledata://606e2a30949/89a90-c143-4154-9a9b-6c36d1f
      ...
      ...
  )

Example Scripts
_______________

A list of examples scripts for use.

* `cancel_batch.py`__ to concurrently cancel tasks in batches

__ https://github.com/scaleapi/scaleapi-python-client/blob/master/examples/cancel_batch.py

Evaluation tasks (For Scale Rapid projects only)
________________________________________________

Evaluation tasks are tasks that we know the answer to and are used to measure workers' performance internally to ensure the quality

Create Evaluation Task
^^^^^^^^^^^^^^^^^^^^^^

Create an evaluation task.

.. code-block:: python

    client.create_evaluation_task(TaskType, ...task parameters...)

Passing in the applicable values into the function definition. The applicable fields are the same as for create_task. Applicable fields for each task type can be found in `Scale's API documentation`__. Additionally an expected_response is required. An optional initial_response can be provided if it's for a review phase evaluation task.

__ https://docs.scale.com/reference

.. code-block:: python

    from scaleapi.tasks import TaskType

    expected_response = {
        "annotations": {
            "answer_reasonable": {
                "type": "category",
                "field_id": "answer_reasonable",
                "response": [
                    [
                        "no"
                    ]
                ]
            }
        }
    }

    initial_response = {
        "annotations": {
            "answer_reasonable": {
                "type": "category",
                "field_id": "answer_reasonable",
                "response": [
                    [
                        "yes"
                    ]
                ]
            }
        }
    }

    attachments = [
        {"type": "image", "content": "https://i.imgur.com/bGjrNzl.jpeg"}
    ]

    payload = dict(
        project = "test_project",
        attachments,
        initial_response=initial_response,
        expected_response=expected_response,
    )

    client.create_evaluation_task(TaskType.TextCollection, **payload)

Training tasks (For Scale Rapid projects only)
________________________________________________

Training tasks are used to onboard taskers onto your project

Create Training Task
^^^^^^^^^^^^^^^^^^^^^^

Create a training task.

.. code-block:: python

    client.create_training_task(TaskType, ...task parameters...)

Error handling
______________

If something went wrong while making API calls, then exceptions will be raised automatically
as a `ScaleException` parent type and child exceptions:

- ``ScaleInvalidRequest``: 400 - Bad Request -- The request was unacceptable, often due to missing a required parameter.
- ``ScaleUnauthorized``: 401 - Unauthorized -- No valid API key provided.
- ``ScaleNotEnabled``: 402 - Not enabled -- Please contact sales@scaleapi.com before creating this type of task.
- ``ScaleResourceNotFound``: 404 - Not Found -- The requested resource doesn't exist.
- ``ScaleDuplicateResource``: 409 - Conflict -- Object already exists with same name, idempotency key or unique_id.
- ``ScaleTooManyRequests``: 429 - Too Many Requests -- Too many requests hit the API too quickly.
- ``ScaleInternalError``: 500 - Internal Server Error -- We had a problem with our server. Try again later.
- ``ScaleServiceUnavailable``: 503 - Server Timeout From Request Queueing -- Try again later.
- ``ScaleTimeoutError``: 504 - Server Timeout Error -- Try again later.

Check out `Scale's API documentation <https://docs.scale.com/reference#errors>`_ for more details.

For example:

.. code-block:: python

    from scaleapi.exceptions import ScaleException

    try:
        client.create_task(TaskType.TextCollection, attachment="Some parameters are missing.")
    except ScaleException as err:
        print(err.code)  # 400
        print(err.message)  # Parameter is invalid, reason: "attachments" is required

Troubleshooting
_______________

If you notice any problems, please email us at support@scale.com.
