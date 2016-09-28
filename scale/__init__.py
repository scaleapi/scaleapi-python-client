import requests

from . import tasks

DEFAULT_FIELDS = {'callback_url', 'instruction', 'urgency'}

class ScaleClient(object):
    def __init__(self, api_key, callback_key=None,
                 endpoint='https://api.scaleapi.com/v1/'):
        self.api_key = api_key
        self.callback_key = callback_key
        self.endpoint = endpoint

    def create_comparison_task(**kwargs):
        payload = generic_payload(kwargs)
        allowed_fields = DEFAULT_FIELDS + \
            {'attachment', 'attachment_type', 'categories', 'category_ids', 'allow_multiple'}
            if field in kwargs:
                payload[field] = kwargs[field]
        payload = {
            'callback_url': callback_url,
            'instruction': instruction,
        }
        return self._dotask(tasks.ComparisonTask(*args, **kwargs))

    def create_transcription_task(*args, **kwargs):
        return self._dotask(tasks.TranscriptionTask(*args, **kwargs))

    def create_phonecall_task(*args, **kwargs):
        return self._dotask(tasks.PhonecallTask(*args, **kwargs))

    def create_comparison_task(*args, **kwargs):
        return self._dotask(tasks.TranscriptionTask(*args, **kwargs))

    def create_annotation_task(*args, **kwargs):
        return self._dotask(tasks.AnnotationTask(*args, **kwargs))
