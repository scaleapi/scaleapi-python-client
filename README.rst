=====================
Scale AI | Python SDK
=====================

Installation
____________

.. code-block:: bash

    $ pip install --upgrade scaleapi

Note: We strongly suggest using `scaleapi` with Python version 2.7.9 or greater due to SSL issues with prior versions.

Usage
_____

.. code-block:: python

    import scaleapi
    client = scaleapi.ScaleClient('YOUR_API_KEY_HERE')

Tasks
_____

Most of these methods will return a `scaleapi.Task` object, which will contain information
about the json response (task_id, status, etc.).

Any parameter available in `Scale's API documentation`__ can be passed as an argument option with the corresponding type.

__ https://docs.scale.com/reference#task-object

The following endpoints for tasks are available:

Create Task
^^^^^^^^^^^

This method can be used for any Scale supported task type using the following format:

.. code-block:: python

    client.create_{{Task Type}}_task(...)

Passing in the applicable values into the function definition. The applicable fields and further information for each task type can be found in `Scale's API documentation`__.

__ https://docs.scale.com/reference#general-image-annotation

.. code-block:: python

    client.create_imageannotation_task(
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

Retrieve task
^^^^^^^^^^^^^

Retrieve a task given its id. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#retrieve-tasks

.. code-block :: python

    task = client.fetch_task('asdfasdfasdfasdfasdfasdf')
    print(task.status)  // Task status ('pending', 'completed', 'error', 'canceled')
    print(task.response) // If task is complete

List Tasks
^^^^^^^^^^

Retrieve a list of tasks, with optional filter by start and end date/time. Paginated with `next_token`. The return value is a `scaleapi.Tasklist`, which acts as a list, but also has fields for the total number of tasks, the limit and offset, and whether or not there's more. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#list-multiple-tasks

.. code-block :: python

    next_token = None;
    counter = 0
    all_tasks =[]
    while True:
        tasks = client.tasks(
            start_time = "2020-09-08",
            end_time = "2021-01-01",
            customer_review_status = "accepted",
            next_token = next_token,
        )
        for task in tasks:
            counter += 1
            print('Downloading Task %s | %s' % (counter, task.task_id))
            all_tasks.append(task.__dict__['param_dict'])
        next_token = tasks.next_token
        if next_token is None:
            break
    print(all_tasks)

Cancel Task
^^^^^^^^^^^

Cancel a task given its id if work has not stared on the task (task status is `queued` in the UI). Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#cancel-task

.. code-block :: python

    task = client.cancel_task('asdfasdfasdfasdfasdfasdf')

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

Retrieve Batch
^^^^^^^^^^^^^^

Retrieve a single Batch. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-retrieval

.. code-block:: python

    client.get_batch( batch_name = "batch_name_01_07_2021" )

List Batches
^^^^^^^^^^^^

Retrieve a list of Batches. Check out `Scale's API documentation`__ for more information.

__ https://docs.scale.com/reference#batch-list

.. code-block :: python

    next_token = None;
    counter = 0
    all_batchs =[]
    while True:
        batches = client.list_batches(
            status = "completed"
        )
        for batch in batches:
            counter += 1
            print('Downloading Batch %s | %s | %s' % (counter, batch.name, batch.param_dict['status']))
            all_batchs.append(batch.__dict__['param_dict'])
        next_token = batches.next_token
        if next_token is None:
            break
    print(all_batchs)

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
        print('Downloading project %s | %s | %s' % (counter, project['name'], project['type']))

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
as a `scaleapi.ScaleException` or `scaleapi.ScaleInvalidRequest` runtime error. For example:

.. code-block:: python

    try
        client.create_categorization_task('Some parameters are missing.')
    except scaleapi.ValidationError as e:
        print(e.code)  # 400
        print(e.message)  # missing param X

Troubleshooting
_______________

If you notice any problems, please email us at support@scale.com.
