from typing import Dict


class ScaleException(Exception):
    """Generic ScaleException class"""

    code = None

    def __init__(self, message, errcode=None):
        if not message:
            message = type(self).__name__
        self.message = message

        if errcode:
            self.code = errcode

        if self.code:
            super().__init__(f"<Response [{self.code}]> {message}")
        else:
            super().__init__(f"<Response> {message}")


class ScaleInvalidRequest(ScaleException):
    """400 - Bad Request -- The request was unacceptable,
    often due to missing a required parameter.
    """

    code = 400


class ScaleUnauthorized(ScaleException):
    """401 - Unauthorized -- No valid API key provided."""

    code = 401


class ScaleNotEnabled(ScaleException):
    """402 - Not enabled -- Please contact sales@scaleapi.com before
    creating this type of task.
    """

    code = 402


class ScaleResourceNotFound(ScaleException):
    """404 - Not Found -- The requested resource doesn't exist."""

    code = 404


class ScaleDuplicateTask(ScaleException):
    """409 - Conflict -- The provided idempotency key or unique_id is
    already in use for a different request.
    """

    code = 409


class ScaleTooManyRequests(ScaleException):
    """429 - Too Many Requests -- Too many requests hit the API
    too quickly.
    """

    code = 429


class ScaleInternalError(ScaleException):
    """500 - Internal Server Error -- We had a problem with our server.
    Try again later.
    """

    code = 500


class ScaleServiceUnavailable(ScaleException):
    """503 - Server Timeout From Request Queueing -- Try again later."""

    code = 503


class ScaleTimeoutError(ScaleException):
    """504 - Server Timeout Error -- Try again later."""

    code = 504


ExceptionMap: Dict[int, ScaleException] = {
    ScaleInvalidRequest.code: ScaleInvalidRequest,
    ScaleUnauthorized.code: ScaleUnauthorized,
    ScaleNotEnabled.code: ScaleNotEnabled,
    ScaleResourceNotFound.code: ScaleResourceNotFound,
    ScaleDuplicateTask.code: ScaleDuplicateTask,
    ScaleTooManyRequests.code: ScaleTooManyRequests,
    ScaleInternalError.code: ScaleInternalError,
    ScaleTimeoutError.code: ScaleTimeoutError,
    ScaleServiceUnavailable.code: ScaleServiceUnavailable,
}
