=====================
Scale AI | Python SDK
=====================

If you use earlier versions of the SDK, please refer to `v1.0.4 documentation <https://github.com/scaleapi/scaleapi-python-client/blob/release-1.0.4/README.rst>`_.


Migration Guide to v2.x
________________________

If you are migrating from v0.x or v1.x,  this guide explains how to update your application for compatibility with v2.x. We recommend migrating as soon as possible to ensure that your application is unaffected.

Creating New Tasks
^^^^^^^^^^^^^^^^^^
Methods with task types such as ``create_imageannotation_task, create_textcollection_task`` etc. are deprecated.

Creating a new task is now unified under the ``create_task(TaskType, ...)`` method. Please review `Create Task`_ section for more details.


.. code-block:: python

    # Deprecated
    client.create_imageannotation_task(
        project = 'test_project',
        instruction= "Draw a box around each baby cow and big cow.",
        ...
    )

    # New Method
    from scaleapi.tasks import TaskType
    client.create_task(
        TaskType.ImageAnnotation,
        project = 'test_project',
        instruction= "Draw a box around each baby cow and big cow.",
        ...
    )

Retrieving Tasks
^^^^^^^^^^^^^^^^
A new generator method is introduced to retrieve a list of tasks with all available parameters. The new method handles pagination and tokens: `tasks_all(...)`. You can have a simpler code by replacing `tasks()` loops with pagination. 

Please refer to `List Tasks`_ for more details.

Accessing Attributes (Task, Batch, Project)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The old `param_dict` attribute is now replaced with a method `as_dict()` to return an object's attributes as a dictionary.

First-level attributes of Task can also be accessed with `.` annotation as `task.as_dict()["status"]` is equal to `task.status`. 
Other examples are `task.type, task.params, task.response["annotations"]`.

Task Count Summary of Batches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Attributes of Batch `pending, completed, error, canceled` are replaced with `tasks_pending, tasks_completed, tasks_error, tasks_canceled` respectively.

Deprecated Methods
^^^^^^^^^^^^^^^^^^
- `fetch_task()` replaced with `get_task()`
- `list_batches()`  replaced with `batches()`

Enabled Auto-Retry
^^^^^^^^^^^^^^^^^^
SDK now enables auto-retry in case of a TimeOut (504) or TooManyRequests (429) occurs.

New Exceptions
^^^^^^^^^^^^^^
New error types are introduces if you want to handle specific exception cases.
`ScaleInvalidRequest, ScaleUnauthorized, ScaleNotEnabled, ScaleResourceNotFound, ScaleDuplicateTask, ScaleTooManyRequests, ScaleInternalError` and `ScaleTimeoutError`.
All new error types are child of the existing `ScaleException` which can be used to handle all cases.


Installation
____________

.. code-block:: bash

    $ pip install --upgrade scaleapi

Usage
_____

.. code-block:: python

    import scaleapi
    client = scaleapi.ScaleClient('YOUR_API_KEY_HERE')

Tasks
_____

Most of these methods will return a `scaleapi.Task` object, which will contain information
about the json response (task_id, status, params, response etc.).

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
    
    client.create_task(
        TaskType.ImageAnnotation,
        project = 'test_project',
        callback_url = "http://www.example.com/callback",
        instruction= "Draw a box around each baby cow and big cow.",
        attachment_type = "image",
        attachment = "http://i.imgur.com/v4cBreD.jpg",
        geometries = {
            "box": {
              "objects_to_annotate": ["Baby Cow", "Big Cow"],
              "min_height": 10,
              "min_width": 10
            }
        }
    )
    
Retrieve a task
^^^^^^^^^^^^^^^

Retrieve a task given its id. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#retrieve-tasks

.. code-block :: python

    task = client.get_task('30553edd0b6a93f8f05f0fee')
    print(task.status)  # Task status ('pending', 'completed', 'error', 'canceled')
    print(task.response) # If task is complete

List Tasks
^^^^^^^^^^

