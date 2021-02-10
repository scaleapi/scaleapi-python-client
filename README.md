===================
Scale AI | Python SDK
===================

# Installation

.. code-block:: bash

    $ pip install --upgrade scaleapi

Note: We strongly suggest using `scaleapi` with Python version 2.7.9 or greater due to SSL issues with prior versions.

# Usage

.. code-block:: python

    import scaleapi
    client = scaleapi.ScaleClient('YOUR_API_KEY_HERE')

# Tasks

Most of these methods will return a `scaleapi.Task` object, which will contain information
about the json response (task_id, status...).

Any parameter available in the documentation\_ can be passed as an argument option with the corresponding type.

.. \_documentation: https://docs.scale.com/reference#task-object

The following endpoints for tasks are available:

## Create Task

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#general-image-annotation

.. code-block:: python

    client.create_task(
        task_type = 'imageannotation',
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

## Retrieve task

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#retrieve-tasks

Retrieve a task given its id.

.. code-block :: python

    task = client.fetch_task('asdfasdfasdfasdfasdfasdf')
    print(task.status)  // Task status ('pending', 'completed', 'error', 'canceled')
    print(task.response) // If task is complete

## List Tasks

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#list-multiple-tasks

Retrieve a list of tasks, with optional filter by stand and end date/type. Paginated with `next_token`. The return value is a `scaleapi.Tasklist`, which acts as a list, but also has fields for the total number of tasks, the limit and offset, and whether or not there's more.

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

## Cancel Task

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#cancel-task

Cancel a task given its id if work has not stared on the task (task status is "que).

.. code-block :: python

    task = client.cancel_task('asdfasdfasdfasdfasdfasdf')

# Batches

## Create Batch

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#batch-creation

.. code-block:: python

    client.create_batch(
        project = 'test_project',
        callback = "http://www.example.com/callback",
        name = 'batch_name_01_07_2021'
    )

## Finalize Batch

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#batch-finalization

.. code-block:: python

    client.create_batch(batch_name = 'batch_name_01_07_2021')

## Check Batch Status

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#batch-status

.. code-block:: python

    client.batch_status(batch_name = 'batch_name_01_07_2021')

## Retrieve Batch

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#batch-retrieval

.. code-block:: python

    client.get_batch( batch_name = "batch_name_01_07_2021" )

## List Batchs

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#batch-list

Retrieve a list of batches

.. code-block :: python

    next_token = None;
    counter = 0
    all_batchs =[]
    while True:
        batches = client.batches(
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

# Projects

## Create Project

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#project-creation

.. code-block:: python

    client.create_project(
        project_name = 'test_project',
        type = 'imageannotation,
        params = {'instruction':'Please label the kittens'}
    )

## Retrieve Project

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#project-retrieval

.. code-block:: python

    client.get_projet(project_name = 'test_project')

## List Projects

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#batch-list

Retrieve a list of batches

.. code-block :: python

    counter = 0
    projects = client.projects()
    for project in projects:
        counter += 1
        print('Downloading project %s | %s | %s' % (counter, project['name'], project['type']))

## Update Project

Check `this`\_\_ for further information.

\_\_ https://docs.scale.com/reference#project-update-parameters

Retrieve a list of batches

.. code-block :: python

    data = client.update_project(
        project_name='test_project',
        pathc = false,
        instruction='update: Please label all the stuff',

)

# Error handling

If something went wrong while making API calls, then exceptions will be raised automatically
as a `scaleapi.ScaleException` or `scaleapi.ScaleInvalidRequest` runtime error. For example:

.. code-block:: python

    try
        client.create_categorization_task('Some parameters are missing.')
    except scaleapi.ValidationError as e:
        print(e.code)  # 400
        print(e.message)  # missing param X

# Troubleshooting

If you notice any problems, please email us at support@scale.com.