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

If you need to use a proxy to connect Scale API, you can feed ``proxies``, ``cert`` and ``verify`` attributes of the python ``requests`` package during the client initialization.
Proxy support is available with SDK version 2.14.0 and beyond.

`Documentation of Proxies usage in requests package`__

__ https://requests.readthedocs.io/en/latest/user/advanced/#proxies

.. code-block:: python

    proxies = { 'https': 'http://10.10.1.10:1080' }

    client = scaleapi.ScaleClient(
                api_key="YOUR_API_KEY_HERE",
                proxies=proxies,
                cert='/path/client.cert',
                verify=True
            )

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

If you use the ``limited_response = True`` filter in ``get_tasks()``, you will only receive the following attributes: ``task_id``, ``status``, ``metadata``, ``project`` and ``otherVersion``.

Retrieve List of Tasks
^^^^^^^^^^^^^^^^^^^^^^

Retrieve a list of `Task` objects, with filters for: ``project_name``, ``batch_name``, ``type``, ``status``,
``review_status``, ``unique_id``, ``completed_after``, ``completed_before``, ``updated_after``, ``updated_before``,
``created_after``, ``created_before``, ``tags``, ``limited_response`` and ``limit``.

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
    print(f"{len(task_list)} tasks retrieved")

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


Audit a Task
^^^^^^^^^^^^

This method allows you to ``accept`` or ``reject`` completed tasks, along with support for adding comments about the reason for the given audit status, mirroring our Audit UI.
Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/audit-a-task

.. code-block :: python

    # Accept a completed task by submitting an audit
    client.audit_task('30553edd0b6a93f8f05f0fee', True)

    # Reject a completed task by submitting a comment with the audit
    client.audit_task('30553edd0b6a93f8f05f0fee', False, 'Rejected due to quality')

    # audit() is also available on Task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    task.audit(True)


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

Set A Task's Tags
^^^^^^^^^^^^^^^^^^^^^^^^^

Set a given task's ``tags``. This will replace all existing tags on a task. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/setting-tags

.. code-block :: python

    # set a list of tags on a task by specifying task id
    new_tags = ["tag1", "tag2", "tag3"]
    task = client.set_task_tags('30553edd0b6a93f8f05f0fee', new_tags)

    # set a list of tags on a task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    new_tags = ["tag1", "tag2", "tag3"]
    task.set_tags(new_tags)

Add Tags to A Task
^^^^^^^^^^^^^^^^^^^^^^^^^

Add ``tags`` to a given task. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/adding-tags

.. code-block :: python

    # add a list of tags on a task by specifying task id
    tags_to_add = ["tag4", "tag5"]
    task = client.add_task_tags('30553edd0b6a93f8f05f0fee', tags_to_add)

    # add a list of tags on a task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    tags_to_add = ["tag4", "tag5"]
    task.add_tags(tags_to_add)

Delete Tags from A Task
^^^^^^^^^^^^^^^^^^^^^^^^^

Delete ``tags`` from a given task. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference/deleting-tags

.. code-block :: python

    # delete a list of tags on a task by specifying task id
    tags_to_delete = ["tag1", "tag2"]
    task = client.delete_task_tags('30553edd0b6a93f8f05f0fee', tags_to_delete)

    # delete a list of tags on a task object
    task = client.get_task('30553edd0b6a93f8f05f0fee')
    tags_to_delete = ["tag1", "tag2"]
    task.delete_tags(tags_to_delete)

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

Retrieve a list of Batches. Optional parameters are ``project_name``, ``batch_status``, ``exclude_archived``, ``created_after`` and ``created_before``.

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

Manage Teammates
________________

Manage the members of your Scale team via API. Check out `Scale Team API Documentation`__ for more information.

__ https://docs.scale.com/reference/teams-overview

List Teammates
^^^^^^^^^^^^^^

Lists all teammates in your Scale team.
Returns all teammates in a List of Teammate objects.

.. code-block:: python

    teammates = client.list_teammates()

Invite Teammate
^^^^^^^^^^^^^^^

Invites a list of email strings to your team with the provided role.
The available teammate roles are: 'labeler', 'member', or 'manager'.
Returns all teammates in a List of Teammate objects.

