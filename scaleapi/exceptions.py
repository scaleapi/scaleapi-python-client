class ScaleException(Exception):
    def __init__(self, message, errcode=None):
        self.code = errcode
        if errcode:
            super(ScaleException, self).__init__(f"<Response [{errcode}]> {message}")
        else:
            super(ScaleException, self).__init__(f"<Response> {message}")


class ScaleInvalidRequest(ScaleException):
    """400 - Bad Request -- The request was unacceptable,
    often due to missing a required parameter."""

    pass


class ScaleUnauthorized(ScaleException):
    """401 - Unauthorized -- No valid API key provided."""

    pass


class ScaleNotEnabled(ScaleException):
    """402 - Not enabled -- Please contact sales@scaleapi.com before creating
    this type of task."""

    pass


class ScaleResourceNotFound(ScaleException):
    """404 - Not Found -- The requested resource doesn't exist."""

    pass


class ScaleDuplicateTask(ScaleException):
    """409 - Conflict -- The provided idempotency key or unique_id is already
    in use for a different request."""

    pass


class ScaleTooManyRequests(ScaleException):
    """429 - Too Many Requests -- Too many requests hit the API too quickly."""

    pass


class ScaleInternalError(ScaleException):
    """500 - Internal Server Error -- We had a problem with our server.
    Try again later."""

    pass
