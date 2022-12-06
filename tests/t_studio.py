import os
import time
import uuid

import scaleapi

# Testing with live key since Studio endpoints require live projects

client = scaleapi.ScaleClient(os.environ["JF_STUDIO_KEY"])

test_project = "vfps"
# test teammates

# test list_teammates
teammates = client.list_teammates()
for teammate in teammates:
    print("Testing list_teammates:")
    print(teammate.as_dict())
    break

# test invite_teammate
test_email_invite = f"jon.feng+sdk_test_{str(uuid.uuid4())[-4:]}@scale.com"
new_teammates = client.invite_teammates(
    [test_email_invite], scaleapi.TeammateRole.Member
)

for new_teammate in new_teammates:
    if new_teammate.email == test_email_invite:
        print("testing invite teammate:")
        print(new_teammate.as_dict())

time.sleep(20)

updated_teammates = client.update_teammates_role(
    [test_email_invite], scaleapi.TeammateRole.Manager
)

for updated_teammate in updated_teammates:
    if updated_teammate.email == test_email_invite:
        print("testing update teammate:")
        print(updated_teammate.as_dict())

# test assignments
assignments = client.list_studio_assignments()
print("Testing listing assignments:")
print(assignments["jon.feng@scale.com"])

added_assignment = client.add_studio_assignments([test_email_invite], [test_project])

print("Testing adding assignment:")
print(added_assignment.get(test_email_invite))

removed_assignment = client.remove_studio_assignments(
    [test_email_invite], [test_project]
)
print("Testing removing assignment:")
print(removed_assignment.get(test_email_invite))
# re-add assignment for next step
added_assignment = client.add_studio_assignments([test_email_invite], [test_project])

project_group_name = "sdk-testing"
added_project_group = client.create_project_group(
    test_project, [test_email_invite], project_group_name
)

print("Test creating project group:")
print(added_project_group.as_dict())

list_project_group = client.list_project_groups(test_project)
print("Test listing project groups")
print(list_project_group)

updated_project_group = client.update_project_group(
    test_project, project_group_name, [], [test_email_invite]
)
print("Test removing project group")
print(updated_project_group.as_dict())

re_updated_project_group = client.update_project_group(
    test_project, project_group_name, [test_email_invite], []
)
print("Test adding back project group")
print(re_updated_project_group.as_dict())

studio_batches = client.list_studio_batches()
print("Test studio batches")
print(studio_batches)

test_batch = "testing_vfps"

assigned_studio_batch = client.assign_studio_batches(test_batch, [project_group_name])
print("Test studio batch assignment")
print(assigned_studio_batch)

studio_batch_priority = client.set_studio_batches_priorities(
    list(map(lambda sb: sb.name, studio_batches))
)
print("Test set studio batch priority")
print(studio_batch_priority)

reset_studio_batch_prioprity = client.reset_studio_batches_priorities()
print("Test reset studio batch priority")
print(reset_studio_batch_prioprity)