.. code-block:: python

    from scaleapi import TeammateRole

    teammates = client.invite_teammates(['email1@example.com', 'email2@example.com'], TeammateRole.Member)

Update Teammate Role
^^^^^^^^^^^^^^^^^^^^^

Updates a list of emails of your Scale team members with the new role.
The available teammate roles are: 'labeler', 'member', or 'manager'.
Returns all teammates in a List of Teammate objects.

.. code-block python

    from scaleapi import TeammateRole

    teammates = client.update_teammates_role(['email1@example.com', 'email2@example.com'], TeammateRole.Manager)

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

Studio Assignments (For Scale Studio only)
__________________________________________

Manage project assignments for your labelers.

List All Assignments
^^^^^^^^^^^^^^^^^^^^

Lists all your Scale team members and the projects they are assigned to.
Returns a dictionary of all teammate assignments with keys as 'emails' of each teammate, and values as a list of project names the teammate are assigned to.

.. code-block:: python

    assignments = client.list_studio_assignments()
    my_assignment = assignments.get('my-email@example.com')

Add Studio Assignment
^^^^^^^^^^^^^^^^^^^^^

Assigns provided projects to specified teammate emails.

Accepts a list of emails and a list of projects.

Returns a dictionary of all teammate assignments with keys as 'emails' of each teammate, and values as a list of project names the teammate are assigned to.

.. code-block:: python

    assignments = client.add_studio_assignments(['email1@example.com', 'email2@example.com'], ['project 1', 'project 2'])


Remove Studio Assignment
^^^^^^^^^^^^^^^^^^^^^^^^

Removes provided projects from specified teammate emails.

Accepts a list of emails and a list of projects.

Returns a dictionary of all teammate assignments with keys as 'emails' of each teammate, and values as a list of project names the teammate are assigned to.

.. code-block:: python

    assignments = client.remove_studio_assignments(['email1@example.com', 'email2@example.com'], ['project 1', 'project 2'])

Studio Project Groups (For Scale Studio Only)
_____________________________________________

Manage groups of labelers in our project by using Studio Project Groups.

List Studio Project Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns all labeler groups for the specified project.

.. code-block:: python

    list_project_group = client.list_project_groups('project_name')

Add Studio Project Group
^^^^^^^^^^^^^^^^^^^^^^^^

Creates a project group with the provided group_name for the specified project and adds the provided teammate emails to the new project group. The team members must be assigned to the specified project in order to be added to the new group.

Returns the created StudioProjectGroup object.

.. code-block:: python

    added_project_group = client.create_project_group(
        'project_name', ['email1@example.com'], 'project_group_name'
    )

Update Studio Project Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assign or remove teammates from a project group.

Returns the updated StudioProjectGroup object.

.. code-block:: python

    updated_project_group = client.update_project_group(
        'project_name', 'project_group_name', ['emails_to_add'], ['emails_to_remove']
    )

Studio Batches (For Scale Studio Only)
_______________________________________

Get information about your pending Studio batches.

List Studio Batches
^^^^^^^^^^^^^^^^^^^

Returns a list of StudioBatch objects for all pending Studio batches.

.. code-block:: python

    studio_batches = client.list_studio_batches()

Assign Studio Batches
^^^^^^^^^^^^^^^^^^^^^^

Sets labeler group assignment for the specified batch.

Returns a StudioBatch object for the specified batch.

.. code-block:: python

    assigned_studio_batch = client.assign_studio_batches('batch_name', ['project_group_name'])

Set Studio Batches Priority
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets the order to prioritize your pending Studio batches. You must include all pending studio batches in the List.

Returns a List of StudioBatch objects in the new order.

.. code-block:: python

    studio_batch_priority = client.set_studio_batches_priorities(
        ['pending_batch_1', 'pending_batch_2', 'pending_batch_3']
    )

Reset Studio Batches Priority
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Resets the order of your Studio batches to the default order, which prioritizes older batches first.

Returns a List of StudioBatch objects in the new order.

.. code-block:: python

    reset_studio_batch_prioprity = client.reset_studio_batches_priorities()


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

If you notice any problems, please contact our support via Intercom by logging into your dashboard, or, if you are Enterprise, by contacting your Engagement Manager.
