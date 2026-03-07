"""Define package errors."""


class WittiotError(Exception):
    """Define a base error."""

    pass


class RequestError(WittiotError):
    """Define an error related to invalid requests."""

    pass


class WebsocketError(WittiotError):
    """Define an error related to generic websocket errors."""

    pass


class FirmwareUpdateUnsupportedError(WittiotError):
    """Define an error for unsupported firmware update operations."""

    pass


class FirmwareUpdateInstallError(WittiotError):
    """Define an error for firmware install failures."""

    pass
