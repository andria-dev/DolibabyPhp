import requests


class DolibabyException(Exception):
    """Base class for other exceptions"""

    pass


class UploadException(Exception):
    pass


class SiteWasDeletedError(UploadException):
    def __init__(self):
        super().__init__("Unable to edit the page because the site was deleted.")


class PayloadUploadError(UploadException):
    payload: str
    response: requests.Response

    def __init__(self, payload: str, response: requests.Response) -> None:
        super().__init__(
            f"Unable to edit the site to include the payload (HTTP status code {response.status_code}).",
            payload,
            response,
        )
        self.payload = payload
        self.response = response


class CleanupScriptUploadError(UploadException):
    site_name: str
    response: requests.Response

    def __init__(self, site_name: str, response: requests.Response) -> None:
        super().__init__(
            f"Unable to edit the site to include the cleanup script (HTTP status code {response.status_code}).",
            site_name,
            response,
        )
        self.site_name = site_name
        self.response = response


class TriggerException(DolibabyException):
    pass


class PayloadTriggerError(TriggerException):
    response: requests.Response

    def __init__(self, response: requests.Response):
        super().__init__(
            f"Unable to trigger the payload (HTTP status code {response.status_code}). Please try again in a minute."
        )
        self.response = response


class CleanupTriggerError(TriggerException):
    response: requests.Response

    def __init__(self, response: requests.Response):
        super().__init__(
            f"Unable to trigger the cleanup script (HTTP status code {response.status_code}). Please try again in a minute."
        )


class CleanupNoOutputError(DolibabyException):
    def __init__(self):
        super().__init__("Cleanup for the exploit did not return any output.")


class CleanupInvalidExitCodeError(DolibabyException):
    output: str | None

    def __init__(self, output: str | None):
        super().__init__(
            f"Cleanup for the exploit returned an invalid exit code: {output}"
        )
        self.output = output
