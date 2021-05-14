import platform
import urllib.parse

import requests
from requests.adapters import HTTPAdapter, Response, Retry

from ._version import __package_name__, __version__
from .exceptions import ExceptionMap, ScaleException

SCALE_ENDPOINT = "https://api.scale.com/v1"

# Parameters for HTTP retry
HTTP_TOTAL_RETRIES = 3  # Number of total retries
HTTP_RETRY_BACKOFF_FACTOR = 2  # Wait 1, 2, 4 seconds between retries
HTTP_STATUS_FORCE_LIST = [408, 429] + list(range(500, 531))
HTTP_RETRY_ALLOWED_METHODS = frozenset({"GET", "POST"})


class Api:
    """Internal Api reference for handling http operations"""

    def __init__(self, api_key, user_agent_extension=None):
        if api_key == "" or api_key is None:
            raise ScaleException("Please provide a valid API Key.")

        self.api_key = api_key

        self._auth = (self.api_key, "")
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": self._generate_useragent(user_agent_extension),
        }
        self._headers_multipart_form_data = {
            "User-Agent": self._generate_useragent(user_agent_extension),
        }

    @staticmethod
    def _http_request(
        method,
        url,
        headers=None,
        auth=None,
        params=None,
        body=None,
        files=None,
        data=None,
    ) -> Response:

        https = requests.Session()
        retry_strategy = Retry(
            total=HTTP_TOTAL_RETRIES,
            backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
            status_forcelist=HTTP_STATUS_FORCE_LIST,
            allowed_methods=HTTP_RETRY_ALLOWED_METHODS,
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
                files=files,
                data=data,
            )

            return res
        except Exception as err:
            raise ScaleException(err) from err

    @staticmethod
    def _raise_on_respose(res: Response):

        try:
            message = res.json().get("error", res.text)
        except ValueError:
            message = res.text

        exception = ExceptionMap.get(res.status_code, ScaleException)
        raise exception(message, res.status_code)

    def _api_request(
        self,
        method,
        endpoint,
        headers=None,
        auth=None,
        params=None,
        body=None,
        files=None,
        data=None,
    ):
        """Generic HTTP request method with error handling."""

        url = f"{SCALE_ENDPOINT}/{endpoint}"

        res = self._http_request(method, url, headers, auth, params, body, files, data)

        json = None
        if res.status_code == 200:
            json = res.json()
        else:
            self._raise_on_respose(res)

        return json

    def get_request(self, endpoint, params=None):
        """Generic GET Request Wrapper"""
        return self._api_request(
            "GET", endpoint, headers=self._headers, auth=self._auth, params=params
        )

    def post_request(self, endpoint, body=None, files=None, data=None):
        """Generic POST Request Wrapper"""
        return self._api_request(
            "POST",
            endpoint,
            headers=self._headers
            if files is None
            else self._headers_multipart_form_data,
            auth=self._auth,
            body=body,
            files=files,
            data=data,
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
