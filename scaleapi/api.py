import platform
import urllib.parse

import requests
from requests.adapters import HTTPAdapter, Retry

from ._version import __package_name__, __version__
from .exceptions import (
    ScaleDuplicateTask,
    ScaleException,
    ScaleInternalError,
    ScaleInvalidRequest,
    ScaleNotEnabled,
    ScaleResourceNotFound,
    ScaleTimeoutError,
    ScaleTooManyRequests,
    ScaleUnauthorized,
)

SCALE_ENDPOINT = "https://api.scale.com/v1"
NUM_OF_RETRIES = 3


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
        """Generic HTTP request method with error handling."""

        url = f"{SCALE_ENDPOINT}/{endpoint}"
        error_message = None

        https = requests.Session()
        retry_strategy = Retry(
            total=NUM_OF_RETRIES,
            backoff_factor=2,  # Will wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 504],
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        https.mount("https://", adapter)

        try:
            params = params or {}
            body = body or {}

            res = https.request(
                method=method,
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=body,
            )

            if res.status_code == 200:
                return res.json()
            else:
                try:
                    error_message = res.json().get("error", res.text)
                except Exception:
                    error_message = res.text

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
                elif res.status_code == 504:
                    raise ScaleTimeoutError(error_message, res.status_code)
                else:
                    raise ScaleException(error_message, res.status_code)

        except (requests.exceptions.Timeout, requests.exceptions.RetryError,) as err:
            raise ScaleException(err)

    def _get_request(self, endpoint, params=None):
        """Generic GET Request Wrapper"""
        return self._request(
            "GET", endpoint, headers=self._headers, auth=self._auth, params=params
        )

    def _post_request(self, endpoint, body=None):
        """Generic POST Request Wrapper"""
        return self._request(
            "POST", endpoint, headers=self._headers, auth=self._auth, body=body
        )

    @staticmethod
    def _generate_useragent(extension: str = None) -> str:
        """Generates UserAgent parameter with module, Python
        and OS details

        Args:
            extension (str, optional): Option to extend UserAgent
            with source system

        Returns:
            str: Generated UserAgent parameter with platform versions
        """
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
    def quote_string(text: str) -> str:
        """Project and Batch names can be a part of URL, which causes
        an error in case of a special character used.
        Quotation assures the right object to be retrieved from API.

        `quote_string('a bc/def')` -> `a%20bc%2Fdef`

        Args:
            text (str): Input text to be quoted

        Returns:
            str: Quoted text in return
        """
        return urllib.parse.quote(text, safe="")
