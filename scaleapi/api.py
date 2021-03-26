import platform
import urllib.parse

import requests

from ._version import __package_name__, __version__
from .exceptions import (
    ScaleDuplicateTask,
    ScaleException,
    ScaleInternalError,
    ScaleInvalidRequest,
    ScaleNotEnabled,
    ScaleResourceNotFound,
    ScaleTooManyRequests,
    ScaleUnauthorized,
)

SCALE_ENDPOINT = "https://api.scale.com/v1"


class Api(object):
    def __init__(self, api_key, user_agent_extension=None):
        if api_key == "" or api_key is None:
            raise ScaleException("Please provide a valid API Key.")

        self.api_key = api_key

        self._auth = (self.api_key, "")
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": self._generate_useragent(user_agent_extension),
        }

    def _request(
        self, method, endpoint, headers=None, auth=None, params=None, body=None
    ):
        """Generic request method with error handling."""

        url = f"{SCALE_ENDPOINT}/{endpoint}"
        error_message = None

        try:
            params = params or {}
            body = body or {}

            res = requests.request(
                method=method,
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=body,
            )

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as err:
            raise err

        if res.status_code == 200:
            return res.json()
        else:
            error_message = res.json().get("error", res.text)

            if res.status_code == 400:
                raise ScaleInvalidRequest(error_message, res.status_code)
            elif res.status_code == 401:
                raise ScaleUnauthorized(error_message, res.status_code)
            elif res.status_code == 402:
                raise ScaleNotEnabled(error_message, res.status_code)
            elif res.status_code == 404:
                raise ScaleResourceNotFound(error_message, res.status_code)
            elif res.status_code == 409:
                raise ScaleDuplicateTask(error_message, res.status_code)
            elif res.status_code == 429:
                raise ScaleTooManyRequests(error_message, res.status_code)
            elif res.status_code == 500:
                raise ScaleInternalError(error_message, res.status_code)
            else:
                raise ScaleException(error_message, res.status_code)

    def _get_request(self, endpoint, params=None):
        return self._request(
            "GET", endpoint, headers=self._headers, auth=self._auth, params=params
        )

    def _post_request(self, endpoint, body=None):
        return self._request(
            "POST", endpoint, headers=self._headers, auth=self._auth, body=body
        )

    @staticmethod
    def _generate_useragent(extension=None):
        python_version = platform.python_version()
        os_platform = platform.platform()

        user_agent = " ".join(
            filter(
                None,
                [
                    f"{__package_name__}/{__version__}",
                    f"Python/{python_version}",
                    f"OS/{os_platform}",
                    extension,
                ],
            )
        )
        return user_agent

    @staticmethod
    def quote_string(text):
        """`quote_string('a bc/def')` -> `a%20bc%2Fdef`

        Project and Batch names can be a part of URL, which causes
        an error in case of a special character used.
        Quotation assures the right object to be retrieved from API.
        """
        return urllib.parse.quote(text, safe="")
