from enum import Enum


class EndpointErrorEnum(Enum):
    ZIP_FILE_EXPECTED = "Archive must be .zip"
    DB_CONNECTION_FAILED = "Can't connect to Data Base, please ask administrator"
    NOT_FOUND = "Resource not found"
    FORBIDDEN = "You do not have permission to access this resource"
    REQUEST_VALIDATION = "Input data error"


class GlobalErrorEnum(Enum):
    SOME_EXCEPTION = "Server exception"