Retrieve a list of `Task` objects, with optional filters for: `project_name, batch_name, type, status, review_status, unique_id, completed_after, completed_before, updated_after, updated_before, created_after, created_before` and `tags`. 

This method is a generator and yields tasks. It can be wrapped in a `list` statement if a Task list is needed.

Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#list-multiple-tasks

.. code-block :: python
    
    from scaleapi.tasks import TaskReviewStatus, TaskStatus

    tasks = client.tasks_all(
        project_name = "My Project",
        created_after = "2020-09-08",
        completed_before = "2021-04-01",
        status = TaskStatus.Completed,
        review_status = TaskReviewStatus.Accepted
    )
    
    for task in tasks:
        # Download task or do something!
        print(task.task_id)
    
    # Alternative for accessing as a Task list
    task_list = list(tasks) 
    print(f"{len(task_list))} tasks retrieved")

Cancel Task
^^^^^^^^^^^

Cancel a task given its id if work has not started on the task (task status is `Queued` in the UI). Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#cancel-task

.. code-block :: python

    task = client.cancel_task('30553edd0b6a93f8f05f0fee')

Batches
_______

Create Batch
^^^^^^^^^^^^

Create a new Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-creation

.. code-block:: python

    client.create_batch(
        project = 'test_project',
        callback = "http://www.example.com/callback",
        name = 'batch_name_01_07_2021'
    )

Finalize Batch
^^^^^^^^^^^^^^^

Finalize a Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-finalization

.. code-block:: python

    client.finalize_batch(batch_name = 'batch_name_01_07_2021')

Check Batch Status
^^^^^^^^^^^^^^^^^^

Get the status of a Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-status

.. code-block:: python

    client.batch_status(batch_name = 'batch_name_01_07_2021')

    # Alternative via Batch.get_status()
    batch = client.get_batch('batch_name_01_07_2021')
    batch.get_status() # Refreshes tasks_{status} attributes of Batch
    print(batch.tasks_pending, batch.tasks_completed)

Retrieve Batch
^^^^^^^^^^^^^^

Retrieve a single Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-retrieval

.. code-block:: python

    client.get_batch(batch_name = 'batch_name_01_07_2021')

List Batches
^^^^^^^^^^^^

Retrieve a list of Batches. Optional parameters are `project_name, batch_status, created_after, created_before`. 

Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-list

.. code-block :: python

    from scaleapi.batches import BatchStatus
    
    batches = client.batches_all(
        batch_status=BatchStatus.Completed,
        created_after = "2020-09-08"
    )    
    
    counter = 0
    for batch in batches:
        counter += 1
        print(f'Downloading batch {counter} | {batch.name} | {batch.project}')

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

    client.create_project(
        project_name = 'test_project',
        type = 'imageannotation,
        params = {'instruction':'Please label the kittens'}
    )

Retrieve Project
^^^^^^^^^^^^^^^^

Retrieve a single Project. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#project-retrieval

.. code-block:: python

    client.get_project(project_name = 'test_project')

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
        print(f'Downloading project {counter} | {project.name} | { project.type}')

Update Project
^^^^^^^^^^^^^^

Creates a new version of the Project. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#project-update-parameters

.. code-block :: python

    data = client.update_project(
        project_name='test_project',
        pathc = false,
        instruction='update: Please label all the stuff',
    )

Error handling
______________

If something went wrong while making API calls, then exceptions will be raised automatically
as a `scaleapi.ScaleException` parent type and child exceptions like: `ScaleInvalidRequest, ScaleUnauthorized, ScaleNotEnabled, ScaleResourceNotFound, ScaleDuplicateTask, ScaleTooManyRequests, ScaleInternalError` and `ScaleTimeoutError`.

For example:

.. code-block:: python

    try:
        client.create_task(TaskType.TextCollection, attachment='Some parameters are missing.')
    except ScaleException as err:
        print(err.code)  # 400
        print(err.message)  # Parameters is invalid, reason: "attachments" is required
    
Troubleshooting
_______________

If you notice any problems, please email us at support@scale.com.