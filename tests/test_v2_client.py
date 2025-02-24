# # pylint: disable=missing-function-docstring
# import os

# import scaleapi
# from scaleapi.exceptions import (
#     ScaleResourceNotFound,
# )
# from scaleapi.tasks import TaskType

# # The test project needs to be setup before running these tests
# # Alternatively, you can use an existing project
# TEST_PROJECT_NAME = "scaleapi-python-sdk-v2-test"

# try:
#     print(f"SDK Version: {scaleapi.__version__}")
#     test_api_key = os.environ["SCALE_TEST_API_KEY"]

#     if test_api_key.startswith("test_") or \
#         test_api_key.endswith("|test"):
#         client = scaleapi.ScaleClient(test_api_key, "pytest")
#     else:
#         raise Exception("Please provide a valid"
#           + "TEST environment key.")
# except KeyError as err:
#     raise Exception(
#         "Please set the environment variable"
#           + "SCALE_TEST_API_KEY to run tests."
#     ) from err

# try:
#     project = client.get_project(TEST_PROJECT_NAME)
# except ScaleResourceNotFound:
#     res = client.create_project(project_name=TEST_PROJECT_NAME, \
#       task_type=TaskType.Chat)


# def make_a_chat_task():
#     args = {
#         "project": TEST_PROJECT_NAME,
#         "instruction": "Task instructions.",
#         "params": {
#             "before": [],
#             "turn": [],
#             "after": [],
#         },
#         "template_variables": {
#             "some_key": "some_value",
#             "languageCode": "en_US",
#         },
#     }
#     return client.create_task(TaskType.Chat, **args)


# def test_v2_get_tasks():
#     new_task = make_a_chat_task()
#     tasks = client.v2_get_tasks(
#         project_name=TEST_PROJECT_NAME,
#     )
#     task_ids = {task.task_id for task in tasks}
#     assert new_task.id in task_ids


# def test_v2_get_task():
#     new_task = make_a_chat_task()
#     task = client.v2.get_task(task_id=new_task.id)
#     assert task.task_id == new_task.id
