import scaleapi

nofel_key = "live_ecf03a873847470e8ec59f20b09276b4"
# stanford_key = 'live_c23b58e102b044bd9e854436a9c64a18'
client = scaleapi.ScaleClient(nofel_key)
attachment = 'https://p-ZmFjlye.t1.n0.cdn.getcloudapp.com/items/eDuwnDY4/f5fa720d-6c2c-4ef1-8aed-59e7f1021db6.jpeg?source=client&v=1700792a861cc7747f10f1c36e5ba057'

# task = client.create_task(
#   task_type= 'imageannotation',
#   callback_url= "http://www.example.com/callback",
#   attachment= attachment,
#   batch = 'batch_name_01_07_2021',
#   # attachment = "s3://scale-sales-uploads/TRI/2d_bbox_sample.mp4",
#   # attachment_type = 'video',
#   project = 'nofel_test_project',
# )

# print(f'attachment: {attachment}')
# print(f'frame_rate: {frame_rate}')

# data = client.update_project(
#   project_name='nofel_test_project',
#   instruction='update: Please label all the stuff',
#   geometries={'box':{'objects_to_annotate':['update_label']}}
# )

# project = client.create_project(
#         project_name = 'nofel_test_project',
#         type = 'imageannotation',
#         params = {'instruction':'Please label the stuff'}
#     )

batch = client.get_projet(
        project_name = 'nofel_test_project',
    )

print(batch.param_dict['type'])


# counter = 0
# projects = client.projects()
# for project in projects:
#     counter += 1
#     print('Downloading project %s | %s | %s' % (counter, project['name'], project['type']))
