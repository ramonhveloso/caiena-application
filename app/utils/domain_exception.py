class DomainException(Exception):
    def __init__(self, message: str, code: str, details: str):
        self.code = code
        self.details = details
        self.message = message
        super().__init__(message)


class EntityNotFoundError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, "NOT_FOUND", "")


class EntityAlreadyExistsError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, "ALREADY_EXISTS", "")


class InvalidInputError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_INPUT", "")


class UnauthorizedError(DomainException):
    def __init__(self, message: str):
        super().__init__(message, "UNAUTHORIZED", "")


class ServerError(DomainException):
    def __init__(self):
        super().__init__("Internal server error", "SERVER_ERROR", "")
